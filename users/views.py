from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
import secrets
import string
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from .serializers import RegisterSerializer, UserSerializer, ProfileSerializer
from .models import Profile

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class ProfileMeView(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class ProfileUpdateView(generics.UpdateAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get_object(self):
        return self.request.user.profile

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class GoogleLoginView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        token = request.data.get('id_token')
        if not token:
            return Response({'error': 'id_token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if not settings.GOOGLE_OAUTH2_CLIENT_ID:
                return Response({'error': 'Backend Google configuration error: GOOGLE_OAUTH2_CLIENT_ID is not set.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                settings.GOOGLE_OAUTH2_CLIENT_ID
            )

            email = idinfo.get('email')
            if not email:
                return Response({'error': 'Token did not provide an email'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=email).first()
            if not user:
                base_username = email.split('@')[0]
                username = base_username
                counter = 1
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1

                alphabet = string.ascii_letters + string.digits
                password = ''.join(secrets.choice(alphabet) for i in range(20))
                
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=idinfo.get('given_name', ''),
                    last_name=idinfo.get('family_name', '')
                )
                
            refresh = RefreshToken.for_user(user)

            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response({'error': 'Invalid token: ' + str(e)}, status=status.HTTP_400_BAD_REQUEST)
