from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile
from edushop.serializers import CartSerializer, WishlistSerializer, OrderSerializer

User = get_user_model()

def get_default_avatar_url(username):
    import hashlib
    import dicebear
    styles = ['toon-head', 'personas', 'miniavs', 'dylan', 'big-ears', 'avataaars', 'adventurer']
    h = int(hashlib.md5(username.encode('utf-8')).hexdigest(), 16)
    style = styles[h % len(styles)]
    av = dicebear.create_avatar(style=style, seed=username)
    return av.url_png

class ProfileSerializer(serializers.ModelSerializer):
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, source='user.role')
    is_coach = serializers.ReadOnlyField(source='user.is_coach')
    wallet_balance = serializers.DecimalField(source='user.wallet.balance', max_digits=12, decimal_places=2, read_only=True)
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['bio', 'avatar', 'preferences', 'created_at', 'updated_at', 'first_name', 'last_name', 'role', 'is_coach', 'wallet_balance']
        read_only_fields = ['created_at', 'updated_at']

    def get_avatar(self, obj):
        if obj.avatar:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.avatar.url)
            return obj.avatar.url
        return get_default_avatar_url(obj.user.username)

    def update(self, instance, validated_data):
        # Extract user data (nested in source)
        user_data = validated_data.pop('user', {})
        role = user_data.get('role')
        
        # Update user role if provided
        if role:
            instance.user.role = role
            instance.user.save()
            
        # Update profile fields
        return super().update(instance, validated_data)

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
