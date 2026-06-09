from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import uuid
import logging

from .models import Transaction, Wallet
from .serializers import InitiatePaymentSerializer, TransactionSerializer, CartCheckoutSerializer, WalletSerializer
from .pesapal_service import PesaPalService
from edushop.models import Order, OrderItem, Product

logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """List current user's transactions"""
        transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='initiate')
    def initiate(self, request):
        serializer = InitiatePaymentSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            description = serializer.validated_data['description']
            
            # 1. Create local transaction
            merchant_ref = f"EDM-{uuid.uuid4().hex[:8].upper()}"
            transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                merchant_reference=merchant_ref,
                transaction_type='ORDER',
                status='PENDING'
            )
            
            # 2. Get PesaPal Service
            pesapal = PesaPalService()
            
            # 3. Submit Order
            # For production, this should be your live frontend URL
            callback_url = getattr(settings, 'PESAPAL_CALLBACK_URL', 'http://localhost:5173/payment-success')
            order_res = pesapal.submit_order(transaction, callback_url)
            
            if order_res and 'redirect_url' in order_res:
                transaction.order_tracking_id = order_res['order_tracking_id']
                transaction.save()
                return Response({
                    "redirect_url": order_res['redirect_url'],
                    "merchant_reference": merchant_ref,
                    "order_tracking_id": order_res['order_tracking_id']
                })
            
            return Response({"error": "Failed to initiate payment with PesaPal"}, status=500)
        
        return Response(serializer.errors, status=400)

    @action(detail=False, methods=['post'], url_path='cart_checkout/initiate')
    def cart_checkout_initiate(self, request):
        """
        Checkout from cart: reads user's Cart, creates Order, and initiates payment.
        No request body needed - cart is read from database.
        """
        # 1. Get user's cart
        try:
            cart = request.user.cart
        except:
            return Response({"error": "Cart not found"}, status=400)
        
        # 2. Validate cart has items
        cart_items = cart.items.all()
        if not cart_items.exists():
            return Response({"error": "Cart is empty"}, status=400)
        
        # 3. Calculate total from current product prices
        total = sum(item.product.price * item.quantity for item in cart_items)
        
        # 4. Create Transaction
        merchant_ref = f"EDM-{uuid.uuid4().hex[:8].upper()}"
        transaction = Transaction.objects.create(
            user=request.user,
            amount=total,
            description=f"Cart Checkout - {cart_items.count()} items",
            merchant_reference=merchant_ref,
            transaction_type='ORDER',
            status='PENDING'
        )
        
        # 5. Create Order
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            status='Pending',
            transaction=transaction
        )
        
        # 6. Create OrderItems from CartItems
        for cart_item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity,
                price=cart_item.product.price  # Use current price
            )
        
        # 7. Initiate PesaPal Payment
        pesapal = PesaPalService()
        callback_url = getattr(settings, 'PESAPAL_CALLBACK_URL', 'http://localhost:5173/payment-success')
        order_res = pesapal.submit_order(transaction, callback_url)
        
        if order_res and 'redirect_url' in order_res:
            transaction.order_tracking_id = order_res['order_tracking_id']
            transaction.save()
            
            return Response({
                "total": float(total),
                "redirect_url": order_res['redirect_url'],
                "merchant_reference": merchant_ref,
                "order_tracking_id": order_res['order_tracking_id'],
                "order_id": order.id
            })
        
        return Response({"error": "Failed to initiate payment with PesaPal"}, status=500)

