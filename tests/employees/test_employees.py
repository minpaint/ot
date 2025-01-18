import pytest
from django.urls import reverse
from rest_framework import status
from ..models import Employee
from .factories import EmployeeFactory, DepartmentFactory, PositionFactory

@pytest.mark.django_db
class TestEmployee:
    def test_create_employee(self):
        """Тест создания сотрудника"""
        employee = EmployeeFactory()
        assert isinstance(employee, Employee)
        assert employee.pk is not None

    def test_employee_full_name(self):
        """Тест полного имени сотрудника"""
        employee = EmployeeFactory(
            last_name='Иванов',
            first_name='Иван',
            middle_name='Иванович'
        )
        assert employee.get_full_name() == 'Иванов Иван Иванович'

    def test_employee_department_position(self):
        """Тест связей с подразделением и должностью"""
        department = DepartmentFactory()
        position = PositionFactory(department=department)
        employee = EmployeeFactory(
            department=department,
            position=position
        )

        assert employee.department == department
        assert employee.position == position

@pytest.mark.django_db
class TestEmployeeAPI:
    def test_list_employees(self, api_client):
        """Тест получения списка сотрудников"""
        EmployeeFactory.create_batch(3)
        url = reverse('api:employee-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3

    def test_create_employee_api(self, api_client):
        """Тест создания сотрудника через API"""
        department = DepartmentFactory()
        position = PositionFactory(department=department)

        url = reverse('api:employee-list')
        data = {
            'last_name': 'Петров',
            'first_name': 'Петр',
            'middle_name': 'Петрович',
            'department': department.pk,
            'position': position.pk
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Employee.objects.count() == 1

    def test_search_employees(self, api_client):
        """Тест поиска сотрудников"""
        EmployeeFactory(last_name='Иванов')
        EmployeeFactory(last_name='Петров')

        url = reverse('api:employee-list')
        response = api_client.get(url, {'search': 'Иванов'})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 1
        assert response.data['results'][0]['last_name'] == 'Иванов'

    def test_filter_employees_by_department(self, api_client):
        """Тест фильтрации сотрудников по подразделению"""
        department1 = DepartmentFactory()
        department2 = DepartmentFactory()

        EmployeeFactory(department=department1)
        EmployeeFactory(department=department1)
        EmployeeFactory(department=department2)

        url = reverse('api:employee-list')
        response = api_client.get(url, {'department': department1.pk})

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2