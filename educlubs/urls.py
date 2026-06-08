from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    SectionViewSet, LevelViewSet, SubjectViewSet,
    TopicViewSet, SubtopicViewSet, LessonViewSet, AssessmentViewSet,
    ClubListAPIView, MainCategoriesView, SubCategoriesView, AIAssistView,
    DiscussionMessageViewSet
)

router = DefaultRouter()
router.register(r'sections', SectionViewSet, basename='section')
router.register(r'levels', LevelViewSet, basename='level')
router.register(r'subjects', SubjectViewSet, basename='subject')
router.register(r'topics', TopicViewSet, basename='topic')
router.register(r'subtopics', SubtopicViewSet, basename='subtopic')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'assessments', AssessmentViewSet, basename='assessment')
router.register(r'clubs', ClubListAPIView, basename='clubs')
router.register(r'discussions', DiscussionMessageViewSet, basename='discussions')

urlpatterns = [
    path('main-categories/', MainCategoriesView.as_view(), name='main-categories'),
    path('sub-categories/', SubCategoriesView.as_view(), name='sub-categories'),
    path('ai/assist/', AIAssistView.as_view(), name='ai-assist'),
    path('', include(router.urls)),
]
