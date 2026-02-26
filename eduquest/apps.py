from django.apps import AppConfig


class EduquestConfig(AppConfig):
    name = 'eduquest'

    def ready(self):
        try:
            import eduquest.signals
        except ImportError:
            pass
        from core.utils import register_file_cleanup
        from eduquest.models import Material
        register_file_cleanup(Material, ['file'])
