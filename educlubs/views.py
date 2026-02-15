from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Club, Topic, Lesson, RoleModel, PracticalApplication, ClubDiscussion, AskAIQuery, ClubCategory
from .serializers import (
    ClubSerializer, TopicSerializer, LessonSerializer, RoleModelSerializer, 
    PracticalApplicationSerializer, ClubDiscussionSerializer, AskAIQuerySerializer,
    ClubCategorySerializer
)

class ClubCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ClubCategory.objects.all()
    serializer_class = ClubCategorySerializer

class ClubViewSet(viewsets.ModelViewSet):
    queryset = Club.objects.all()
    serializer_class = ClubSerializer
    filterset_fields = ['category', 'level']

    @action(detail=True, methods=['get'])
    def curriculum(self, request, pk=None):
        club = self.get_object()
        topics = club.topics.all()
        serializer = TopicSerializer(topics, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def projects(self, request, pk=None):
        club = self.get_object()
        apps = club.practical_apps.all()
        serializer = PracticalApplicationSerializer(apps, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def role_models(self, request, pk=None):
        club = self.get_object()
        models = club.role_models.all()
        serializer = RoleModelSerializer(models, many=True)
        return Response(serializer.data)

class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class RoleModelViewSet(viewsets.ModelViewSet):
    queryset = RoleModel.objects.all()
    serializer_class = RoleModelSerializer

class PracticalApplicationViewSet(viewsets.ModelViewSet):
    queryset = PracticalApplication.objects.all()
    serializer_class = PracticalApplicationSerializer

class ClubDiscussionViewSet(viewsets.ModelViewSet):
    queryset = ClubDiscussion.objects.all()
    serializer_class = ClubDiscussionSerializer

class AskAIQueryViewSet(viewsets.ModelViewSet):
    queryset = AskAIQuery.objects.all()
    serializer_class = AskAIQuerySerializer
