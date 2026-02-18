from django.contrib import admin
from .models import Coach, CoachingSession, VirtualClass, ClassEnrollment

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'price_per_hour', 'rating', 'is_active')
    search_fields = ('user__username', 'user__email', 'title')
    list_filter = ('is_active', 'rating')

@admin.register(CoachingSession)
class CoachingSessionAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'student', 'coach', 'date', 'time', 'status')
    search_fields = ('student__username', 'coach__user__username')
    list_filter = ('status', 'date')
    
    def booking_id(self, obj):
        return f"BK-{obj.id}"

@admin.register(VirtualClass)
class VirtualClassAdmin(admin.ModelAdmin):
    list_display = ('title', 'coach', 'subject', 'level', 'start_date', 'enrolled_count', 'capacity')
    search_fields = ('title', 'subject', 'coach__user__username')
    list_filter = ('start_date', 'subject', 'level')

@admin.register(ClassEnrollment)
class ClassEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'virtual_class', 'enrolled_at', 'payment_reference')
    search_fields = ('student__username', 'virtual_class__title', 'payment_reference')
    list_filter = ('enrolled_at',)
