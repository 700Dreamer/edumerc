from rest_framework import serializers
from .models import Club, Topic, Lesson, RoleModel, PracticalApplication, ClubDiscussion, AskAIQuery, ClubCategory

class ClubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubCategory
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

class RoleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleModel
        fields = '__all__'

class PracticalApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticalApplication
        fields = '__all__'

class ClubDiscussionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClubDiscussion
        fields = '__all__'

class AskAIQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = AskAIQuery
        fields = ['id', 'user_name', 'club', 'query', 'response', 'created_at']

class ClubSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    
    class Meta:
        model = Club
        fields = ["id", "name", "category", "category_name", "level", "description", "cover_image"]