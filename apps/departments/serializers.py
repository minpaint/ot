from rest_framework import serializers
from .models import Department


class DepartmentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Department."""

    class Meta:
        model = Department
        fields = ['id', 'name', 'organization']