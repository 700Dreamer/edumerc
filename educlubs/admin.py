from django.contrib import admin
from .models import Club, Topic, Lesson, RoleModel, PracticalApplication, ClubDiscussion, AskAIQuery

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'level', 'created_at']
    list_filter = ['category', 'level']
    search_fields = ['name', 'description']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'club', 'order']
    list_filter = ['club']
    inlines = [LessonInline]

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'content_type', 'order']
    list_filter = ['topic__club', 'content_type']

@admin.register(RoleModel)
class RoleModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'club']

@admin.register(PracticalApplication)
class PracticalApplicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'club']

@admin.register(ClubDiscussion)
class ClubDiscussionAdmin(admin.ModelAdmin):
    list_display = ['user_name', 'club', 'created_at']
    list_filter = ['club']

@admin.register(AskAIQuery)
class AskAIQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'club', 'created_at']
