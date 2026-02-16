from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    MainCategoryViewSet, SubCategoryViewSet, ClubViewSet,
    TopicViewSet, LessonViewSet, ClubDiscussionViewSet
)

router = DefaultRouter()
router.register(r'main-categories', MainCategoryViewSet, basename='main-category')
router.register(r'sub-categories', SubCategoryViewSet, basename='sub-category')
router.register(r'clubs', ClubViewSet, basename='club')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'discussions', ClubDiscussionViewSet, basename='discussion')

urlpatterns = [
    path('', include(router.urls)),
]
