from django.apps import AppConfig


class EdupediaConfig(AppConfig):
    name = 'edupedia'

    def ready(self):
        from core.utils import register_file_cleanup
        from edupedia.models import School, SchoolGalleryImage, SchoolEvent, SchoolAdministrator, PromotionalMaterial
        register_file_cleanup(School,               ['logo', 'coverImage', 'school_anthem'])
        register_file_cleanup(SchoolGalleryImage,    ['image'])
        register_file_cleanup(SchoolEvent,          ['image'])
        register_file_cleanup(SchoolAdministrator,  ['photo'])
        register_file_cleanup(PromotionalMaterial,  ['file'])
