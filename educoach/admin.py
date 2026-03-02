from django.contrib import admin
from .models import Coach, CoachingSession, VirtualClass, ClassEnrollment, CoachAvailabilityRange, CoachEarnings, HMSSession, HMSPeer

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'price_per_hour', 'rating', 'is_active')
    search_fields = ('user__username', 'user__email', 'title')
    list_filter = ('is_active', 'rating')

@admin.register(CoachingSession)
class CoachingSessionAdmin(admin.ModelAdmin):
    list_display = ('booking_id', 'student', 'coach', 'date', 'start_time', 'end_time', 'status')
    search_fields = ('student__username', 'coach__user__username', 'booking_id')
    list_filter = ('status', 'date')

@admin.register(CoachAvailabilityRange)
class CoachAvailabilityRangeAdmin(admin.ModelAdmin):
    list_display = ('coach', 'get_day_of_week_display', 'start_time', 'end_time', 'is_active')
    search_fields = ('coach__user__username', 'coach__user__email')
    list_filter = ('day_of_week', 'is_active')

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

@admin.register(CoachEarnings)
class CoachEarningsAdmin(admin.ModelAdmin):
    list_display = ('coach', 'transaction_type', 'amount', 'status', 'date')
    search_fields = ('coach__user__username', 'transaction_id')
    list_filter = ('transaction_type', 'status', 'date')

class HMSPeerInline(admin.TabularInline):
    model = HMSPeer
    extra = 0
    readonly_fields = ('peer_id', 'name', 'role', 'user_id', 'joined_at', 'left_at')

@admin.register(HMSSession)
class HMSSessionAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_id', 'active', 'created_at', 'ended_at')
    search_fields = ('id', 'room_id')
    list_filter = ('active', 'created_at')
    inlines = [HMSPeerInline]

@admin.register(HMSPeer)
class HMSPeerAdmin(admin.ModelAdmin):
    list_display = ('peer_id', 'name', 'role', 'session', 'joined_at', 'left_at')
    search_fields = ('name', 'peer_id', 'user_id')
    list_filter = ('role', 'joined_at')
