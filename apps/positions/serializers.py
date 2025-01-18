from rest_framework import serializers
from .models import Position
from apps.departments.serializers import DepartmentSerializer
from apps.documents.serializers import DocumentSerializer


class PositionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Position"""
    department_data = DepartmentSerializer(source='department', read_only=True)
    familiarization_documents_data = DocumentSerializer(source='familiarization_documents', many=True, read_only=True)

    class Meta:
        model = Position
        fields = [
            'id',
            'organization',
            'department',
            'department_data',
            'name',
            'division',
            'safety_instructions',
            'electrical_safety_group',
            'internship_period',
            'is_safety_responsible',
            'is_electrical_personnel',
            'contract_instructions',
            'familiarization_documents',
            'familiarization_documents_data'
        ]