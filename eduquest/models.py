from django.db import models
from django.conf import settings

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
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='material_orders')
    material = models.ForeignKey(Material, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    ordered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user.username} for {self.material.title} - {self.status}"
