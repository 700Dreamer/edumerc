# club_models.py

"""Models related to EduClubs that are not part of the curriculum hierarchy.
These models provide the data the front‑end expects for a club's detail page.
"""

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Club(models.Model):
    class ClubType(models.TextChoices):
        SUBJECT = "subject", _("Subject Club")
        SOCIAL = "social", _("Social Club")
        TEACHER = "teacher", _("Teacher Club")

    name = models.CharField(max_length=255)
    icon = models.CharField(max_length=64, help_text=_("Icon name or emoji"))
    description = models.TextField(blank=True)
    level = models.ForeignKey(
        "Level", on_delete=models.CASCADE, related_name="clubs"
    )
    subject = models.ForeignKey(
        "Subject", on_delete=models.SET_NULL, null=True, blank=True, related_name="clubs"
    )
    type = models.CharField(
        max_length=10, choices=ClubType.choices, default=ClubType.SUBJECT
    )
    popular = models.BooleanField(default=False, help_text=_("Show popular badge"))

    class Meta:
        verbose_name = _("Club")
        verbose_name_plural = _("Clubs")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.level})"


class Note(models.Model):
    """Free‑form academic material – header and rich‑text content (stored as Markdown)."""

    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="notes")
    header = models.CharField(max_length=255)
    content = models.TextField(help_text=_("Markdown content for the note"))
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _("Note")
        verbose_name_plural = _("Notes")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.header} (Club: {self.club.name})"


class RoleModel(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="role_models")
    name = models.CharField(max_length=255)
    contribution = models.TextField()
    image = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = _("Role Model")
        verbose_name_plural = _("Role Models")
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} (Club: {self.club.name})"


class PracticalProject(models.Model):
    club = models.OneToOneField(Club, on_delete=models.CASCADE, related_name="practical")
    title = models.CharField(max_length=255)
    description = models.TextField()
    steps = models.JSONField(help_text=_("Ordered list of step strings"))
    guide_url = models.URLField(blank=True, null=True, help_text=_("Download link for project guide"))

    class Meta:
        verbose_name = _("Practical Project")
        verbose_name_plural = _("Practical Projects")

    def __str__(self):
        return f"{self.title} (Club: {self.club.name})"


class DiscussionMessage(models.Model):
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="discussion")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="discussion_messages"
    )
    comment = models.TextField()
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = _("Discussion Message")
        verbose_name_plural = _("Discussion Messages")
        ordering = ["-time"]

    def __str__(self):
        return f"{self.user.username}: {self.comment[:30]}..."


class Question(models.Model):
    assessment = models.ForeignKey(
        "Assessment", on_delete=models.CASCADE, related_name="questions"
    )
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")
        ordering = ["order"]

    def __str__(self):
        return f"{self.text[:30]}... ({self.assessment.title})"


class Choice(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="choices"
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Choice")
        verbose_name_plural = _("Choices")

    def __str__(self):
        return f"{self.text} (Correct: {self.is_correct})"
