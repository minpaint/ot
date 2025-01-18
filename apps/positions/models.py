from django.db import models
from apps.organizations.models import Organization
from apps.departments.models import Department
from apps.documents.models import Document

class Position(models.Model):
    """
    Модель должности
    """
    ELECTRICAL_SAFETY_GROUPS = [
        (0, 'Не требуется'),
        (2, 'II группа'),
        (3, 'III группа'),
        (4, 'IV группа'),
        (5, 'V группа'),
    ]

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        verbose_name='Организация'
    )

    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        verbose_name='Подразделение'
    )

    name = models.CharField(
        'Наименование должности',
        max_length=250
    )

    division = models.CharField(
        'Участок/отдел',
        max_length=250,
        blank=True
    )

    safety_instructions = models.CharField(
        'Инструкции по охране труда',
        max_length=250,
        blank=True,
        help_text='Номера инструкций через запятую'
    )

    electrical_safety_group = models.IntegerField(
        'Группа по электробезопасности',
        choices=ELECTRICAL_SAFETY_GROUPS,
        default=0
    )

    internship_period = models.PositiveIntegerField(
        'Срок стажировки (смен)',
        default=0,
        help_text='0 - стажировка не требуется'
    )

    is_safety_responsible = models.BooleanField(
        'Ответственный по ОТ',
        default=False
    )

    is_electrical_personnel = models.BooleanField(
        'Электротехнический персонал',
        default=False
    )

    contract_instructions = models.TextField(
        'Должностные обязанности',
        blank=True
    )

    familiarization_documents = models.ManyToManyField(
        Document,
        verbose_name='Документы для ознакомления',
        blank=True
    )

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['organization', 'department', 'name']
        unique_together = ['organization', 'department', 'name', 'division']

    def __str__(self):
        if self.division:
            return f"{self.name} ({self.division})"
        return self.name