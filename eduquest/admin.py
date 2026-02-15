from django.contrib import admin
from .models import Material, MaterialOrder

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['title', 'material_type', 'session', 'price', 'uploaded_at']
    list_filter = ['material_type', 'session']
    search_fields = ['title', 'description']

@admin.register(MaterialOrder)
class MaterialOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'material', 'status', 'ordered_at']
    list_filter = ['status']
    search_fields = ['user__username', 'material__title']
