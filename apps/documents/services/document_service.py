from django.db.models import Q
from ..models import Document

class DocumentService:
    @staticmethod
    def search_documents(query):
        """Поиск документов"""
        return Document.objects.filter(
            Q(name__icontains=query) |
            Q(content__icontains=query)
        )

    @staticmethod
    def get_documents_for_position(position_id):
        """Получает документы для должности"""
        return Document.objects.filter(
            positions_for_familiarization__id=position_id
        )

    @staticmethod
    def get_documents_for_department(department_id):
        """Получает документы подразделения"""
        return Document.objects.filter(department_id=department_id)

    @staticmethod
    def mark_as_familiarized(document_id, employee_id):
        """Отмечает, что сотрудник ознакомлен с документом"""
        document = Document.objects.get(pk=document_id)
        document.familiarized_employees.add(employee_id)
        return document