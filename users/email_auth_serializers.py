from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.settings import api_settings

User = get_user_model()

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Serializer that allows authentication using email instead of username.

    Accepts 'email' and 'password' in the request.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove the username field and add the email field
        username_field = get_user_model().USERNAME_FIELD
        self.fields.pop(username_field, None)
        self.fields['email'] = serializers.EmailField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if not email or not password:
            raise serializers.ValidationError(
                {'detail': 'Both email and password are required'}
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                {'detail': 'No active account found with the given credentials'}
            )

        self.user = authenticate(username=user.username, password=password)

        if not self.user or not self.user.is_active:
            raise serializers.ValidationError(
                {'detail': 'No active account found with the given credentials'}
            )

        data = {}
        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
