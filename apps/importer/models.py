from django.db import models
from django.contrib.contenttypes.models import ContentType

class ImportSession(models.Model):
    """
    Модель импорта данных
    """
    IMPORT_STATUS = (
        ('pending', 'В ожидании'),
        ('processing', 'Обработка'),
        ('completed', 'Завершено'),
        ('failed', 'Ошибка'),
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name='Тип содержимого'
    )

    file = models.FileField(
        'Excel файл',
        upload_to='imports/%Y/%m/'
    )

    status = models.CharField(
        'Статус',
        max_length=20,
        choices=IMPORT_STATUS,
        default='pending'
    )

    errors = models.JSONField(
        'Ошибки',
        default=dict,
        blank=True
    )

    created = models.DateTimeField(
        'Создано',
        auto_now_add=True
    )

    updated = models.DateTimeField(
        'Обновлено',
        auto_now=True
    )

    processed_rows = models.IntegerField(
        'Обработано строк',
        default=0
    )

    total_rows = models.IntegerField(
        'Всего строк',
        default=0
    )

    class Meta:
        verbose_name = 'Сессия импорта'
        verbose_name_plural = 'Сессии импорта'
        ordering = ['-created']

    def __str__(self):
        return f"Импорт {self.content_type} от {self.created.strftime('%d.%m.%Y %H:%M')}"