from django.db import models
from apps.organizations.models import Organization


class Department(models.Model):
    """Модель подразделения"""

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='Организация'
    )

    name = models.CharField(
        'Наименование',
        max_length=250
    )

    created = models.DateTimeField(
        'Создано',
        auto_now_add=True
    )

    updated = models.DateTimeField(
        'Изменено',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'
        ordering = ['name']
        unique_together = ['organization', 'name']

    def __str__(self):
        return self.name