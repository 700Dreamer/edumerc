from rest_framework import serializers
from .models import Section, Level, Subject, Topic, Subtopic, Lesson, Assessment, Question, Choice

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

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'text', 'is_correct']

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'choices', 'order']

class AssessmentSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Assessment
        fields = ['id', 'title', 'lesson', 'description', 'order', 'questions']

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

# ---------------------------------------------------------------------------
# Club‑related serializers
# ---------------------------------------------------------------------------

from .club_models import Club, Note, RoleModel, PracticalProject, DiscussionMessage, ClubSubscription

class ClubSerializer(serializers.ModelSerializer):
    level_name = serializers.ReadOnlyField(source='level.name')
    is_subscribed = serializers.SerializerMethodField()
    price = serializers.ReadOnlyField()

    class Meta:
        model = Club
        fields = ['id', 'name', 'icon', 'description', 'level', 'level_name', 'type', 'popular', 'price', 'is_subscribed', 'subscription_duration_days']

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user or request.user.is_anonymous:
            return False
        from django.utils import timezone
        from django.db.models import Q
        return request.user.is_superuser or obj.subscriptions.filter(
            user=request.user,
            status='active'
        ).filter(
            Q(expires_at__gt=timezone.now()) | Q(expires_at__isnull=True)
        ).exists()

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'header', 'content', 'created_at']

class RoleModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoleModel
        fields = ['id', 'name', 'contribution', 'image']

class PracticalProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = PracticalProject
        fields = ['id', 'title', 'description', 'steps', 'guide_url']

class DiscussionMessageSerializer(serializers.ModelSerializer):
    club = serializers.PrimaryKeyRelatedField(queryset=Club.objects.all(), required=False)
    message = serializers.CharField(source='comment', required=False)
    comment = serializers.CharField(required=False)
    user = serializers.SerializerMethodField()

    class Meta:
        model = DiscussionMessage
        fields = ['id', 'club', 'user', 'comment', 'message', 'time']

    def get_user(self, obj):
        return obj.user.username if obj.user else "Anonymous"

    def validate(self, attrs):
        if 'comment' not in attrs and 'message' in attrs:
            attrs['comment'] = attrs['message']
        return attrs

# Nested ClubDetailSerializer – re‑uses the existing curriculum serializers
class ClubDetailSerializer(serializers.ModelSerializer):
    level = LevelSerializer(read_only=True)
    notes = NoteSerializer(many=True, read_only=True)
    roleModels = RoleModelSerializer(many=True, read_only=True, source='role_models')
    practical = PracticalProjectSerializer(read_only=True)
    discussion = DiscussionMessageSerializer(many=True, read_only=True)
    curriculum = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()
    price = serializers.ReadOnlyField()

    class Meta:
        model = Club
        fields = [
            'id', 'name', 'icon', 'description', 'type', 'popular',
            'level', 'notes', 'roleModels', 'practical', 'discussion',
            'curriculum', 'price', 'is_subscribed', 'subscription_duration_days'
        ]

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if not request or not request.user or request.user.is_anonymous:
            return False
        from django.utils import timezone
        from django.db.models import Q
        return request.user.is_superuser or obj.subscriptions.filter(
            user=request.user,
            status='active'
        ).filter(
            Q(expires_at__gt=timezone.now()) | Q(expires_at__isnull=True)
        ).exists()


    def get_curriculum(self, obj):
        subject = obj.subject
        if not subject:
            subject = obj.level.subjects.filter(name__icontains=obj.name).first()
        if not subject:
            # Fallback to first subject if name doesn't match
            subject = obj.level.subjects.first()
        if not subject:
            return []

        data = []
        for topic in subject.topics.all().order_by('order'):
            lessons_data = []
            for subtopic in topic.subtopics.all().order_by('order'):
                for lesson in subtopic.lessons.all().order_by('order'):
                    # Retrieve assessments for this lesson
                    assessments_data = []
                    for assessment in lesson.assessments.all():
                        questions_data = []
                        for question in assessment.questions.all().order_by('order'):
                            choices_data = []
                            for choice in question.choices.all():
                                choices_data.append({
                                    'id': choice.id,
                                    'text': choice.text,
                                    'is_correct': choice.is_correct
                                })
                            questions_data.append({
                                'id': question.id,
                                'text': question.text,
                                'choices': choices_data
                              })
                        assessments_data.append({
                            'id': assessment.id,
                            'title': assessment.title,
                            'description': assessment.description,
                            'questions': questions_data
                        })
                    
                    lessons_data.append({
                        'title': lesson.title,
                        'type': 'Interactive Quiz' if lesson.assessments.exists() else ('Video Lesson' if lesson.video_url else 'Reading Material'),
                        'duration': f"{lesson.duration_minutes}m" if lesson.duration_minutes else "15m",
                        'content': lesson.content,
                        'assessments': assessments_data
                    })
            data.append({
                'title': topic.title,
                'lessons': lessons_data
            })
        return data

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        is_subscribed = ret.get('is_subscribed', False)
        if not is_subscribed:
            ret['notes'] = []
            ret['roleModels'] = []
            ret['practical'] = None
            ret['discussion'] = []
            
            if 'curriculum' in ret and isinstance(ret['curriculum'], list):
                preview_curriculum = []
                for topic in ret['curriculum']:
                    preview_lessons = []
                    for lesson in topic.get('lessons', []):
                        preview_lessons.append({
                            'title': lesson.get('title'),
                            'type': lesson.get('type'),
                            'duration': lesson.get('duration'),
                            'content': None,
                            'video_url': None,
                            'assessments': []
                        })
                    preview_curriculum.append({
                        'title': topic.get('title'),
                        'lessons': preview_lessons
                    })
                ret['curriculum'] = preview_curriculum
        return ret

