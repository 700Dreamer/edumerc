from django.contrib import admin
from .models import (
    MainCategory, SubjectLevel, SubjectClub, Topic, Lesson,
    SocialGroup, SocialClub, ClubDiscussion,
    TeacherCategory, TeacherClub, RoleModel, PracticalApplication, AskAIQuery
)

# --- INLINE HELPERS ---

class LessonInline(admin.TabularInline):
    model = Lesson
    extra = 1

# --- SUBJECT INLINES ---

class TopicSubjectInline(admin.StackedInline):
    model = Topic
    extra = 0
    fk_name = 'subject_club'
    inlines = [LessonInline]

class RoleModelSubjectInline(admin.TabularInline):
    model = RoleModel
    extra = 0
    fk_name = 'subject_club'

class PracticalAppSubjectInline(admin.TabularInline):
    model = PracticalApplication
    extra = 0
    fk_name = 'subject_club'

class DiscussionSubjectInline(admin.TabularInline):
    model = ClubDiscussion
    extra = 0
    fk_name = 'subject_club'

# --- SOCIAL INLINES ---

class TopicSocialInline(admin.StackedInline):
    model = Topic
    extra = 0
    fk_name = 'social_club'
    inlines = [LessonInline]

class RoleModelSocialInline(admin.TabularInline):
    model = RoleModel
    extra = 0
    fk_name = 'social_club'

class PracticalAppSocialInline(admin.TabularInline):
    model = PracticalApplication
    extra = 0
    fk_name = 'social_club'

class DiscussionSocialInline(admin.TabularInline):
    model = ClubDiscussion
    extra = 0
    fk_name = 'social_club'

# --- TEACHER INLINES ---

class TopicTeacherInline(admin.StackedInline):
    model = Topic
    extra = 0
    fk_name = 'teacher_club'
    inlines = [LessonInline]

class RoleModelTeacherInline(admin.TabularInline):
    model = RoleModel
    extra = 0
    fk_name = 'teacher_club'

class DiscussionTeacherInline(admin.TabularInline):
    model = ClubDiscussion
    extra = 0
    fk_name = 'teacher_club'

# --- ADMIN REGISTRATIONS ---

@admin.register(SubjectLevel)
class SubjectLevelAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']

@admin.register(SubjectClub)
class SubjectClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'icon']
    inlines = [TopicSubjectInline, RoleModelSubjectInline, PracticalAppSubjectInline, DiscussionSubjectInline]

@admin.register(SocialGroup)
class SocialGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon']

@admin.register(SocialClub)
class SocialClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'group', 'facilitator', 'icon']
    inlines = [TopicSocialInline, RoleModelSocialInline, PracticalAppSocialInline, DiscussionSocialInline]

@admin.register(TeacherCategory)
class TeacherCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_administrative']

@admin.register(TeacherClub)
class TeacherClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'icon']
    inlines = [TopicTeacherInline, RoleModelTeacherInline, DiscussionTeacherInline]

@admin.register(MainCategory)
class MainCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']

admin.site.register(Topic)
admin.site.register(Lesson)
admin.site.register(RoleModel)
admin.site.register(PracticalApplication)
admin.site.register(ClubDiscussion)
admin.site.register(AskAIQuery)
