from rest_framework import serializers
from .models import ImportSession

class ImportSessionSerializer(serializers.ModelSerializer):
    """Сериализатор для сессии импорта"""
    progress = serializers.SerializerMethodField()

    class Meta:
        model = ImportSession
        fields = [
            'id', 'file', 'content_type',
            'status', 'processed_rows', 'total_rows',
            'errors', 'progress', 'created', 'updated'
        ]
        read_only_fields = [
            'status', 'processed_rows', 'total_rows',
            'errors', 'progress'
        ]

    def get_progress(self, obj):
        if obj.total_rows:
            return round((obj.processed_rows / obj.total_rows) * 100, 2)
        return 0