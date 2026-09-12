"""Broadcast item changes onto the realtime channel.

Imported from ``models.py`` so the receivers are registered as soon as the app
loads. Every create/update/delete fans out an :class:`ItemSignal` to the
``"items"`` group, which the GraphQL subscription streams to clients.
"""

import logging

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from demo import models
from demo.channels import ItemSignal, item_channel

logger = logging.getLogger(__name__)


@receiver(post_save, sender=models.Item)
def on_item_saved(sender, instance=None, created=None, **kwargs):
    """Broadcast a create/update signal when an item is saved."""
    if instance is None:
        return
    signal = ItemSignal(create=instance.id) if created else ItemSignal(update=instance.id)
    item_channel.broadcast(signal, ["items"])


@receiver(pre_delete, sender=models.Item)
def on_item_deleted(sender, instance=None, **kwargs):
    """Broadcast a delete signal just before an item is removed."""
    if instance is not None:
        item_channel.broadcast(ItemSignal(delete=instance.id), ["items"])
