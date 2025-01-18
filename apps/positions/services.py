from typing import Dict, Any, List, Optional
from django.db import transaction
from django.db.models import Q
from .models import Position
from ..documents.models import Document

class PositionService:
    """Сервис для работы с должностями"""

    @staticmethod
    @transaction.atomic
    def create_position(data: Dict[str, Any]) -> Position:
        """
        Создает новую должность

        Args:
             Словарь с данными должности
        Returns:
            Position: Созданная должность
        """
        familiarization_docs = data.pop('familiarization_documents', [])
        position = Position.objects.create(**data)

        if familiarization_docs:
            position.familiarization_documents.set(familiarization_docs)

        return position

    @staticmethod
    def get_positions_by_department(department_id: int) -> List[Position]:
        """
        Получает все должности подразделения

        Args:
            department_id: ID подразделения
        Returns:
            List[Position]: Список должностей
        """
        return Position.objects.filter(department_id=department_id)

    @staticmethod
    def get_positions_with_safety_responsibility() -> List[Position]:
        """
        Получает все должности с ответственностью за охрану труда

        Returns:
            List[Position]: Список должностей
        """
        return Position.objects.filter(is_safety_responsible=True)

    @staticmethod
    def get_electrical_personnel_positions() -> List[Position]:
        """
        Получает все должности электротехнического персонала

        Returns:
            List[Position]: Список должностей
        """
        return Position.objects.filter(is_electrical_personnel=True)

    @staticmethod
    def search_positions(query: str) -> List[Position]:
        """
        Поиск должностей по названию или отделу

        Args:
            query: Поисковый запрос
        Returns:
            List[Position]: Список должностей
        """
        return Position.objects.filter(
            Q(name__icontains=query) |
            Q(division__icontains=query)
        )