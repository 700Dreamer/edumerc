from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile
from django import forms
from edushop.models import Cart, CartItem, Wishlist, Order, OrderItem, Product
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


class CartAdminForm(forms.ModelForm):
    quick_add_product = forms.ModelChoiceField(
        queryset=Product.objects.filter(is_active=True),
        required=False,
        label="Quick Add Product",
        help_text="Select a product to add to this cart"
    )
    quick_add_quantity = forms.IntegerField(
        initial=1,
        min_value=1,
        required=False,
        label="Quantity"
    )

    class Meta:
        model = Cart
        fields = '__all__'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
            
        # Handle quick add
        product = self.cleaned_data.get('quick_add_product')
        quantity = self.cleaned_data.get('quick_add_quantity')
        
        if product and quantity:
            # Check if item exists
            item, created = CartItem.objects.get_or_create(
                cart=instance,
                product=product,
                defaults={'quantity': 0}
            )
            item.quantity += quantity
            item.save()
            
        return instance

class CartInline(admin.StackedInline):
    model = Cart
    form = CartAdminForm
    can_delete = False
    show_change_link = True
    verbose_name_plural = 'Cart'
    fields = ['created_at', 'quick_add_product', 'quick_add_quantity']
    readonly_fields = ['created_at']




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
