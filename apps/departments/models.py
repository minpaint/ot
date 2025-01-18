from django.db import models
from treebeard.mp_tree import MP_Node
from apps.organizations.models import Organization


class Department(MP_Node):
    """
    Модель подразделения с поддержкой древовидной структуры
    """
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='Организация'
    )

    name = models.CharField(
        'Наименование',
        max_length=500
    )

    short_name = models.CharField(
        'Краткое наименование',
        max_length=250
    )

    node_order_by = ['name']

    class Meta:
        verbose_name = 'Подразделение'
        verbose_name_plural = 'Подразделения'

    def __str__(self):
        return f"{self.short_name} ({self.organization.short_name})"