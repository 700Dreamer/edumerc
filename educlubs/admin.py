from django.contrib import admin
from .models import (
    MainCategory, SubjectLevel, SubjectClub, Topic, Lesson,
    SocialGroup, SocialClub, ClubDiscussion,
    TeacherCategory, TeacherClub, RoleModel, PracticalApplication, AskAIQuery
)

# --- SUBJECT ADMIN ---

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

class TopicInline(admin.StackedInline):
    model = Topic
    extra = 1

class SubjectClubInline(admin.TabularInline):
    model = SubjectClub
    extra = 1

@admin.register(SubjectLevel)
class SubjectLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']
    inlines = [SubjectClubInline]

@admin.register(SubjectClub)
class SubjectClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'level']
    inlines = [TopicInline]

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['title', 'club', 'order']
    inlines = [LessonInline]

# --- SOCIAL ADMIN ---

class SocialClubInline(admin.TabularInline):
    model = SocialClub
    extra = 1

class ClubDiscussionInline(admin.TabularInline):
    model = ClubDiscussion
    extra = 1

@admin.register(SocialGroup)
class SocialGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']
    inlines = [SocialClubInline]

@admin.register(SocialClub)
class SocialClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'facilitator']
    inlines = [ClubDiscussionInline]

# --- TEACHER ADMIN ---

class TeacherClubInline(admin.TabularInline):
    model = TeacherClub
    extra = 1

@admin.register(TeacherCategory)
class TeacherCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_administrative']
    inlines = [TeacherClubInline]

@admin.register(TeacherClub)
class TeacherClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']

# --- MAIN & COMMON ---

class SubjectLevelInline(admin.TabularInline):
    model = SubjectLevel
    extra = 0

class SocialGroupInline(admin.TabularInline):
    model = SocialGroup
    extra = 0

class TeacherCategoryInline(admin.TabularInline):
    model = TeacherCategory
    extra = 0

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    inlines = [SubjectLevelInline, SocialGroupInline, TeacherCategoryInline]

admin.site.register(RoleModel)
admin.site.register(PracticalApplication)
admin.site.register(AskAIQuery)
admin.site.register(Lesson)
