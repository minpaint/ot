from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Document"""
    class Meta:
        model = Document
        fields = [
            'id',
            'organization',
            'name',
            'number',
            'date',
            'file',
            'created',
            'updated'
        ]