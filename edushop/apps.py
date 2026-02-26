from django.apps import AppConfig


class EdushopConfig(AppConfig):
    name = 'edushop'

    def ready(self):
        from core.utils import register_file_cleanup
        from edushop.models import Category, Product, Bundle
        register_file_cleanup(Category, ['image'])
        register_file_cleanup(Product,  ['image', 'file'])
        register_file_cleanup(Bundle,   ['image'])
