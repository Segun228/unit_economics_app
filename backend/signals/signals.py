from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache

from api.models import ModelSet, UnitModel, User


@receiver([post_save, post_delete], sender=ModelSet)
def clear_set_related_cache(sender, instance, **kwargs):
    user = instance.user
    set_id = instance.id
    user_id = user.id


    cache.delete(f"set_{set_id}_text_report_user_{user_id}")
    cache.delete(f"set_{set_id}_exel_report_user_{user_id}")
    cache.delete(f"set_{set_id}_image_report_user_{user_id}")
    cache.delete(f"set_{set_id}_cohort_report_user_{user_id}")


    cache.delete(f"set_list_user_{user_id}")
    cache.delete(f"db_report_user_{user_id}")


@receiver([post_save, post_delete], sender=UnitModel)
def clear_unit_related_cache(sender, instance, **kwargs):
    model_set = instance.model_set
    set_id = model_set.id
    user = model_set.user
    user_id = user.id
    unit_id = instance.id


    cache.delete(f"model_{unit_id}_text_report_user_{user_id}")
    cache.delete(f"model_{unit_id}_exel_report_user_{user_id}")
    cache.delete(f"model_{unit_id}_bep_report_user_{user_id}")
    cache.delete(f"model_{unit_id}_cohort_report_user_{user_id}")


    cache.delete(f"model_list_{set_id}_user_{user_id}")
    cache.delete(f"set_list_user_{user_id}")
    cache.delete(f"db_report_user_{user_id}")


@receiver([post_save, post_delete], sender=User)
def clear_user_cache(sender, instance, **kwargs):
    cache.delete("users")