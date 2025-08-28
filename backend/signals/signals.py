from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from api.models import ModelSet, UnitModel


@receiver(post_save, sender=Unit)
def clear_set_cache(sender, instance, created, **kwargs):
    if created:
        model_set = instance.model_set
        for user in model_set.users.all():
            cache_key = f"set_list_user_{user.id}"
            cache.delete(cache_key)