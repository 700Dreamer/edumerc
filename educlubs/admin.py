from django.contrib import admin
from .models import Section, Level, Subject, Topic, Subtopic, Lesson, Assessment
from .club_models import Club, Note, RoleModel, PracticalProject, DiscussionMessage, ClubSubscription

@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'section', 'order')
    list_filter = ('section',)
    search_fields = ('name',)
    ordering = ('section', 'order')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'order')
    list_filter = ('level__section', 'level')
    search_fields = ('name',)
    ordering = ('level', 'order')

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'subject', 'order')
    list_filter = ('subject__level__section', 'subject__level', 'subject')
    search_fields = ('title', 'description')
    ordering = ('subject', 'order')

@admin.register(Subtopic)
class SubtopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'topic', 'order')
    list_filter = ('topic__subject__level', 'topic__subject', 'topic')
    search_fields = ('title', 'description')
    ordering = ('topic', 'order')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'subtopic', 'order', 'is_published')
    list_filter = ('is_published', 'subtopic__topic__subject')
    search_fields = ('title', 'content', 'objectives')
    ordering = ('subtopic', 'order')

@admin.register(Assessment)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'lesson', 'order')
    list_filter = ('lesson__subtopic__topic__subject',)
    search_fields = ('title', 'description')
    ordering = ('lesson', 'order')

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'type', 'popular')
    list_filter = ('type', 'popular', 'level__section')
    search_fields = ('name', 'description')
    ordering = ('name',)
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('header', 'club', 'created_at')
    list_filter = ('club',)
    search_fields = ('header', 'content')
    ordering = ('-created_at',)
@admin.register(RoleModel)
class RoleModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'club')
    search_fields = ('name', 'contribution')
    ordering = ('name',)
@admin.register(PracticalProject)
class PracticalProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'club')
    search_fields = ('title', 'description')
    ordering = ('title',)
@admin.register(DiscussionMessage)
class DiscussionMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'club', 'time')
    list_filter = ('club',)
    search_fields = ('user', 'comment')
    ordering = ('-time',)


@admin.register(ClubSubscription)
class ClubSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "club", "status", "expires_at", "created_at")
    list_filter = ("status", "club")
    search_fields = ("user__username", "club__name")
    ordering = ("-created_at",)