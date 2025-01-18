from rest_framework import serializers
from .models import Position


class PositionSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Position"""

    class Meta:
        model = Position
        fields = [
            'id',
            'organization',
            'department',
            'name',
            'division',
            'safety_instructions',
            'electrical_safety_group',
            'internship_period',
            'is_safety_responsible',
            'is_electrical_personnel',
            'contract_instructions',
            'familiarization_documents'
        ]