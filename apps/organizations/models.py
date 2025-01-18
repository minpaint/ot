from django.db import models
from treebeard.mp_tree import MP_Node


class Organization(MP_Node):
    """
    Модель организации с поддержкой древовидной структуры
    """
    full_name = models.CharField(
        'Полное наименование',
        max_length=500
    )

    short_name = models.CharField(
        'Краткое наименование',
        max_length=250
    )

    name_by = models.CharField(
        'Наименование на белорусском',
        max_length=500,
        blank=True
    )

    details_ru = models.TextField(
        'Дополнительная информация',
        blank=True
    )

    details_by = models.TextField(
        'Дополнительная информация на белорусском',
        blank=True
    )

    node_order_by = ['short_name']  # определяет порядок узлов в дереве

    class Meta:
        verbose_name = 'Организация'
        verbose_name_plural = 'Организации'

    def __str__(self):
        return self.short_name