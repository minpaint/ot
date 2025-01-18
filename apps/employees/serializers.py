from rest_framework import serializers
from .models import Employee
from apps.organizations.serializers import OrganizationSerializer
from apps.departments.serializers import DepartmentSerializer
from apps.positions.serializers import PositionSerializer

class EmployeeListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка сотрудников"""
    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )
    position_name = serializers.CharField(
        source='position.name',
        read_only=True
    )

    class Meta:
        model = Employee
        fields = [
            'id', 'last_name', 'first_name',
            'middle_name', 'department_name',
            'position_name'
        ]

class EmployeeDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной информации о сотруднике"""
    organization = OrganizationSerializer(read_only=True)
    department = DepartmentSerializer(read_only=True)
    position = PositionSerializer(read_only=True)
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = [
            'id', 'organization', 'department',
            'position', 'last_name', 'first_name',
            'middle_name', 'full_name', 'birth_date',
            'age', 'address', 'phone', 'email',
            'photo', 'created', 'updated'
        ]

    def get_full_name(self, obj):
        return obj.get_full_name()

    def get_age(self, obj):
        from core.utils.helpers import get_age
        return get_age(obj.birth_date)