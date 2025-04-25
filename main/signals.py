"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Task
from .utils import notify_bot


@receiver(post_save, sender=Task)
def check_task_overdue(sender, instance, created, **kwargs):
    if (
        not instance.complete and
        instance.deadline and
        instance.deadline < timezone.now() and
        not instance.is_notified
    ):
        notify_bot(instance)
        instance.is_notified = True
        instance.save(update_fields=['is_notified'])
"""