from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

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

class CoachingSession(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    coach = models.ForeignKey(Coach, on_delete=models.CASCADE, related_name='sessions')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='booked_sessions')
    
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField(default=1, help_text="Duration in hours")
    
    note = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    meeting_link = models.URLField(blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', '-time']

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
