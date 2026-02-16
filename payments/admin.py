from django.contrib import admin
from .models import Transaction, PesaPalIPN

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('merchant_reference', 'user', 'amount', 'currency', 'status', 'created_at')
    list_filter = ('status', 'currency')
    search_fields = ('merchant_reference', 'order_tracking_id', 'user__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(PesaPalIPN)
class PesaPalIPNAdmin(admin.ModelAdmin):
    list_display = ('ipn_id', 'url', 'created_at')
