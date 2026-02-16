from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings
import uuid
import logging

from .models import Transaction
from .serializers import InitiatePaymentSerializer, TransactionSerializer
from .pesapal_service import PesaPalService

logger = logging.getLogger(__name__)

class PaymentViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    
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

class PesaPalIPNViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
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
                    # 1: Completed, 0: Failed, 2: Reversed
                    if status_res['status_code'] == 1:
                        transaction.status = 'COMPLETED'
                    elif status_res['status_code'] == 0:
                        transaction.status = 'FAILED'
                    elif status_res['status_code'] == 2:
                        transaction.status = 'REVERSED'
                    
                    transaction.payment_method = status_res.get('payment_method', '')
                    transaction.save()
                    
                    logger.info(f"Transaction {tracking_id} updated to {transaction.status}")
                    
                except Transaction.DoesNotExist:
                    logger.error(f"Transaction with tracking ID {tracking_id} not found")
            
        # PesaPal expects a response with the same parameters to acknowledge receipt
        return Response(request.query_params)
