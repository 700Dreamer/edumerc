from rest_framework import serializers
from .models import (
    MainCategory, SubjectLevel, SubjectClub, Topic, Lesson,
    SocialGroup, SocialClub, ClubDiscussion,
    TeacherCategory, TeacherClub, RoleModel, PracticalApplication, AskAIQuery
)

class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'

# --- SUBJECT SERIALIZERS ---

class SubjectLevelSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='subject', read_only=True)
    class Meta:
        model = SubjectLevel
        fields = '__all__'

class SubjectClubSerializer(serializers.ModelSerializer):
    level_name = serializers.ReadOnlyField(source='level.name')
    class Meta:
        model = SubjectClub
        fields = '__all__'

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class TopicSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    class Meta:
        model = Topic
        fields = '__all__'

# --- SOCIAL SERIALIZERS ---

class SocialGroupSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='social', read_only=True)
    class Meta:
        model = SocialGroup
        fields = '__all__'

class SocialClubSerializer(serializers.ModelSerializer):
    group_name = serializers.ReadOnlyField(source='group.name')
    class Meta:
        model = SocialClub
        fields = '__all__'

class ClubDiscussionSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = ClubDiscussion
        fields = '__all__'

# --- TEACHER SERIALIZERS ---

class TeacherCategorySerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='teacher', read_only=True)
    class Meta:
        model = TeacherCategory
        fields = '__all__'

class TeacherClubSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    class Meta:
        model = TeacherClub
        fields = '__all__'

# --- COMMON SERIALIZERS ---

class RoleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleModel
        fields = '__all__'

class PracticalApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticalApplication
        fields = '__all__'

class AskAIQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AskAIQuery
        fields = '__all__'
