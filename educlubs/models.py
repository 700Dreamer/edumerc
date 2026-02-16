from django.db import models
from django.conf import settings
from django.utils.text import slugify

class MainCategory(models.Model):
    name = models.CharField(max_length=255) # Subject, Social, Teachers
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Main Categories"

# --- SUBJECT BRANCH (Academic) ---

class SubjectLevel(models.Model):
    main_category = models.ForeignKey(MainCategory, related_name='subject_levels', on_delete=models.CASCADE)
    name = models.CharField(max_length=255) # Nursery, P7, S6
    slug = models.SlugField(unique=True)
    order = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Level: {self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['order']

class SubjectClub(models.Model):
    level = models.ForeignKey(SubjectLevel, related_name='clubs', on_delete=models.CASCADE)
    name = models.CharField(max_length=255) # Math Club, Science Club
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="📚")
    cover_image = models.ImageField(upload_to='subject_club_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.level.name})"

class Topic(models.Model):
    subject_club = models.ForeignKey('SubjectClub', related_name='topics', on_delete=models.CASCADE, null=True, blank=True)
    social_club = models.ForeignKey('SocialClub', related_name='topics', on_delete=models.CASCADE, null=True, blank=True)
    teacher_club = models.ForeignKey('TeacherClub', related_name='topics', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        club_name = self.subject_club.name if self.subject_club else (self.social_club.name if self.social_club else self.teacher_club.name if self.teacher_club else "Unknown")
        return f"{self.title} - {club_name}"

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

# --- SOCIAL BRANCH (Interests) ---

class SocialGroup(models.Model):
    main_category = models.ForeignKey(MainCategory, related_name='social_groups', on_delete=models.CASCADE)
    name = models.CharField(max_length=255) # Sports, Business
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"Group: {self.name}"

class SocialClub(models.Model):
    group = models.ForeignKey(SocialGroup, related_name='clubs', on_delete=models.CASCADE)
    name = models.CharField(max_length=255) # Football, Chess
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="🤝")
    facilitator = models.CharField(max_length=255, blank=True)
    cover_image = models.ImageField(upload_to='social_club_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.group.name})"

class ClubDiscussion(models.Model):
    subject_club = models.ForeignKey('SubjectClub', related_name='discussions', on_delete=models.CASCADE, null=True, blank=True)
    social_club = models.ForeignKey('SocialClub', related_name='discussions', on_delete=models.CASCADE, null=True, blank=True)
    teacher_club = models.ForeignKey('TeacherClub', related_name='discussions', on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        club_name = self.subject_club.name if self.subject_club else (self.social_club.name if self.social_club else self.teacher_club.name if self.teacher_club else "Unknown")
        return f"Discussion in {club_name} by {self.user.username}"

# --- TEACHER BRANCH (Professional) ---

class TeacherCategory(models.Model):
    main_category = models.ForeignKey(MainCategory, related_name='teacher_categories', on_delete=models.CASCADE)
    name = models.CharField(max_length=255) # Administrative, Professional
    slug = models.SlugField(unique=True)
    is_administrative = models.BooleanField(default=False)

    def __str__(self):
        return f"Category: {self.name}"

class TeacherClub(models.Model):
    category = models.ForeignKey(TeacherCategory, related_name='clubs', on_delete=models.CASCADE)
    name = models.CharField(max_length=255) # Headteachers Forum
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, default="👨‍🏫")
    duration = models.CharField(max_length=100, blank=True, help_text="e.g. 6 months")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.category.name})"

# --- COMMON MODELS ---

class RoleModel(models.Model):
    subject_club = models.ForeignKey('SubjectClub', related_name='role_models', on_delete=models.CASCADE, null=True, blank=True)
    social_club = models.ForeignKey('SocialClub', related_name='role_models', on_delete=models.CASCADE, null=True, blank=True)
    teacher_club = models.ForeignKey('TeacherClub', related_name='role_models', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    bio = models.TextField()
    contribution = models.TextField()
    image = models.ImageField(upload_to='role_models/', blank=True, null=True)

    def __str__(self):
        return self.name

class PracticalApplication(models.Model):
    subject_club = models.ForeignKey('SubjectClub', related_name='practical_apps', on_delete=models.CASCADE, null=True, blank=True)
    social_club = models.ForeignKey('SocialClub', related_name='practical_apps', on_delete=models.CASCADE, null=True, blank=True)
    teacher_club = models.ForeignKey('TeacherClub', related_name='practical_apps', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    guide = models.TextField()
    image = models.ImageField(upload_to='practical_apps/', blank=True, null=True)

    def __str__(self):
        return self.title

class AskAIQuery(models.Model):
    subject_club = models.ForeignKey('SubjectClub', related_name='ai_queries', on_delete=models.CASCADE, null=True, blank=True)
    social_club = models.ForeignKey('SocialClub', related_name='ai_queries', on_delete=models.CASCADE, null=True, blank=True)
    teacher_club = models.ForeignKey('TeacherClub', related_name='ai_queries', on_delete=models.CASCADE, null=True, blank=True)
    user_name = models.CharField(max_length=255)
    query = models.TextField()
    response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Query by {self.user_name} in {self.subject_club.name if self.subject_club else 'General'}"
