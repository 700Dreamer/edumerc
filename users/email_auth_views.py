from rest_framework_simplejwt.views import TokenObtainPairView
from .email_auth_serializers import EmailTokenObtainPairSerializer

class EmailTokenObtainPairView(TokenObtainPairView):
    """Token obtain view that supports email login.
    Accepts 'email' in the request payload. The serializer will map it to the user's username.
    """
    serializer_class = EmailTokenObtainPairSerializer
