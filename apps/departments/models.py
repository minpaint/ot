from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Department(MPTTModel):
    organization = models.ForeignKey(
        'organizations.Organization',
        on_delete=models.CASCADE,
        verbose_name='Организация'
    )
    name = models.CharField('Наименование', max_length=255)
    short_name = models.CharField('Сокращенное наименование', max_length=50, default='') # Добавляем default
    parent = TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='Родительское подразделение'
    )
    is_active = models.BooleanField('Действующее', default=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = 'Структурное подразделение'
        verbose_name_plural = 'Структурные подразделения'

    def __str__(self):
        return f"{self.name} ({self.organization.short_name})"