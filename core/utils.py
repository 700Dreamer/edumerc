"""
core/utils.py

Reusable helpers for auto-deleting GCS (or local) media files when a model
record is deleted or its file field is replaced with a new upload.

Usage — inside any app's apps.py ready() method:

    from core.utils import register_file_cleanup
    from django.db.models.signals import post_delete, pre_save

    def ready(self):
        from myapp.models import MyModel
        register_file_cleanup(MyModel, ['image', 'file'])
"""

import logging
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

logger = logging.getLogger(__name__)


def _delete_file(file_field):
    """Delete the underlying storage file if it exists."""
    if not file_field or not file_field.name:
        return
    storage = file_field.storage
    try:
        if storage.exists(file_field.name):
            storage.delete(file_field.name)
            logger.debug("Deleted media file: %s", file_field.name)
    except Exception as exc:
        # Never crash the app because a cleanup failed
        logger.warning("Could not delete media file %s: %s", file_field.name, exc)


def register_file_cleanup(model, field_names):
    """
    Register post_delete and pre_save signals on *model* so that old files
    stored in *field_names* are automatically removed from storage.

    Args:
        model:       A Django model class.
        field_names: List of FileField / ImageField attribute names on that model.
    """

    dispatch_uid_delete = f"file_cleanup_delete_{model.__name__}"
    dispatch_uid_update = f"file_cleanup_update_{model.__name__}"

    # ------------------------------------------------------------------ #
    # 1. Delete all file fields when the record itself is deleted          #
    # ------------------------------------------------------------------ #
    def on_delete(sender, instance, **kwargs):
        for fname in field_names:
            _delete_file(getattr(instance, fname, None))

    post_delete.connect(on_delete, sender=model, dispatch_uid=dispatch_uid_delete)

    # ------------------------------------------------------------------ #
    # 2. Delete the *old* file when it is replaced by a new upload        #
    # ------------------------------------------------------------------ #
    def on_update(sender, instance, **kwargs):
        if not instance.pk:
            return  # brand-new object, nothing to clean up
        try:
            old = sender.objects.get(pk=instance.pk)
        except sender.DoesNotExist:
            return
        for fname in field_names:
            old_file = getattr(old, fname, None)
            new_file = getattr(instance, fname, None)
            old_name = old_file.name if old_file else None
            new_name = new_file.name if new_file else None
            # Only delete if it has actually changed to a different file
            if old_name and old_name != new_name:
                _delete_file(old_file)

    pre_save.connect(on_update, sender=model, dispatch_uid=dispatch_uid_update)
