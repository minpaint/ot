from typing import Dict, Any, List, Optional
from django.db import transaction
from django.db.models import Q
from .models import Employee

class EmployeeService:
    """Сервис для работы с сотрудниками"""

    @staticmethod
    @transaction.atomic
    def create_employee( Dict[str, Any]) -> Employee:
        """
        Создает нового сотрудника

        Args:
             Словарь с данными сотрудника
        Returns:
            Employee: Созданный сотрудник
        """
        return Employee.objects.create(**data)

    @staticmethod
    def get_employees_by_department(department_id: int) -> List[Employee]:
        """
        Получает всех сотрудников подразделения

        Args:
            department_id: ID подразделения
        Returns:
            List[Employee]: Список сотрудников
        """
        return Employee.objects.filter(department_id=department_id)

    @staticmethod
    def get_contractors() -> List[Employee]:
        """
        Получает всех сотрудников по договору подряда

        Returns:
            List[Employee]: Список сотрудников
        """
        return Employee.objects.filter(is_contractor=True)

    @staticmethod
    def search_employees(query: str) -> List[Employee]:
        """
        Поиск сотрудников по ФИО или должности

        Args:
            query: Поисковый запрос
        Returns:
            List[Employee]: Список сотрудников
        """
        return Employee.objects.filter(
            Q(last_name__icontains=query) |
            Q(first_name__icontains=query) |
            Q(middle_name__icontains=query) |
            Q(position__name__icontains=query)
        )

    @staticmethod
    def get_employee_details(employee_id: int) -> Dict[str, Any]:
        """
        Получает полную информацию о сотруднике

        Args:
            employee_id: ID сотрудника
        Returns:
            Dict[str, Any]: Информация о сотруднике
        """
        employee = Employee.objects.select_related(
            'organization',
            'department',
            'position'
        ).get(id=employee_id)

        return {
            'personal_info': {
                'full_name': employee.full_name,
                'full_name_dative': employee.full_name_dative,
                'birth_date': employee.birth_date,
                'contacts': {
                    'address': employee.address,
                    'phone': employee.phone,
                    'email': employee.email
                }
            },
            'work_info': {
                'organization': employee.organization.short_name,
                'department': employee.department.name,
                'position': employee.position.name,
                'is_contractor': employee.is_contractor
            },
            'position_details': {
                'safety_instructions': employee.position.safety_instructions,
                'electrical_safety_group': employee.position.electrical_safety_group,
                'is_safety_responsible': employee.position.is_safety_responsible,
                'is_electrical_personnel': employee.position.is_electrical_personnel
            }
        }