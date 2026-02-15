from django.db import models
from django.conf import settings

class MainCategory(models.Model):
    name = models.CharField(max_length=255) # e.g., Subject, Social, Teachers
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Main Categories"

class SubCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, related_name='subcategories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255) # e.g., Nursery, P7, Sports
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.main_category.name} > {self.name}"

    class Meta:
        verbose_name_plural = "Sub Categories"
        ordering = ['order', 'name']

class Club(models.Model):
    name = models.CharField(max_length=255) # e.g., Math Club, Sports Club
    subcategory = models.ForeignKey(SubCategory, related_name='clubs', on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='club_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.subcategory.name})"

class Topic(models.Model):
    club = models.ForeignKey(Club, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.title} - {self.club.name}"

class Lesson(models.Model):
    TYPE_CHOICES = (
        ('Text', 'Text Content'),
        ('Video', 'Video URL'),
        ('File', 'File Download'),
    )

    topic = models.ForeignKey(Topic, related_name='lessons', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Text')
    text_content = models.TextField(blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)
    file_content = models.FileField(upload_to='lesson_files/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return self.title

class RoleModel(models.Model):
    club = models.ForeignKey(Club, related_name='role_models', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    bio = models.TextField()
    contribution = models.TextField(help_text="Their contribution to this field")
    image = models.ImageField(upload_to='role_models/', blank=True, null=True)

    def __str__(self):
        return self.name

class PracticalApplication(models.Model):
    club = models.ForeignKey(Club, related_name='practical_apps', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    guide = models.TextField(help_text="Step-by-step guide or explanation")
    image = models.ImageField(upload_to='practical_apps/', blank=True, null=True)

    def __str__(self):
        return self.title

class ClubDiscussion(models.Model):
    club = models.ForeignKey(Club, related_name='discussions', on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # Uncomment when auth is fully integrated
    user_name = models.CharField(max_length=255, default='Anonymous') # Identifying user for now
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message by {self.user_name} on {self.club.name}"

class AskAIQuery(models.Model):
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=255, default='Anonymous')
    club = models.ForeignKey(Club, related_name='ai_queries', on_delete=models.CASCADE)
    query = models.TextField()
    response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query on {self.club.name}"
