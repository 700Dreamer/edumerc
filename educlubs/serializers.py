from rest_framework import serializers
from .models import Club, Topic, Lesson, RoleModel, PracticalApplication, ClubDiscussion, AskAIQuery

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
        fields = '__all__'

class ClubSerializer(serializers.ModelSerializer):
    # topics = TopicSerializer(many=True, read_only=True)
    # role_models = RoleModelSerializer(many=True, read_only=True)
    # practical_apps = PracticalApplicationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Club
        fields = ["name","category","id","cover_image"]