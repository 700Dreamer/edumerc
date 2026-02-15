from rest_framework import serializers
from .models import Club, Topic, Lesson, RoleModel, PracticalApplication, ClubDiscussion, AskAIQuery, MainCategory, SubCategory

class MainCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MainCategory
        fields = '__all__'

class SubCategorySerializer(serializers.ModelSerializer):
    main_category_name = serializers.ReadOnlyField(source='main_category.name')
    
    class Meta:
        model = SubCategory
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
    subcategory_name = serializers.ReadOnlyField(source='subcategory.name')
    main_category_name = serializers.ReadOnlyField(source='subcategory.main_category.name')
    
    class Meta:
        model = Club
        fields = '__all__'

