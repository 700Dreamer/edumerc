from django.db import models
from django.utils.translation import gettext_lazy as _

class Section(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text=_("e.g. Primary, Secondary"))
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = _("Section")
        verbose_name_plural = _("Sections")

    def __str__(self):
        return self.name

class Level(models.Model):
    name = models.CharField(max_length=100, help_text=_("e.g. P.1, S.4"))
    section = models.ForeignKey(Section, on_delete=models.CASCADE, related_name='levels')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = _("Level")
        verbose_name_plural = _("Levels")

    def __str__(self):
        return f"{self.name} ({self.section.name})"

class Subject(models.Model):
    name = models.CharField(max_length=255)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='subjects')
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'name']
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return f"{self.name} - {self.level.name}"

class Topic(models.Model):
    title = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = _("Topic")
        verbose_name_plural = _("Topics")

    def __str__(self):
        return self.title

class Subtopic(models.Model):
    title = models.CharField(max_length=255)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = _("Subtopic")
        verbose_name_plural = _("Subtopics")

    def __str__(self):
        return self.title

class Lesson(models.Model):
    title = models.CharField(max_length=255)
    subtopic = models.ForeignKey(Subtopic, on_delete=models.CASCADE, related_name='lessons')
    objectives = models.TextField(blank=True, null=True)
    content = models.TextField(help_text=_("Main content unit."))
    video_url = models.URLField(blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_published = models.BooleanField(default=False)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")

    def __str__(self):
        return self.title

class Assessment(models.Model):
    title = models.CharField(max_length=255)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='assessments')
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = _("Assessment")
        verbose_name_plural = _("Assessments")

    def __str__(self):
        return self.title

# ---- New Club‑related models -------------------------------------------------

# Import for the new models defined in a separate file
from .club_models import *  # noqa: F401,F403
