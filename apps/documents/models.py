from django.db import models
from apps.organizations.models import Organization


class Document(models.Model):
    """Модель документа"""
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='Организация'
    )

    name = models.CharField(
        'Наименование',
        max_length=250
    )

    number = models.CharField(
        'Номер документа',
        max_length=50,
        blank=True
    )

    date = models.DateField(
        'Дата документа',
        null=True,
        blank=True
    )

    file = models.FileField(
        'Файл',
        upload_to='documents/',
        null=True,
        blank=True
    )

    created = models.DateTimeField(
        'Создан',
        auto_now_add=True
    )

    updated = models.DateTimeField(
        'Изменен',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Документ'
        verbose_name_plural = 'Документы'
        ordering = ['-created']

    def __str__(self):
        if self.number:
            return f"{self.name} №{self.number}"
        return self.name