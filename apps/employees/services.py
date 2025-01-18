from typing import Dict, Any, List, Optional
from django.db import transaction
from django.db.models import Q
from .models import Employee

class EmployeeService:
    """������ ��� ������ � ������������"""

    @staticmethod
    @transaction.atomic
    def create_employee( Dict[str, Any]) -> Employee:
        """
        ������� ������ ����������

        Args:
             ������� � ������� ����������
        Returns:
            Employee: ��������� ���������
        """
        return Employee.objects.create(**data)

    @staticmethod
    def get_employees_by_department(department_id: int) -> List[Employee]:
        """
        �������� ���� ����������� �������������

        Args:
            department_id: ID �������������
        Returns:
            List[Employee]: ������ �����������
        """
        return Employee.objects.filter(department_id=department_id)

    @staticmethod
    def get_contractors() -> List[Employee]:
        """
        �������� ���� ����������� �� �������� �������

        Returns:
            List[Employee]: ������ �����������
        """
        return Employee.objects.filter(is_contractor=True)

    @staticmethod
    def search_employees(query: str) -> List[Employee]:
        """
        ����� ����������� �� ��� ��� ���������

        Args:
            query: ��������� ������
        Returns:
            List[Employee]: ������ �����������
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
        �������� ������ ���������� � ����������

        Args:
            employee_id: ID ����������
        Returns:
            Dict[str, Any]: ���������� � ����������
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