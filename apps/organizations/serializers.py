from rest_framework import serializers
from treebeard.mp_tree import MP_Node
from .models import Organization


class OrganizationSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Organization
    """

    class Meta:
        model = Organization
        fields = [
            'id',
            'path',
            'depth',
            'numchild',
            'full_name',
            'short_name',
            'description',
            'is_active',
            'created',
            'updated'
        ]
        read_only_fields = ['path', 'depth', 'numchild']


class OrganizationTreeSerializer(serializers.ModelSerializer):
    """
    Сериализатор для древовидного представления организаций
    """
    children = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = [
            'id',
            'full_name',
            'short_name',
            'description',
            'is_active',
            'children'
        ]

    def get_children(self, obj):
        """
        Рекурсивно получает дочерние организации
        """
        children = obj.get_children()
        serializer = self.__class__(children, many=True)
        return serializer.data