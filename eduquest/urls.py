from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MaterialViewSet, MaterialOrderViewSet

router = DefaultRouter()
router.register(r'orders', MaterialOrderViewSet, basename='material-order')
router.register(r'', MaterialViewSet, basename='material')

urlpatterns = [
    path('', include(router.urls)),
]
