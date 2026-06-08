import graphene
from graphene_django import DjangoObjectType
from graphene.types.generic import GenericScalar
from django.contrib.auth import get_user_model
from .models import Section, Level, Subject, Topic, Subtopic, Lesson, Assessment, Question, Choice
from .club_models import Club, Note, RoleModel, PracticalProject, DiscussionMessage

User = get_user_model()

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ("id", "username", "email", "role")

class SectionType(DjangoObjectType):
    class Meta:
        model = Section
        fields = "__all__"

class LevelType(DjangoObjectType):
    class Meta:
        model = Level
        fields = "__all__"

class SubjectType(DjangoObjectType):
    class Meta:
        model = Subject
        fields = "__all__"

class TopicType(DjangoObjectType):
    class Meta:
        model = Topic
        fields = "__all__"

class SubtopicType(DjangoObjectType):
    class Meta:
        model = Subtopic
        fields = "__all__"

class LessonType(DjangoObjectType):
    class Meta:
        model = Lesson
        fields = "__all__"

class AssessmentType(DjangoObjectType):
    class Meta:
        model = Assessment
        fields = "__all__"

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = "__all__"

class ChoiceType(DjangoObjectType):
    class Meta:
        model = Choice
        fields = "__all__"

class NoteType(DjangoObjectType):
    class Meta:
        model = Note
        fields = "__all__"

class RoleModelType(DjangoObjectType):
    class Meta:
        model = RoleModel
        fields = "__all__"

class PracticalProjectType(DjangoObjectType):
    class Meta:
        model = PracticalProject
        fields = "__all__"

class DiscussionMessageType(DjangoObjectType):
    class Meta:
        model = DiscussionMessage
        fields = "__all__"

class ClubType(DjangoObjectType):
    curriculum = GenericScalar()
    role_models = graphene.List(RoleModelType)
    discussion = graphene.List(DiscussionMessageType)

    class Meta:
        model = Club
        fields = ("id", "name", "icon", "description", "level", "subject", "type", "popular", "notes", "practical")

    def resolve_curriculum(self, info):
        subject = self.subject
        if not subject:
            subject = self.level.subjects.filter(name__icontains=self.name).first()
        if not subject:
            subject = self.level.subjects.first()
        if not subject:
            return []

        data = []
        for topic in subject.topics.all().order_by('order'):
            lessons_data = []
            for subtopic in topic.subtopics.all().order_by('order'):
                for lesson in subtopic.lessons.all().order_by('order'):
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

    def resolve_role_models(self, info):
        return self.role_models.all()

    def resolve_discussion(self, info):
        return self.discussion.all().order_by("-time")

class Query(graphene.ObjectType):
    all_clubs = graphene.List(
        ClubType,
        subcategory_id=graphene.Int(),
        type=graphene.String()
    )
    club_detail = graphene.Field(
        ClubType,
        id=graphene.ID(required=True),
        type=graphene.String()
    )

    def resolve_all_clubs(self, info, subcategory_id=None, type=None):
        queryset = Club.objects.select_related('level').all()
        if subcategory_id:
            queryset = queryset.filter(level_id=subcategory_id)
        if type:
            queryset = queryset.filter(type=type)
        return queryset

    def resolve_club_detail(self, info, id, type=None):
        try:
            club = Club.objects.prefetch_related(
                'notes',
                'role_models',
                'practical',
                'discussion',
                'level__subjects__topics__subtopics__lessons__assessments'
            ).select_related('level').get(pk=id)
        except Club.DoesNotExist:
            return None
        return club

class PostDiscussionMessage(graphene.Mutation):
    class Arguments:
        club_id = graphene.ID(required=True)
        comment = graphene.String(required=True)

    success = graphene.Boolean()
    message = graphene.Field(DiscussionMessageType)

    def mutate(self, info, club_id, comment):
        user = info.context.user
        if not user or user.is_anonymous:
            # Replicate the REST fallback
            UserClass = get_user_model()
            user = UserClass.objects.filter(is_superuser=True).first() or UserClass.objects.first()

        try:
            club = Club.objects.get(pk=club_id)
        except Club.DoesNotExist:
            raise Exception("Club not found")

        msg = DiscussionMessage.objects.create(
            club=club,
            user=user,
            comment=comment
        )
        return PostDiscussionMessage(success=True, message=msg)

class Mutation(graphene.ObjectType):
    post_discussion_message = PostDiscussionMessage.Field()
