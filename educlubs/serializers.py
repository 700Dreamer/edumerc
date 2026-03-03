from rest_framework import serializers
from .models import Section, Level, Subject, Topic, Subtopic, Lesson, Assessment

class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = ['id', 'name', 'description']

class LevelSerializer(serializers.ModelSerializer):
    section_name = serializers.ReadOnlyField(source='section.name')

    class Meta:
        model = Level
        fields = ['id', 'name', 'section', 'section_name', 'order']

class SubjectSerializer(serializers.ModelSerializer):
    level_name = serializers.ReadOnlyField(source='level.name')

    class Meta:
        model = Subject
        fields = ['id', 'name', 'level', 'level_name', 'description', 'order']

class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'title', 'subject', 'description', 'order']

class SubtopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtopic
        fields = ['id', 'title', 'topic', 'description', 'order']

class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'subtopic', 'objectives', 'content', 
            'video_url', 'duration_minutes', 'order', 'is_published'
        ]

class AssessmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assessment
        fields = ['id', 'title', 'lesson', 'description', 'order']

# Nested Serializers for Breadcrumb/Detail views
class LessonDetailSerializer(serializers.ModelSerializer):
    assessments = AssessmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'subtopic', 'objectives', 'content', 
            'video_url', 'duration_minutes', 'order', 'is_published',
            'assessments'
        ]

class SubtopicDetailSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Subtopic
        fields = ['id', 'title', 'topic', 'description', 'order', 'lessons']

class TopicDetailSerializer(serializers.ModelSerializer):
    subtopics = SubtopicSerializer(many=True, read_only=True)

    class Meta:
        model = Topic
        fields = ['id', 'title', 'subject', 'description', 'order', 'subtopics']

class SubjectDetailSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)

    class Meta:
        model = Subject
        fields = ['id', 'name', 'level', 'description', 'order', 'topics']
