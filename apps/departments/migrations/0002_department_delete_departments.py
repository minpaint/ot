# Generated by Django 4.2.18 on 2025-01-18 09:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("organizations", "0002_organization_delete_organizations"),
        ("departments", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Department",
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
                ("name", models.CharField(max_length=250, verbose_name="Наименование")),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Создано"),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, verbose_name="Изменено"),
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
                "verbose_name": "Подразделение",
                "verbose_name_plural": "Подразделения",
                "ordering": ["name"],
                "unique_together": {("organization", "name")},
            },
        ),
        migrations.DeleteModel(
            name="Departments",
        ),
    ]
