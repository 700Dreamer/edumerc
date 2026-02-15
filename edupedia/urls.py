from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SchoolViewSet, SchoolEventViewSet

router = DefaultRouter()
router.register(r'', SchoolViewSet, basename='school')
router.register(r'events', SchoolEventViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
