from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClubViewSet, TopicViewSet, LessonViewSet, RoleModelViewSet, 
    PracticalApplicationViewSet, ClubDiscussionViewSet, AskAIQueryViewSet,
    MainCategoryViewSet, SubCategoryViewSet
)

router = DefaultRouter()
router.register(r'main-categories', MainCategoryViewSet, basename='main-category')
router.register(r'sub-categories', SubCategoryViewSet, basename='sub-category')
router.register(r'clubs', ClubViewSet, basename='educlub')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'role-models', RoleModelViewSet, basename='role-model')
router.register(r'practical-apps', PracticalApplicationViewSet, basename='practical-app')
router.register(r'discussions', ClubDiscussionViewSet, basename='discussion')
router.register(r'ai/assist', AskAIQueryViewSet, basename='ai-assist')

urlpatterns = [
    path('', include(router.urls)),
]
