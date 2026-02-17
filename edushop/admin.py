from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, Bundle, Wishlist

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'discount_price', 'stock', 'is_active', 'is_digital', 'category']
    list_filter = ['is_active', 'category', 'is_digital', 'level', 'language']
    search_fields = ['title', 'description', 'sku', 'author']
    prepopulated_fields = {}


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    fields = ['product', 'quantity']
    readonly_fields = ['product', 'quantity']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'item_count']
    inlines = [CartItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
    item_count.short_description = 'Items'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'total_price', 'status', 'transaction', 'created_at']
    list_filter = ['status']
    raw_id_fields = ['transaction']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'quantity', 'price']

@admin.register(Bundle)
class BundleAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'is_active']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['user', 'updated_at']
    filter_horizontal = ['products']
