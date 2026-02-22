from django.apps import AppConfig


class EduquestConfig(AppConfig):
    name = 'eduquest'

    def ready(self):
        import eduquest.signals
