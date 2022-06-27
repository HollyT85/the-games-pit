from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import OrderLineItem


@receiver(post_save, sender=OrderLineItem)
def update_total(sender, instance, created, **kwargs):
    """
    update total when orderlineitem is created or updated
    """
    instance.order.update_total()


@receiver(post_delete, sender=OrderLineItem)
def update_total_delete(sender, instance, **kwargs):
    """
    update total when orderlineitem is deleted
    """
    instance.order.update_total()
