from django.contrib import admin
from .models import School, SchoolGalleryImage, SchoolEvent, SchoolAdministrator, PromotionalMaterial, SchoolReview

class GalleryInline(admin.TabularInline):
    model = SchoolGalleryImage
    extra = 1

class EventInline(admin.TabularInline):
    model = SchoolEvent
    extra = 1

class AdminInline(admin.TabularInline):
    model = SchoolAdministrator
    extra = 1

class PromoInline(admin.TabularInline):
    model = PromotionalMaterial
    extra = 1

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ['name', 'location', 'email', 'created_at']
    search_fields = ['name', 'location', 'motto']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [GalleryInline, EventInline, AdminInline, PromoInline]

@admin.register(SchoolEvent)
class SchoolEventAdmin(admin.ModelAdmin):
    list_display = ['title', 'school', 'date']
    list_filter = ['school']

@admin.register(SchoolAdministrator)
class SchoolAdministratorAdmin(admin.ModelAdmin):
    list_display = ['name', 'role', 'school']
    list_filter = ['school', 'role']
