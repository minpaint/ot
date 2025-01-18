from typing import Dict, Any, Optional
from django.db import transaction
from .models import Organization

class OrganizationService:
    """Сервис для работы с организациями"""

    @staticmethod
    @transaction.atomic
    def create_organization( Dict[str, Any]) -> Organization:
        """
        Создает новую организацию

        Args:
             Словарь с данными организации
        Returns:
            Organization: Созданная организация
        """
        return Organization.add_root(**data)

    @staticmethod
    @transaction.atomic
    def create_child_organization(
        parent: Organization,
         Dict[str, Any]
    ) -> Organization:
        """
        Создает дочернюю организацию

        Args:
            parent: Родительская организация
            data: Словарь с данными организации
        Returns:
            Organization: Созданная организация
        """
        return parent.add_child(**data)

    @staticmethod
    def get_organization_tree(organization_id: Optional[int] = None):
        """
        Получает дерево организаций

        Args:
            organization_id: ID организации (если None, возвращает все дерево)
        Returns:
            QuerySet: Дерево организаций
        """
        if organization_id:
            org = Organization.objects.get(id=organization_id)
            return org.get_descendants(include_self=True)
        return Organization.get_tree()