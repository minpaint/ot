from typing import Dict, Any, Optional
from django.db import transaction
from .models import Organization

class OrganizationService:
    """������ ��� ������ � �������������"""

    @staticmethod
    @transaction.atomic
    def create_organization( Dict[str, Any]) -> Organization:
        """
        ������� ����� �����������

        Args:
             ������� � ������� �����������
        Returns:
            Organization: ��������� �����������
        """
        return Organization.add_root(**data)

    @staticmethod
    @transaction.atomic
    def create_child_organization(
        parent: Organization,
         Dict[str, Any]
    ) -> Organization:
        """
        ������� �������� �����������

        Args:
            parent: ������������ �����������
            data: ������� � ������� �����������
        Returns:
            Organization: ��������� �����������
        """
        return parent.add_child(**data)

    @staticmethod
    def get_organization_tree(organization_id: Optional[int] = None):
        """
        �������� ������ �����������

        Args:
            organization_id: ID ����������� (���� None, ���������� ��� ������)
        Returns:
            QuerySet: ������ �����������
        """
        if organization_id:
            org = Organization.objects.get(id=organization_id)
            return org.get_descendants(include_self=True)
        return Organization.get_tree()