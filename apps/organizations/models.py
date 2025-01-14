
from django.db import models

class Organization(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="Полное наименование организации")
    short_name = models.CharField(max_length=100, verbose_name="Сокращенное наименование организации")
    full_name_ru = models.CharField(max_length=255, verbose_name="Полное наименование организации (рус)")
    full_name_by = models.CharField(max_length=255, verbose_name="Полное наименование организации (бел)")
    requisites_ru = models.TextField(verbose_name="Реквизиты организации (рус)")
    requisites_by = models.TextField(verbose_name="Реквизиты организации (бел)")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

class Department(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name='departments', verbose_name="Организация")
    name = models.CharField(max_length=255, verbose_name="Наименование структурного подразделения")
    short_name = models.CharField(max_length=100, verbose_name="Сокращенное наименование")

    def __str__(self):
        return f"{self.name} ({self.organization.short_name})"

    class Meta:
        verbose_name = "Структурное подразделение"
        verbose_name_plural = "Структурные подразделения"
