from django.db import models
from django.conf import settings

class Club(models.Model):
    CATEGORY_CHOICES = (
        ('Social', 'Social'),
        ('Teacher', 'Teacher'),
        ('Subject', 'Subject'),
    )
    
    LEVEL_CHOICES = (
        ('Nursery', 'Nursery'),
        
        ('P1', 'Primary 1'), ('P2', 'Primary 2'), ('P3', 'Primary 3'), 
        ('P4', 'Primary 4'), ('P5', 'Primary 5'), ('P6', 'Primary 6'), ('P7', 'Primary 7'),
        
        ('S1', 'Secondary 1'), ('S2', 'Secondary 2'), ('S3', 'Secondary 3'), 
        ('S4', 'Secondary 4'), ('S5', 'Secondary 5'), ('S6', 'Secondary 6'),
        
        ('General', 'General (All Levels)'),
    )

    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='General', blank=True, null=True)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='club_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.level})" if self.level else self.name

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
