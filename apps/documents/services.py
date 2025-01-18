from typing import Dict, Any, List, Optional
from django.db import transaction
from django.db.models import Q
from .models import Document

class DocumentService:
    """Сервис для работы с документами"""

    @staticmethod
    @transaction.atomic
    def create_document( Dict[str, Any]) -> Document:
        """
        Создает новый документ

        Args:
             Словарь с данными документа
        Returns:
            Document: Созданный документ
        """
        return Document.objects.create(**data)

    @staticmethod
    def get_documents_by_organization(
        organization_id: int,
        department_id: Optional[int] = None
    ) -> List[Document]:
        """
        Получает документы организации

        Args:
            organization_id: ID организации
            department_id: ID подразделения (опционально)
        Returns:
            List[Document]: Список документов
        """
        filters = {'organization_id': organization_id}
        if department_id:
            filters['department_id'] = department_id
        return Document.objects.filter(**filters)

    @staticmethod
    def search_documents(query: str) -> List[Document]:
        """
        Поиск документов по названию

        Args:
            query: Поисковый запрос
        Returns:
            List[Document]: Список документов
        """
        return Document.objects.filter(name__icontains=query)

    @staticmethod
    def get_documents_for_position(position_id: int) -> List[Document]:
        """
        Получает документы, связанные с должностью

        Args:
            position_id: ID должности
        Returns:
            List[Document]: Список документов
        """
        return Document.objects.filter(
            positions_for_familiarization__id=position_id
        )