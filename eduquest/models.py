from django.db import models
from django.conf import settings
import uuid

def generate_quest_reference():
    return f"EQ-{uuid.uuid4().hex[:8].upper()}"

class Material(models.Model):
    MATERIAL_TYPE_CHOICES = (
        ('EXAM', 'Sessional Exam'),
        ('PAST_PAPER', 'Past Paper'),
        ('OTHER', 'Other Material'),
    )
    SESSION_CHOICES = (
        ('BOT', 'Beginning of Term'),
        ('MID', 'Mid Term'),
        ('EOT', 'End of Term'),
        ('NONE', 'None'),
    )

    title = models.CharField(max_length=255)
    material_type = models.CharField(max_length=20, choices=MATERIAL_TYPE_CHOICES, default='OTHER')
    session = models.CharField(max_length=10, choices=SESSION_CHOICES, default='NONE')
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.material_type})"

class MaterialOrder(models.Model):
    STATUS_CHOICES = (
        ('PENDING',   'Pending'),
        ('APPROVED',  'Approved'),
        ('DECLINED',  'Declined'),
        ('PAID',      'Paid'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    SESSION_CHOICES = (
        ('BOT', 'Beginning of Term'),
        ('MID', 'Mid Term'),
        ('EOT', 'End of Term'),
    )

    # Core (existing)
    user       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='material_orders')
    material   = models.ForeignKey(Material, null=True, blank=True, on_delete=models.SET_NULL, related_name='orders')
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    ordered_at = models.DateTimeField(auto_now_add=True)

    # NEW: Order reference
    reference  = models.CharField(max_length=20, unique=True, default=generate_quest_reference)

    # NEW: Session type (BOT/MID/EOT)
    session    = models.CharField(max_length=10, choices=SESSION_CHOICES, blank=True)

    # NEW: School / delivery details
    school_name    = models.CharField(max_length=200, blank=True)
    representative = models.CharField(max_length=200, blank=True)
    location       = models.CharField(max_length=200, blank=True)
    address        = models.CharField(max_length=300, blank=True)
    phone          = models.CharField(max_length=20, blank=True)
    email          = models.EmailField(blank=True)
    delivery_date  = models.DateField(null=True, blank=True)  # User requested delivery date
    expected_delivery_date = models.DateField(null=True, blank=True, help_text="Date the administration manages to deliver by")

    # NEW: Flexible levels + subjects snapshot
    levels_data      = models.JSONField(default=list, blank=True)
    total_sets       = models.PositiveIntegerField(default=0)
    estimated_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    # NEW: Payment link
    transaction      = models.ForeignKey('payments.Transaction', on_delete=models.SET_NULL, null=True, blank=True, related_name='material_orders')

    def __str__(self):
        return f"{self.reference} — {self.school_name} ({self.status})"
