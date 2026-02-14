from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=255, help_text="e.g., Kampala, Nakawa Division")
    motto = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    
    # Branding
    logo = models.ImageField(upload_to='school_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='school_covers/', blank=True, null=True)
    
    # Multimedia
    video_360_url = models.URLField(blank=True, null=True, help_text="Link to 360 video (e.g., YouTube/Vimeo)")
    school_anthem = models.FileField(upload_to='school_anthems/', blank=True, null=True, help_text="Audio file for school anthem")
    
    # Contact
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    website = models.URLField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class SchoolGalleryImage(models.Model):
    school = models.ForeignKey(School, related_name='gallery', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='school_gallery/')
    caption = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.school.name}"

class SchoolEvent(models.Model):
    school = models.ForeignKey(School, related_name='events', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField()
    image = models.ImageField(upload_to='school_events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.title} at {self.school.name}"

class SchoolAdministrator(models.Model):
    school = models.ForeignKey(School, related_name='administrators', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=100, help_text="e.g., Headteacher, Deputy Headteacher")
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='school_staff/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.role}) - {self.school.name}"

class PromotionalMaterial(models.Model):
    TYPE_CHOICES = (
        ('Brochure', 'Brochure'),
        ('Flyer', 'Flyer'),
        ('Prospectus', 'Prospectus'),
        ('Other', 'Other'),
    )
    school = models.ForeignKey(School, related_name='promotional_materials', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='school_promos/')
    material_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default='Brochure')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.material_type})"
