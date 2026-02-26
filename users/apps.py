from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'

    def ready(self):
        from core.utils import register_file_cleanup
        from users.models import Profile
        register_file_cleanup(Profile, ['avatar'])
