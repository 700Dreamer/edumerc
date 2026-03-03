from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Section, Level, Subject, Topic, Subtopic, Lesson, Assessment
from .serializers import (
    SectionSerializer, LevelSerializer, SubjectSerializer, 
    TopicSerializer, SubtopicSerializer, LessonSerializer, AssessmentSerializer,
    SubjectDetailSerializer, TopicDetailSerializer, SubtopicDetailSerializer, 
    LessonDetailSerializer
)

class SectionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.AllowAny]

class LevelViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['section']
    ordering_fields = ['order', 'name']

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['level', 'level__section']
    ordering_fields = ['order', 'name']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubjectDetailSerializer
        return super().get_serializer_class()

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['subject']
    ordering_fields = ['order', 'title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TopicDetailSerializer
        return super().get_serializer_class()

class SubtopicViewSet(viewsets.ModelViewSet):
    queryset = Subtopic.objects.all()
    serializer_class = SubtopicSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['topic']
    ordering_fields = ['order', 'title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SubtopicDetailSerializer
        return super().get_serializer_class()

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['subtopic', 'is_published']
    ordering_fields = ['order', 'title']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LessonDetailSerializer
        return super().get_serializer_class()

class AssessmentViewSet(viewsets.ModelViewSet):
    queryset = Assessment.objects.all()
    serializer_class = AssessmentSerializer
    permission_classes = [permissions.DjangoModelPermissionsOrAnonReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['lesson']
    ordering_fields = ['order', 'title']
