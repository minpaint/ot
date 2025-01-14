
from django.db import models
from apps.organizations.models import Organization, Department

class Profession(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Организация")
    department = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name="Структурное подразделение")
    department_name = models.CharField(max_length=255, verbose_name="Наименование отдела")
    instruction_numbers = models.CharField(max_length=255, verbose_name="Номера инструкций по охране труда")
    el_group = models.CharField(max_length=5, verbose_name="Группа по электробезопасности")
    probation_period = models.IntegerField(verbose_name="Срок стажировки")
    contract_instruction = models.CharField(max_length=255, verbose_name="Инструкции по договору подряда")
    is_responsible = models.BooleanField(default=False, verbose_name="Ответственный за охрану труда")
    is_electrical_staff = models.BooleanField(default=False, verbose_name="Является ли электротехническим персоналом")

    def __str__(self):
         return f"{self.department_name} ({self.organization.short_name})"
    class Meta:
        verbose_name = "Профессия/Должность"
        verbose_name_plural = "Профессии/Должности"
