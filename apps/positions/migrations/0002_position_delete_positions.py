# Generated by Django 4.2.18 on 2025-01-18 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0002_organization_delete_organizations"),
        ("documents", "0002_document_delete_documents"),
        ("departments", "0002_department_delete_departments"),
        ("positions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Position",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=250, verbose_name="Наименование должности"
                    ),
                ),
                (
                    "division",
                    models.CharField(
                        blank=True, max_length=250, verbose_name="Участок/отдел"
                    ),
                ),
                (
                    "safety_instructions",
                    models.CharField(
                        blank=True,
                        help_text="Номера инструкций через запятую",
                        max_length=250,
                        verbose_name="Инструкции по охране труда",
                    ),
                ),
                (
                    "electrical_safety_group",
                    models.IntegerField(
                        choices=[
                            (0, "Не требуется"),
                            (2, "II группа"),
                            (3, "III группа"),
                            (4, "IV группа"),
                            (5, "V группа"),
                        ],
                        default=0,
                        verbose_name="Группа по электробезопасности",
                    ),
                ),
                (
                    "internship_period",
                    models.PositiveIntegerField(
                        default=0,
                        help_text="0 - стажировка не требуется",
                        verbose_name="Срок стажировки (смен)",
                    ),
                ),
                (
                    "is_safety_responsible",
                    models.BooleanField(
                        default=False, verbose_name="Ответственный по ОТ"
                    ),
                ),
                (
                    "is_electrical_personnel",
                    models.BooleanField(
                        default=False, verbose_name="Электротехнический персонал"
                    ),
                ),
                (
                    "contract_instructions",
                    models.TextField(
                        blank=True, verbose_name="Должностные обязанности"
                    ),
                ),
                (
                    "department",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="departments.department",
                        verbose_name="Подразделение",
                    ),
                ),
                (
                    "familiarization_documents",
                    models.ManyToManyField(
                        blank=True,
                        to="documents.document",
                        verbose_name="Документы для ознакомления",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="organizations.organization",
                        verbose_name="Организация",
                    ),
                ),
            ],
            options={
                "verbose_name": "Должность",
                "verbose_name_plural": "Должности",
                "ordering": ["organization", "department", "name"],
                "unique_together": {("organization", "department", "name", "division")},
            },
        ),
        migrations.DeleteModel(
            name="Positions",
        ),
    ]
