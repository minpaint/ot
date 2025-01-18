from django.db.models import Q
from ..models import Employee

class EmployeeService:
    @staticmethod
    def search_employees(query):
        """Поиск сотрудников"""
        return Employee.objects.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(position__name__icontains=query)
        )

    @staticmethod
    def get_employees_by_department(department_id):
        """Получает сотрудников подразделения"""
        return Employee.objects.filter(department_id=department_id)

    @staticmethod
    def get_employees_by_position(position_id):
        """Получает сотрудников на должности"""
        return Employee.objects.filter(position_id=position_id)

    @staticmethod
    def transfer_employee(employee_id, new_department_id, new_position_id=None):
        """Переводит сотрудника в другое подразделение/должность"""
        employee = Employee.objects.get(pk=employee_id)
        employee.department_id = new_department_id
        if new_position_id:
            employee.position_id = new_position_id
        employee.save()
        return employee