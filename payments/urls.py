from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, PesaPalIPNViewSet, WalletViewSet

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'ipn', PesaPalIPNViewSet, basename='pesapal-ipn')
router.register(r'wallet', WalletViewSet, basename='wallet')

urlpatterns = [
    path('', include(router.urls)),
]
