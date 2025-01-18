import factory
from django.contrib.auth.models import User
from ..models import (
    Organization,
    Department,
    Position,
    Employee,
    Document
)

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization

    full_name = factory.Sequence(lambda n: f'Organization {n}')
    short_name = factory.Sequence(lambda n: f'Org{n}')
    details_ru = factory.Faker('text', locale='ru_RU')
    details_by = factory.Faker('text', locale='ru_RU')

class DepartmentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Department

    organization = factory.SubFactory(OrganizationFactory)
    name = factory.Sequence(lambda n: f'Department {n}')
    short_name = factory.Sequence(lambda n: f'Dept{n}')

class PositionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Position

    organization = factory.SubFactory(OrganizationFactory)
    department = factory.SubFactory(DepartmentFactory)
    name = factory.Sequence(lambda n: f'Position {n}')
    division = factory.Sequence(lambda n: f'Division {n}')
    safety_instructions = factory.Faker('text')
    electrical_safety_group = factory.Iterator(['I', 'II', 'III', 'IV', 'V'])

class EmployeeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Employee

    organization = factory.SubFactory(OrganizationFactory)
    department = factory.SubFactory(DepartmentFactory)
    position = factory.SubFactory(PositionFactory)
    last_name = factory.Faker('last_name', locale='ru_RU')
    first_name = factory.Faker('first_name', locale='ru_RU')
    middle_name = factory.Faker('middle_name', locale='ru_RU')
    birth_date = factory.Faker('date_of_birth')
    address = factory.Faker('address', locale='ru_RU')
    phone = factory.Faker('phone_number', locale='ru_RU')
    email = factory.LazyAttribute(
        lambda obj: f'{obj.last_name.lower()}@example.com'
    )

class DocumentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Document

    organization = factory.SubFactory(OrganizationFactory)
    department = factory.SubFactory(DepartmentFactory)
    name = factory.Sequence(lambda n: f'Document {n}')
    approval_date = factory.Faker('date')
    file = factory.django.FileField(filename='test.pdf')