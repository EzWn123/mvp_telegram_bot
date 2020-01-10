from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import send_message
from . import models


@receiver(pre_save, sender=models.Message)
def message_sender(sender, instance, *args, **kwargs):
    if not instance.id and not instance.from_user:
        send_message(instance.user.messenger_id, instance.text)
