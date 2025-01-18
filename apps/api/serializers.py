from rest_framework import serializers
from ..organizations.models import Organization
from ..departments.models import Department
from ..positions.models import Position
from ..employees.models import Employee
from ..documents.models import Document
from ..importer.models import ImportSession

class OrganizationSerializer(serializers.ModelSerializer):
    """������������ ��� ����������� (�������)"""
    class Meta:
        model = Organization
        fields = [
            'id',
            'full_name',
            'short_name',
            'name_by',
            'depth'
        ]

class OrganizationDetailSerializer(OrganizationSerializer):
    """������������ ��� ����������� (� ������ �����������)"""
    children = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()

    class Meta(OrganizationSerializer.Meta):
        fields = OrganizationSerializer.Meta.fields + [
            'details_ru',
            'details_by',
            'parent',
            'children'
        ]

    def get_children(self, obj):
        """�������� �������� �����������"""
        children = obj.get_children()
        return OrganizationSerializer(children, many=True).data

    def get_parent(self, obj):
        """�������� ������������ �����������"""
        parent = obj.get_parent()
        if parent:
            return OrganizationSerializer(parent).data
        return None

class DepartmentSerializer(serializers.ModelSerializer):
    """������������ ��� ������������� (�������)"""
    organization_name = serializers.CharField(
        source='organization.short_name',
        read_only=True
    )

    class Meta:
        model = Department
        fields = [
            'id',
            'name',
            'short_name',
            'organization',
            'organization_name',
            'depth'
        ]

class DepartmentDetailSerializer(DepartmentSerializer):
    """������������ ��� ������������� (� ������ �����������)"""
    children = serializers.SerializerMethodField()
    parent = serializers.SerializerMethodField()
    employees_count = serializers.SerializerMethodField()
    positions_count = serializers.SerializerMethodField()

    class Meta(DepartmentSerializer.Meta):
        fields = DepartmentSerializer.Meta.fields + [
            'parent',
            'children',
            'employees_count',
            'positions_count'
        ]

    def get_children(self, obj):
        """�������� �������� �������������"""
        children = obj.get_children()
        return DepartmentSerializer(children, many=True).data

    def get_parent(self, obj):
        """�������� ������������ �������������"""
        parent = obj.get_parent()
        if parent:
            return DepartmentSerializer(parent).data
        return None

    def get_employees_count(self, obj):
        """�������� ���������� ����������� � �������������"""
        return obj.employee_set.count()

    def get_positions_count(self, obj):
        """�������� ���������� ���������� � �������������"""
        return obj.position_set.count()

class PositionSerializer(serializers.ModelSerializer):
    """������������ ��� ���������� (�������)"""
    organization_name = serializers.CharField(
        source='organization.short_name',
        read_only=True
    )
    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )

    class Meta:
        model = Position
        fields = [
            'id',
            'name',
            'organization',
            'organization_name',
            'department',
            'department_name',
            'division',
            'electrical_safety_group',
            'is_safety_responsible',
            'is_electrical_personnel'
        ]

class PositionDetailSerializer(PositionSerializer):
    """������������ ��� ���������� (� ������ �����������)"""
    familiarization_documents = serializers.SerializerMethodField()
    employees_count = serializers.SerializerMethodField()

    class Meta(PositionSerializer.Meta):
        fields = PositionSerializer.Meta.fields + [
            'safety_instructions',
            'internship_period',
            'contract_instructions',
            'familiarization_documents',
            'employees_count'
        ]

    def get_familiarization_documents(self, obj):
        """�������� ��������� ��� ������������"""
        return DocumentSerializer(
            obj.familiarization_documents.all(),
            many=True
        ).data

    def get_employees_count(self, obj):
        """�������� ���������� ����������� �� ���������"""
        return obj.employee_set.count()

class EmployeeSerializer(serializers.ModelSerializer):
    """������������ ��� ����������� (�������)"""
    full_name = serializers.SerializerMethodField()
    organization_name = serializers.CharField(
        source='organization.short_name',
        read_only=True
    )
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
            'id',
            'full_name',
            'organization',
            'organization_name',
            'department',
            'department_name',
            'position',
            'position_name',
            'is_contractor'
        ]

    def get_full_name(self, obj):
        """�������� ������ ��� ����������"""
        return f"{obj.last_name} {obj.first_name} {obj.middle_name}"

class EmployeeDetailSerializer(EmployeeSerializer):
    """������������ ��� ����������� (� ������ �����������)"""
    position_details = serializers.SerializerMethodField()
    familiarization_documents = serializers.SerializerMethodField()

    class Meta(EmployeeSerializer.Meta):
        fields = EmployeeSerializer.Meta.fields + [
            'last_name',
            'first_name',
            'middle_name',
            'full_name_dative',
            'birth_date',
            'address',
            'phone',
            'email',
            'position_details',
            'familiarization_documents'
        ]

    def get_position_details(self, obj):
        """�������� ������ ���������"""
        position = obj.position
        return {
            'safety_instructions': position.safety_instructions,
            'electrical_safety_group': position.electrical_safety_group,
            'internship_period': position.internship_period,
            'is_safety_responsible': position.is_safety_responsible,
            'is_electrical_personnel': position.is_electrical_personnel
        }

    def get_familiarization_documents(self, obj):
        """�������� ��������� ��� ������������"""
        return DocumentSerializer(
            obj.position.familiarization_documents.all(),
            many=True
        ).data

class DocumentSerializer(serializers.ModelSerializer):
    """������������ ��� ���������� (�������)"""
    organization_name = serializers.CharField(
        source='organization.short_name',
        read_only=True
    )
    department_name = serializers.CharField(
        source='department.name',
        read_only=True
    )
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = [
            'id',
            'name',
            'organization',
            'organization_name',
            'department',
            'department_name',
            'approval_date',
            'file_url'
        ]

    def get_file_url(self, obj):
        """�������� URL ����� ���������"""
        if obj.file:
            return self.context['request'].build_absolute_uri(obj.file.url)
        return None

class DocumentDetailSerializer(DocumentSerializer):
    """������������ ��� ���������� (� ������ �����������)"""
    related_positions = serializers.SerializerMethodField()

    class Meta(DocumentSerializer.Meta):
        fields = DocumentSerializer.Meta.fields + ['related_positions']

    def get_related_positions(self, obj):
        """�������� ��������� ���������"""
        positions = obj.positions_for_familiarization.all()
        return PositionSerializer(positions, many=True).data

class ImportSerializer(serializers.ModelSerializer):
    """������������ ��� ������� ������"""
    class Meta:
        model = ImportSession
        fields = [
            'id',
            'content_type',
            'file',
            'status',
            'processed_rows',
            'total_rows',
            'errors',
            'created',
            'updated'
        ]
        read_only_fields = [
            'status',
            'processed_rows',
            'total_rows',
            'errors',
            'created',
            'updated'
        ]