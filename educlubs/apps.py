from django.apps import AppConfig


class EduclubsConfig(AppConfig):
    name = 'educlubs'

    def ready(self):
        from core.utils import register_file_cleanup
        from educlubs.models import SubjectClub, SocialClub, Lesson, RoleModel, PracticalApplication
        register_file_cleanup(SubjectClub,          ['cover_image'])
        register_file_cleanup(SocialClub,           ['cover_image'])
        register_file_cleanup(Lesson,               ['file_content'])
        register_file_cleanup(RoleModel,            ['image'])
        register_file_cleanup(PracticalApplication, ['image'])
