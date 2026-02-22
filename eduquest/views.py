from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import uuid

from .models import Material, MaterialOrder
from .serializers import MaterialSerializer, MaterialOrderSerializer
from payments.models import Transaction
from payments.pesapal_service import PesaPalService

class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filterset_fields = ['material_type', 'session']


class MaterialOrderViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = MaterialOrderSerializer

    def get_queryset(self):
        return MaterialOrder.objects.filter(user=self.request.user).order_by('-ordered_at')

    def perform_create(self, serializer):
        data = self.request.data
        school = data.get('school', {})

        serializer.save(
            user=self.request.user,
            session=data.get('session', ''),
            school_name=school.get('name', ''),
            representative=school.get('representative', ''),
            location=school.get('location', ''),
            address=school.get('address', ''),
            phone=school.get('phone', ''),
            email=school.get('email', ''),
            delivery_date=school.get('delivery_date') or None,
            levels_data=data.get('levels', []),
            total_sets=data.get('total_sets', 0),
            estimated_amount=data.get('estimated_amount', 0),
            material_id=data.get('material'),
        )

    @action(detail=True, methods=['post'], url_path='initiate-payment')
    def initiate_payment(self, request, pk=None):
        order = self.get_object()
        
        # 1. Ensure the order is ready for payment
        if order.status != 'APPROVED':
            return Response(
                {"error": "Order must be APPROVED before payment can be initiated."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        if order.estimated_amount <= 0:
             return Response(
                {"error": "Invalid estimated amount. Cannot proceed with payment."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        # 2. Check if a valid transaction already exists to prevent duplicate requests
        if order.transaction and order.transaction.status == 'PENDING' and order.transaction.order_tracking_id:
             return Response(
                 {"error": "A pending payment already exists for this order."},
                 status=status.HTTP_400_BAD_REQUEST
             )
        
        # 3. Create a local Transaction
        merchant_ref = f"EQ-PMT-{uuid.uuid4().hex[:8].upper()}"
        transaction = Transaction.objects.create(
            user=request.user,
            amount=order.estimated_amount,
            description=f"Payment for EduQuest Order {order.reference}",
            merchant_reference=merchant_ref,
            status='PENDING'
        )
        
        # Link the transaction to the order
        order.transaction = transaction
        order.save(update_fields=['transaction'])
        
        # 4. Get PesaPal Service and Submit
        pesapal = PesaPalService()
        callback_url = getattr(settings, 'PESAPAL_CALLBACK_URL', 'http://localhost:5173/payment-success')
        order_res = pesapal.submit_order(transaction, callback_url)
        
        if order_res and 'redirect_url' in order_res:
            transaction.order_tracking_id = order_res['order_tracking_id']
            transaction.save(update_fields=['order_tracking_id'])
            
            return Response({
                "redirect_url": order_res['redirect_url'],
                "merchant_reference": merchant_ref,
                "order_tracking_id": order_res['order_tracking_id'],
                "order_id": order.id
            })
            
        return Response({"error": "Failed to initiate payment with PesaPal"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
