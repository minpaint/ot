
from django.db import models
from apps.organizations.models import Organization
from apps.positions.models import Profession

class Employee(models.Model):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name="Организация")
    full_name = models.CharField(max_length=255, verbose_name="ФИО")
    full_name_dative = models.CharField(max_length=255, verbose_name="ФИО в дательном падеже")
    birth_date = models.DateField(verbose_name="Дата рождения")
    profession = models.ForeignKey(Profession, on_delete=models.CASCADE, verbose_name="Профессия (Должность)")
    is_contract_work = models.BooleanField(default=False, verbose_name="Договор подряда")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Email")

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
