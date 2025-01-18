from typing import Dict, Any, List, Optional
from django.db import transaction
from django.db.models import Q
from .models import Position
from ..documents.models import Document

class PositionService:
    """������ ��� ������ � �����������"""

    @staticmethod
    @transaction.atomic
    def create_position(data: Dict[str, Any]) -> Position:
        """
        ������� ����� ���������

        Args:
             ������� � ������� ���������
        Returns:
            Position: ��������� ���������
        """
        familiarization_docs = data.pop('familiarization_documents', [])
        position = Position.objects.create(**data)

        if familiarization_docs:
            position.familiarization_documents.set(familiarization_docs)

        return position

    @staticmethod
    def get_positions_by_department(department_id: int) -> List[Position]:
        """
        �������� ��� ��������� �������������

        Args:
            department_id: ID �������������
        Returns:
            List[Position]: ������ ����������
        """
        return Position.objects.filter(department_id=department_id)

    @staticmethod
    def get_positions_with_safety_responsibility() -> List[Position]:
        """
        �������� ��� ��������� � ���������������� �� ������ �����

        Returns:
            List[Position]: ������ ����������
        """
        return Position.objects.filter(is_safety_responsible=True)

    @staticmethod
    def get_electrical_personnel_positions() -> List[Position]:
        """
        �������� ��� ��������� ������������������� ���������

        Returns:
            List[Position]: ������ ����������
        """
        return Position.objects.filter(is_electrical_personnel=True)

    @staticmethod
    def search_positions(query: str) -> List[Position]:
        """
        ����� ���������� �� �������� ��� ������

        Args:
            query: ��������� ������
        Returns:
            List[Position]: ������ ����������
        """
        return Position.objects.filter(
            Q(name__icontains=query) |
            Q(division__icontains=query)
        )