class PesaPalIPNViewSet(viewsets.ViewSet):
    # permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'], url_path='handler')
    def handler(self, request):
        """
        PesaPal calls this endpoint after status change.
        Query params: OrderTrackingId, OrderMerchantReference, OrderNotificationType
        """
        tracking_id = request.query_params.get('OrderTrackingId')
        merchant_ref = request.query_params.get('OrderMerchantReference')
        
        if tracking_id:
            pesapal = PesaPalService()
            status_res = pesapal.get_transaction_status(tracking_id)
            
            if status_res and 'status_code' in status_res:
                try:
                    transaction = Transaction.objects.get(order_tracking_id=tracking_id)
                    
                    # Map PesaPal status to local status
                    # PesaPal V3 status codes: 0=INVALID, 1=COMPLETED, 2=FAILED, 3=REVERSED
                    if status_res['status_code'] == 1:
                        transaction.status = 'COMPLETED'
                        
                        # Clear user's cart on successful payment
                        try:
                            cart = transaction.user.cart
                            cart.items.all().delete()
                            logger.info(f"Cart cleared for user {transaction.user.username} after successful payment")
                        except Exception as e:
                            logger.warning(f"Could not clear cart for user {transaction.user.username}: {e}")
                            
                    elif status_res['status_code'] == 2:
                        transaction.status = 'FAILED'
                    elif status_res['status_code'] == 3:
                        transaction.status = 'REVERSED'
                    elif status_res['status_code'] == 0:
                        transaction.status = 'INVALID'
                        logger.warning(f"Transaction {tracking_id} marked as INVALID by PesaPal")
                    
                    transaction.payment_method = status_res.get('payment_method', '')
                    transaction.save()
                    
                    # Update linked EduShop orders
                    if transaction.orders.exists():
                        for order in transaction.orders.all():
                            if transaction.status == 'COMPLETED':
                                order.status = 'Paid'
                            elif transaction.status in ['FAILED', 'REVERSED', 'INVALID']:
                                order.status = 'Cancelled'
                            order.save()
                            logger.info(f"Order {order.id} status updated to {order.status}")
                            
                    # Update linked EduQuest MaterialOrders
                    if hasattr(transaction, 'material_orders') and transaction.material_orders.exists():
                        for m_order in transaction.material_orders.all():
                            if transaction.status == 'COMPLETED':
                                m_order.status = 'PAID'
                            elif transaction.status in ['FAILED', 'REVERSED', 'INVALID']:
                                m_order.status = 'CANCELLED'
                            m_order.save()
                            logger.info(f"MaterialOrder {m_order.reference} status updated to {m_order.status}")
                    
                    # Update linked EduCoach CoachingSessions
                    if hasattr(transaction, 'coaching_sessions') and transaction.coaching_sessions.exists():
                        for session in transaction.coaching_sessions.all():
                            if transaction.status == 'COMPLETED':
                                session.payment_status = 'paid'
                            elif transaction.status in ['FAILED', 'REVERSED', 'INVALID']:
                                session.payment_status = 'cancelled'
                            session.save()
                            logger.info(f"CoachingSession {session.booking_id} payment_status updated to {session.payment_status}")
                    
                    # Update linked ClubSubscriptions
                    if hasattr(transaction, 'club_subscriptions') and transaction.club_subscriptions.exists():
                        from django.utils import timezone
                        from datetime import timedelta
                        for subscription in transaction.club_subscriptions.all():
                            if transaction.status == 'COMPLETED':
                                subscription.status = 'active'
                                if subscription.club.subscription_duration_days > 0:
                                    subscription.expires_at = timezone.now() + timedelta(days=subscription.club.subscription_duration_days)
                                else:
                                    subscription.expires_at = None
                            elif transaction.status in ['FAILED', 'REVERSED', 'INVALID']:
                                subscription.status = 'cancelled'
                            subscription.save()
                            logger.info(f"ClubSubscription {subscription.id} status updated to {subscription.status}")

                    logger.info(f"Transaction {tracking_id} updated to {transaction.status}")
                    
                    # 4. Handle Wallet Top-up if completed
                    if transaction.status == 'COMPLETED' and transaction.transaction_type == 'TOPUP':
                        try:
                            wallet = transaction.user.wallet
                            wallet.balance += transaction.amount
                            wallet.save()
                            logger.info(f"Wallet for user {transaction.user.username} topped up by {transaction.amount}")
                        except Exception as e:
                            logger.error(f"Failed to top up wallet for user {transaction.user.username}: {e}")
                            
                except Transaction.DoesNotExist:
                    logger.error(f"Transaction with tracking ID {tracking_id} not found")
            
        # PesaPal expects a response with the same parameters to acknowledge receipt
        return Response(request.query_params)

class WalletViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        """Get current user's wallet info"""
        wallet, created = Wallet.objects.get_or_create(user=request.user)
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def topup(self, request):
        """Initiate wallet top-up"""
        serializer = InitiatePaymentSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            description = serializer.validated_data.get('description', f"Wallet Top-up for {request.user.username}")
            
            # 1. Create top-up transaction
            merchant_ref = f"WTU-{uuid.uuid4().hex[:8].upper()}"
            transaction = Transaction.objects.create(
                user=request.user,
                amount=amount,
                description=description,
                merchant_reference=merchant_ref,
                transaction_type='TOPUP',
                status='PENDING'
            )
            
            # 2. Get PesaPal Service
            pesapal = PesaPalService()
            
            # 3. Submit Order
            callback_url = getattr(settings, 'PESAPAL_CALLBACK_URL', 'http://localhost:5173/payment-success')
            order_res = pesapal.submit_order(transaction, callback_url)
            
            if order_res and 'redirect_url' in order_res:
                transaction.order_tracking_id = order_res['order_tracking_id']
                transaction.save()
                return Response({
                    "redirect_url": order_res['redirect_url'],
                    "merchant_reference": merchant_ref,
                    "order_tracking_id": order_res['order_tracking_id']
                })
            
            return Response({"error": "Failed to initiate top-up with PesaPal"}, status=500)
            
        return Response(serializer.errors, status=400)
