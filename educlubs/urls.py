from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SectionViewSet, LevelViewSet, SubjectViewSet, 
    TopicViewSet, SubtopicViewSet, LessonViewSet, AssessmentViewSet
)

router = DefaultRouter()
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'subtopics', SubtopicViewSet, basename='subtopic')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'assessments', AssessmentViewSet, basename='assessment')

urlpatterns = [
    path('', include(router.urls)),
]
