from typing import Dict, Any, Optional
from django.db import transaction
from .models import Department
from ..organizations.models import Organization

class DepartmentService:
    """Сервис для работы с подразделениями"""

    @staticmethod
    @transaction.atomic
    def create_department(
        organization: Organization,
        data: Dict[str, Any]
    ) -> Department:
        """
        Создает новое подразделение

        Args:
            organization: Организация
             Словарь с данными подразделения
        Returns:
            Department: Созданное подразделение
        """
        data['organization'] = organization
        return Department.add_root(**data)

    @staticmethod
    @transaction.atomic
    def create_child_department(
        parent: Department,
         Dict[str, Any]
    ) -> Department:
        """
        Создает дочернее подразделение

        Args:
            parent: Родительское подразделение
             Словарь с данными подразделения
        Returns:
            Department: Созданное подразделение
        """
        data['organization'] = parent.organization
        return parent.add_child(**data)

    @staticmethod
    def get_department_tree(
        organization_id: Optional[int] = None,
        department_id: Optional[int] = None
    ):
        """
        Получает дерево подразделений

        Args:
            organization_id: ID организации
            department_id: ID подразделения
        Returns:
            QuerySet: Дерево подразделений
        """
        qs = Department.objects
        if organization_id:
            qs = qs.filter(organization_id=organization_id)
        if department_id:
            dept = qs.get(id=department_id)
            return dept.get_descendants(include_self=True)
        return qs.get_tree()