from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from .views import RegisterView, ProfileMeView, ProfileUpdateView, GoogleLoginView
from .email_auth_views import EmailTokenObtainPairView

urlpatterns = [
    path('login/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('google/', GoogleLoginView.as_view(), name='google_login'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/me/', ProfileMeView.as_view(), name='profile_me'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
]
