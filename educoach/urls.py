from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CoachViewSet, SessionViewSet, VirtualClassViewSet, 
    PromoteCoachView, CoachAvailabilityView, SmartSlotView, HMSWebhookView
)

router = DefaultRouter()
router.register(r'tutors', CoachViewSet, basename='coach')
router.register(r'sessions', SessionViewSet, basename='session')
router.register(r'classes', VirtualClassViewSet, basename='virtual-class')

urlpatterns = [
    path('', include(router.urls)),
    path('promote/', PromoteCoachView.as_view(), name='promote-coach'),
    path('availability/', CoachAvailabilityView.as_view(), name='coach-availability'),
    path('tutors/<int:id>/slots/', SmartSlotView.as_view(), name='smart-slots'),
    
    path('appointments/', SessionViewSet.as_view({'get': 'my_appointments'}), name='coach-appointments'),
    path('appointments/<str:booking_id>/', SessionViewSet.as_view({'patch': 'update_status_by_booking_id'}), name='coach-appointments-update'),
    
    path('webhooks/100ms/', HMSWebhookView.as_view(), name='hms-webhook'),
]
