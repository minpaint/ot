from django.db import models
from apps.organizations.models import Organization

class Document(models.Model):
    """
    Модель документа
    """
    DOCUMENT_TYPES = [
        ('policy', 'Политика'),
        ('procedure', 'Процедура'),
        ('instruction', 'Инструкция'),
        ('regulation', 'Положение'),
        ('order', 'Приказ'),
        ('other', 'Прочее'),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='Организация'
    )

    type = models.CharField(
        'Тип документа',
        max_length=20,
        choices=DOCUMENT_TYPES,
        default='other'
    )

    number = models.CharField(
        'Номер документа',
        max_length=50,
        blank=True
    )

    name = models.CharField(
        'Наименование',
        max_length=500
    )

    file = models.FileField(
        'Файл документа',
        upload_to='documents/%Y/%m/',
        blank=True
    )

    description = models.TextField(
        'Описание',
        blank=True
    )

    is_active = models.BooleanField(
        'Действующий',
        default=True
    )

    created = models.DateTimeField(
        'Создан',
        auto_now_add=True
    )

    updated = models.DateTimeField(
        'Обновлен',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['-created']
        unique_together = ['organization', 'type', 'number']

    def __str__(self):
        if self.number:
            return f"{self.get_type_display()} №{self.number} - {self.name}"
        return self.name