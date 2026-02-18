from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoachViewSet, SessionViewSet, VirtualClassViewSet, PromoteCoachView

router = DefaultRouter()
router.register(r'tutors', CoachViewSet, basename='coach')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'classes', VirtualClassViewSet, basename='virtual-class')

urlpatterns = [
    path('', include(router.urls)),
    path('promote/', PromoteCoachView.as_view(), name='promote-coach'),
]
