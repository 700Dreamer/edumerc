from django.apps import AppConfig

class EdufundmeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'edufundme'

    def ready(self):
        from core.utils import register_file_cleanup
        from edufundme.models import Application
        register_file_cleanup(Application, ['attachments'])
