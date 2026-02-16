from rest_framework import serializers
from .models import (
    MainCategory, SubjectLevel, SubjectClub, Topic, Lesson,
    SocialGroup, SocialClub, ClubDiscussion,
    TeacherCategory, TeacherClub, RoleModel, PracticalApplication, AskAIQuery
)

# --- UTILITY SERIALIZERS (Internal/Admin) ---

class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'

# --- CONTRACT SERIALIZERS (CamelCase for Frontend) ---

class RoleModelContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleModel
        fields = ['name', 'contribution', 'image']

class PracticalApplicationContractSerializer(serializers.ModelSerializer):
    steps = serializers.SerializerMethodField()
    
    class Meta:
        model = PracticalApplication
        fields = ['title', 'description', 'steps']
    
    def get_steps(self, obj):
        # Splitting guide by newlines or bullet points to create list
        if not obj.guide:
            return []
        return [step.strip() for step in obj.guide.split('\n') if step.strip()]

class DiscussionContractSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    comment = serializers.ReadOnlyField(source='content')
    time = serializers.SerializerMethodField()

    class Meta:
        model = ClubDiscussion
        fields = ['user', 'comment', 'time']

    def get_time(self, obj):
        import datetime
        from django.utils import timezone
        diff = timezone.now() - obj.created_at
        if diff.days > 0:
            return f"{diff.days}d ago"
        hours = diff.seconds // 3600
        if hours > 0:
            return f"{hours}h ago"
        mins = (diff.seconds % 3600) // 60
        return f"{mins}m ago"

class AskAIQueryContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = AskAIQuery
        fields = ['query', 'response', 'created_at']

class LessonContractSerializer(serializers.ModelSerializer):
    type = serializers.ReadOnlyField(source='content_type') # Maps to 'Video Lesson' etc if needed
    duration = serializers.CharField(default="10m") # Placeholder as requested in contract
    
    class Meta:
        model = Lesson
        fields = ['title', 'type', 'duration']

class TopicContractSerializer(serializers.ModelSerializer):
    lessons = LessonContractSerializer(many=True, read_only=True)
    
    class Meta:
        model = Topic
        fields = ['title', 'lessons']

# --- UNIFIED DETAIL SERIALIZER ---

class UnifiedClubDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    level = serializers.SerializerMethodField()
    icon = serializers.CharField()
    description = serializers.CharField()
    type = serializers.SerializerMethodField()
    
    # Sections
    curriculum = serializers.SerializerMethodField()
    roleModels = serializers.SerializerMethodField()
    discussion = serializers.SerializerMethodField()
    practical = serializers.SerializerMethodField()

    def get_level(self, obj):
        if hasattr(obj, 'level'): # SubjectClub
            return obj.level.name
        if hasattr(obj, 'group'): # SocialClub
            # We don't have 'level' for social, but the group name serves as sub-cat
            return obj.group.name
        if hasattr(obj, 'category'): # TeacherClub
            return obj.category.name
        return "N/A"

    def get_type(self, obj):
        if hasattr(obj, 'level'): return 'subject'
        if hasattr(obj, 'group'): return 'social'
        if hasattr(obj, 'category'): return 'teacher'
        return 'unknown'

    def get_curriculum(self, obj):
        topics = obj.topics.all()
        return TopicContractSerializer(topics, many=True).data

    def get_roleModels(self, obj):
        models = obj.role_models.all()
        return RoleModelContractSerializer(models, many=True).data

    def get_discussion(self, obj):
        discussions = obj.discussions.all().order_by('-created_at')[:10]
        return DiscussionContractSerializer(discussions, many=True).data

    def get_practical(self, obj):
        first_app = obj.practical_apps.first()
        if first_app:
            return PracticalApplicationContractSerializer(first_app).data
        return None

# --- LEGACY/LIST SERIALIZERS ---

class SubjectLevelSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='subject', read_only=True)
    class Meta:
        model = SubjectLevel
        fields = '__all__'

class SubjectClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectClub
        fields = '__all__'

class SocialGroupSerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='social', read_only=True)
    class Meta:
        model = SocialGroup
        fields = '__all__'

class SocialClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialClub
        fields = '__all__'

class TeacherCategorySerializer(serializers.ModelSerializer):
    type = serializers.CharField(default='teacher', read_only=True)
    class Meta:
        model = TeacherCategory
        fields = '__all__'

class TeacherClubSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherClub
        fields = '__all__'

# Aliases for views.py compatibility
TopicSerializer = TopicContractSerializer
LessonSerializer = LessonContractSerializer
ClubDiscussionSerializer = DiscussionContractSerializer
RoleModelSerializer = RoleModelContractSerializer
PracticalApplicationSerializer = PracticalApplicationContractSerializer
AskAIQuerySerializer = AskAIQueryContractSerializer # Need to define this one too or alias it
