from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import uuid

class Coach(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coach_profile')
    title = models.CharField(max_length=255, help_text="e.g. Senior P.7 Science Expert")
    experience = models.CharField(max_length=100, help_text="e.g. 12 Years")
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Online Status")
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)
    review_count = models.PositiveIntegerField(default=0)
    
    # Store lists as JSON
    subjects = models.JSONField(default=list, blank=True)
    levels = models.JSONField(default=list, blank=True)
    badges = models.JSONField(default=list, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} - {self.title}"

class CoachAvailabilityRange(models.Model):
    DAYS = [(i, name) for i, name in enumerate(
        ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    )]
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='availability_ranges')
    day_of_week = models.IntegerField(choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['day_of_week', 'start_time']
        indexes = [models.Index(fields=['coach', 'day_of_week'])]

    def clean(self):
        if self.start_time and self.end_time and self.start_time >= self.end_time:
            raise ValidationError("start_time must be before end_time.")

    def __str__(self):
        return f"{self.coach} - {self.get_day_of_week_display()} ({self.start_time} to {self.end_time})"

class CoachingSession(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )

    booking_id = models.CharField(max_length=20, unique=True, blank=True, null=True)

    coach = models.ForeignKey(Coach, on_delete=models.PROTECT, related_name='sessions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='booked_sessions')
    
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    duration = models.PositiveIntegerField(default=1, help_text="Duration in hours")
    
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # NEW: Payment tracking
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction = models.ForeignKey('payments.Transaction', on_delete=models.SET_NULL, null=True, blank=True, related_name='coaching_sessions')

    meeting_link = models.CharField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-start_time']
        indexes = [
            models.Index(fields=['coach', 'date', 'status']),
        ]

    def save(self, *args, **kwargs):
        if not self.booking_id:
            self.booking_id = f"BK-{uuid.uuid4().hex[:6].upper()}"
        if self.start_time and self.duration and self.date and not self.end_time:
            start_dt = datetime.combine(self.date, self.start_time)
            end_dt = start_dt + timedelta(hours=self.duration)
            self.end_time = end_dt.time()
        
        # Calculate total_price if not set
        if self.coach and self.duration and (not self.total_price or self.total_price == 0):
            self.total_price = self.coach.price_per_hour * self.duration
            
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Session: {self.student} with {self.coach} on {self.date}"

class VirtualClass(models.Model):
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='virtual_classes')
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=100)
    level = models.CharField(max_length=50)
    
    start_date = models.DateField()
    schedule = models.CharField(max_length=255, help_text="e.g. Every Monday & Wednesday, 4:00 PM")
    duration_weeks = models.PositiveIntegerField(default=1)
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    capacity = models.PositiveIntegerField(default=50)
    
    description = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def enrolled_count(self):
        return self.enrollments.count()

    def __str__(self):
        return f"{self.title} ({self.coach})"

class ClassEnrollment(models.Model):
    virtual_class = models.ForeignKey(VirtualClass, on_delete=models.CASCADE, related_name='enrollments')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='class_enrollments')
    
    payment_reference = models.CharField(max_length=255, blank=True)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('virtual_class', 'student')

    def __str__(self):
        return f"{self.student} in {self.virtual_class}"

class CoachEarnings(models.Model):
    TRANSACTION_TYPES = (
        ('EARNING', 'Earning'),
        ('WITHDRAWAL', 'Withdrawal'),
    )
    STATUS_CHOICES = (
        ('EXPECTED', 'Expected'),
        ('EARNED', 'Earned'),
        ('WITHDRAWN', 'Withdrawn'),
        ('CANCELLED', 'Cancelled'),
    )
    
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='ledger')
    session = models.ForeignKey(CoachingSession, on_delete=models.SET_NULL, null=True, blank=True, related_name='earnings_records')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='EXPECTED')
    
    # Financial Metadata
    duration = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    date = models.DateField(null=True, blank=True)
    transaction_id = models.CharField(max_length=100, help_text="Session Booking ID or Withdrawal ID")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Coach Earnings"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.coach.user.username} - {self.transaction_type} - {self.amount}"


# ---------------------------------------------------------------------------
# Signals: keep user.is_coach in sync with the Coach profile
# ---------------------------------------------------------------------------

@receiver(post_save, sender=Coach)
def sync_is_coach_on_save(sender, instance, created, **kwargs):
    """Set user.is_coach = True whenever a Coach profile is created or saved."""
    user = instance.user
    if not user.is_coach:
        user.is_coach = True
        user.save(update_fields=['is_coach'])


@receiver(post_delete, sender=Coach)
def sync_is_coach_on_delete(sender, instance, **kwargs):
    """Reset user.is_coach = False when the Coach profile is deleted."""
    user = instance.user
    if user.is_coach:
        user.is_coach = False
        user.save(update_fields=['is_coach'])

@receiver(post_save, sender=CoachingSession)
def create_ledger_entry_on_session_save(sender, instance, created, **kwargs):
    """
    Sync CoachingSession with CoachEarnings ledger.
    - New booking (pending/confirmed) -> EXPECTED
    - Status 'completed' -> EARNED
    - Status 'cancelled' -> CANCELLED
    """
    status_map = {
        'pending': 'EXPECTED',
        'confirmed': 'EXPECTED',
        'completed': 'EARNED',
        'cancelled': 'CANCELLED'
    }
    
    ledger_status = status_map.get(instance.status, 'EXPECTED')
    
    # Use update_or_create to ensure one ledger record per session
    CoachEarnings.objects.update_or_create(
        session=instance,
        defaults={
            'coach': instance.coach,
            'student': instance.student,
            'amount': instance.total_price,
            'transaction_type': 'EARNING',
            'status': ledger_status,
            'duration': instance.duration,
            'price': instance.coach.price_per_hour,
            'date': instance.date,
            'transaction_id': instance.booking_id
        }
    )

@receiver(post_save, sender='payments.Withdrawal')
def create_ledger_entry_on_withdrawal_save(sender, instance, **kwargs):
    """
    Sync Withdrawal with CoachEarnings ledger when COMPLETED.
    """
    if instance.status == 'COMPLETED':
        # Check if we already have this withdrawal in the ledger
        if not CoachEarnings.objects.filter(transaction_id=str(instance.id), transaction_type='WITHDRAWAL').exists():
            try:
                coach = instance.user.coach_profile
                CoachEarnings.objects.create(
                    coach=coach,
                    amount=instance.amount,
                    transaction_type='WITHDRAWAL',
                    status='WITHDRAWN',
                    transaction_id=str(instance.id),
                    date=instance.updated_at.date()
                )
            except Exception:
                # User might not have a coach profile or other issues
                pass

class HMSSession(models.Model):
    id = models.CharField(max_length=100, primary_key=True, unique=True)
    room_id = models.CharField(max_length=100)
    internal_session = models.ForeignKey('CoachingSession', on_delete=models.SET_NULL, null=True, blank=True, related_name='hms_sessions')
    customer_id = models.CharField(max_length=100)
    app_id = models.CharField(max_length=100)
    user_id = models.CharField(blank=True, max_length=100, null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"HMS Session {self.id} (Room: {self.room_id})"

class HMSPeer(models.Model):
    session = models.ForeignKey(HMSSession, on_delete=models.CASCADE, related_name='peers')
    peer_id = models.CharField(max_length=100)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100)
    user_id = models.CharField(max_length=255)
    joined_at = models.DateTimeField()
    left_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        unique_together = ('session', 'peer_id')

    def __str__(self):
        return f"{self.name} ({self.role}) in {self.session.id}"
