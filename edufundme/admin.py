from django.contrib import admin
from .models import Scholarship, Application, Campaign

@admin.register(Scholarship)
class ScholarshipAdmin(admin.ModelAdmin):
    list_display = ['title', 'provider', 'amount', 'deadline', 'is_active']
    list_filter = ['is_active', 'provider']
    search_fields = ['title', 'description', 'provider']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['user', 'scholarship', 'status', 'applied_at']
    list_filter = ['status', 'scholarship']

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['title', 'target_amount', 'raised_amount', 'school', 'is_active']
    list_filter = ['is_active', 'school']
