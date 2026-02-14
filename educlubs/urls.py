from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClubViewSet, TopicViewSet, LessonViewSet, RoleModelViewSet, 
    PracticalApplicationViewSet, ClubDiscussionViewSet, AskAIQueryViewSet
)

router = DefaultRouter()
router.register(r'clubs', ClubViewSet)
router.register(r'topics', TopicViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'role-models', RoleModelViewSet)
router.register(r'practical-apps', PracticalApplicationViewSet)
router.register(r'discussions', ClubDiscussionViewSet)
router.register(r'ai-queries', AskAIQueryViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
