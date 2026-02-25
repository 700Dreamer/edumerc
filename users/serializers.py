from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile
from edushop.serializers import CartSerializer, WishlistSerializer, OrderSerializer

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    role = serializers.ReadOnlyField(source='user.role')
    is_coach = serializers.ReadOnlyField(source='user.is_coach')

    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'preferences', 'created_at', 'updated_at', 'first_name', 'last_name', 'role', 'is_coach']
        read_only_fields = ['created_at', 'updated_at']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)
    cart = CartSerializer(read_only=True)
    wishlist = WishlistSerializer(read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'is_coach', 'profile', 'cart', 'wishlist', 'orders']
        read_only_fields = ['id', 'is_coach']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'STUDENT'),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user
