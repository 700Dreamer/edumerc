from django.contrib import admin
from .models import Category, Product

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
