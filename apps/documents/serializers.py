from rest_framework import serializers
from .models import Document, DocumentFamiliarization

class DocumentListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка документов"""
    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )
    familiarization_count = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'name', 'department_name',
            'approval_date', 'familiarization_count'
        ]

    def get_familiarization_count(self, obj):
        return obj.familiarized_employees.count()

class DocumentDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о документе"""
    file_url = serializers.SerializerMethodField()
    positions = serializers.SerializerMethodField()
    familiarizations = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id', 'organization', 'department',
            'name', 'description', 'file_url',
            'approval_date', 'positions',
            'familiarizations', 'created', 'updated'
        ]

    def get_file_url(self, obj):
        if obj.file:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.file.url)
        return None

    def get_positions(self, obj):
        return [
            {
                'id': pos.id,
                'name': pos.name,
                'department': pos.department.name
            }
            for pos in obj.positions_for_familiarization.all()
        ]

    def get_familiarizations(self, obj):
        return [
            {
                'employee': f"{fam.employee.last_name} {fam.employee.first_name}",
                'date': fam.familiarization_date
            }
            for fam in obj.documentfamiliarization_set.all()
        ]