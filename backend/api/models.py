from django.db import models
from users.models import User
from django.contrib.postgres.fields import ArrayField


class ModelSet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="incomes")
    name = models.CharField(max_length=100, null=False, blank=False, default="Набор моделей")
    description = models.CharField(max_length=1000, null=True, blank=False, default="Описание набора моделей")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name


class UnitModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="single_combination")
    model_set = models.ForeignKey(ModelSet, on_delete=models.CASCADE, related_name="single_combination")
    users = models.IntegerField(blank=False, null=False, default=0)
    customers = models.IntegerField(blank=False, null=False, default=0)
    AVP = models.IntegerField(blank=False, null=False, default=0)
    APC = models.IntegerField(blank=False, null=False, default=0)
    TMS = models.IntegerField(blank=False, null=False, default=0)
    COGS = models.IntegerField(blank=False, null=False, default=0)
    COGS1s = models.IntegerField(blank=False, null=False, default=0)
    FC = models.IntegerField(blank=False, null=False, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'модель юнит-экономики'
        verbose_name_plural = 'модели юнит-экономики'
