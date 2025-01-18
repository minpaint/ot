from django.db import models
from apps.organizations.models import Organization
from apps.departments.models import Department
from apps.positions.models import Position

class Employee(models.Model):
    """
    Модель сотрудника
    """
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
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

    position = models.ForeignKey(
        Position,
        on_delete=models.CASCADE,
        verbose_name='Должность'
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=100
    )

    first_name = models.CharField(
        'Имя',
        max_length=100
    )

    middle_name = models.CharField(
        'Отчество',
        max_length=100,
        blank=True
    )

    gender = models.CharField(
        'Пол',
        max_length=1,
        choices=GENDER_CHOICES
    )

    birth_date = models.DateField(
        'Дата рождения'
    )

    employment_date = models.DateField(
        'Дата приема на работу'
    )

    personnel_number = models.CharField(
        'Табельный номер',
        max_length=50,
        unique=True,
        blank=True,
        null=True
    )

    email = models.EmailField(
        'Email',
        blank=True
    )

    phone = models.CharField(
        'Телефон',
        max_length=20,
        blank=True
    )

    is_active = models.BooleanField(
        'Активен',
        default=True
    )

    notes = models.TextField(
        'Примечания',
        blank=True
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
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['last_name', 'first_name']
        unique_together = ['organization', 'personnel_number']

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_full_name(self):
        """
        Возвращает полное имя сотрудника
        """
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

    def get_short_name(self):
        """
        Возвращает сокращенное имя сотрудника (Фамилия И.О.)
        """
        first_initial = self.first_name[0] if self.first_name else ''
        middle_initial = f"{self.middle_name[0]}." if self.middle_name else ''
        return f"{self.last_name} {first_initial}.{middle_initial}"