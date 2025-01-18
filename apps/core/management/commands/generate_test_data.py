from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.organizations.models import Organization
from apps.departments.models import Department
from apps.positions.models import Position
from apps.employees.models import Employee
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Генерация тестовых данных'

    def add_arguments(self, parser):
        parser.add_argument(
            '--organizations',
            type=int,
            default=5,
            help='Количество организаций'
        )
        parser.add_argument(
            '--departments',
            type=int,
            default=3,
            help='Количество подразделений на организацию'
        )
        parser.add_argument(
            '--positions',
            type=int,
            default=5,
            help='Количество должностей на подразделение'
        )
        parser.add_argument(
            '--employees',
            type=int,
            default=10,
            help='Количество сотрудников на должность'
        )

    def handle(self, *args, **options):
        fake = Faker('ru_RU')

        # Создаем организации
        organizations = []
        for i in range(options['organizations']):
            org = Organization.objects.create(
                full_name=f'ОАО "{fake.company()}"',
                short_name=f'ОАО "{fake.company_prefix()}"',
                details_ru=fake.text(),
                details_by=fake.text()
            )
            organizations.append(org)
            self.stdout.write(f'Создана организация: {org.short_name}')

            # Создаем подразделения
            for j in range(options['departments']):
                dept = Department.objects.create(
                    organization=org,
                    name=fake.job(),
                    description=fake.text()
                )
                self.stdout.write(f'Создано подразделение: {dept.name}')

                # Создаем должности
                for k in range(options['positions']):
                    pos = Position.objects.create(
                        organization=org,
                        department=dept,
                        name=fake.job(),
                        description=fake.text()
                    )
                    self.stdout.write(f'Создана должность: {pos.name}')

                    # Создаем сотрудников
                    for l in range(options['employees']):
                        emp = Employee.objects.create(
                            organization=org,
                            department=dept,
                            position=pos,
                            last_name=fake.last_name(),
                            first_name=fake.first_name(),
                            middle_name=fake.middle_name(),
                            birth_date=fake.date_of_birth(minimum_age=18, maximum_age=65),
                            address=fake.address(),
                            phone=fake.phone_number(),
                            email=fake.email()
                        )
                        self.stdout.write(f'Создан сотрудник: {emp.get_full_name()}')

        self.stdout.write(
            self.style.SUCCESS('Тестовые данные успешно сгенерированы')
        )