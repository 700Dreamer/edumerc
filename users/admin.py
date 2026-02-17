from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from edushop.models import Cart, CartItem, Wishlist, Order, OrderItem
from payments.models import Transaction

# Inlines
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity']

class CartInline(admin.StackedInline):
    model = Cart
    can_delete = False
    show_change_link = True
    verbose_name_plural = 'Cart'

class WishlistInline(admin.StackedInline):
    model = Wishlist
    can_delete = False
    filter_horizontal = ['products']
    verbose_name_plural = 'Wishlist'

class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    readonly_fields = ['merchant_reference', 'amount', 'currency', 'status', 'order_tracking_id', 'created_at']
    can_delete = False
    verbose_name_plural = 'Transactions'

class OrderInline(admin.TabularInline):
    model = Order
    extra = 0
    readonly_fields = ['total_price', 'status', 'transaction', 'created_at']
    can_delete = False
    verbose_name_plural = 'Orders'

# User admin
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),
    )
    inlines = [ProfileInline, CartInline, WishlistInline, OrderInline, TransactionInline]

admin.site.register(User, CustomUserAdmin)
