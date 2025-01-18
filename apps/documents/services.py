from typing import Dict, Any, List, Optional
from django.db import transaction
from django.db.models import Q
from .models import Document

class DocumentService:
    """������ ��� ������ � �����������"""

    @staticmethod
    @transaction.atomic
    def create_document( Dict[str, Any]) -> Document:
        """
        ������� ����� ��������

        Args:
             ������� � ������� ���������
        Returns:
            Document: ��������� ��������
        """
        return Document.objects.create(**data)

    @staticmethod
    def get_documents_by_organization(
        organization_id: int,
        department_id: Optional[int] = None
    ) -> List[Document]:
        """
        �������� ��������� �����������

        Args:
            organization_id: ID �����������
            department_id: ID ������������� (�����������)
        Returns:
            List[Document]: ������ ����������
        """
        filters = {'organization_id': organization_id}
        if department_id:
            filters['department_id'] = department_id
        return Document.objects.filter(**filters)

    @staticmethod
    def search_documents(query: str) -> List[Document]:
        """
        ����� ���������� �� ��������

        Args:
            query: ��������� ������
        Returns:
            List[Document]: ������ ����������
        """
        return Document.objects.filter(name__icontains=query)

    @staticmethod
    def get_documents_for_position(position_id: int) -> List[Document]:
        """
        �������� ���������, ��������� � ����������

        Args:
            position_id: ID ���������
        Returns:
            List[Document]: ������ ����������
        """
        return Document.objects.filter(
            positions_for_familiarization__id=position_id
        )