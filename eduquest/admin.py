from django.contrib import admin
from .models import Material, MaterialOrder

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'material_type', 'session', 'price', 'uploaded_at']
    list_filter = ['material_type', 'session']
    search_fields = ['title', 'description']

@admin.register(MaterialOrder)
class MaterialOrderAdmin(admin.ModelAdmin):
    list_display = ['reference', 'user', 'school_name', 'status', 'expected_delivery_date', 'total_sets', 'estimated_amount', 'ordered_at']
    list_filter = ['status', 'session']
    search_fields = ['reference', 'user__username', 'school_name', 'representative', 'email', 'phone']
