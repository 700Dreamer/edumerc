from rest_framework import serializers
from .models import Transaction, Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['balance', 'currency', 'updated_at']

class InitiatePaymentSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    description = serializers.CharField(max_length=255)
    
class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

class CartCheckoutSerializer(serializers.Serializer):
    """Serializer for cart checkout payment"""
    subtotal = serializers.DecimalField(max_digits=12, decimal_places=2)
    products = serializers.ListField(
        child=serializers.DictField(),
        help_text="Array of products with id, quantity, and price"
    )
    description = serializers.CharField(max_length=255, default="Cart Checkout")
