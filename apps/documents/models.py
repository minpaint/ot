
from django.db import models

class Document(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название документа')
    file = models.FileField(upload_to='documents/', verbose_name='Файл документа')

    def __str__(self):
        return self.name

    class Meta:
         verbose_name = "Документ"
         verbose_name_plural = "Документы"
