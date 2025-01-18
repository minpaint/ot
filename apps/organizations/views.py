from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Organization
from .serializers import OrganizationSerializer, OrganizationTreeSerializer


class OrganizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с организациями
    """
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_serializer_class(self):
        if self.action == 'tree':
            return OrganizationTreeSerializer
        return OrganizationSerializer

    def get_queryset(self):
        """
        Возвращает отфильтрованный queryset организаций
        """
        queryset = Organization.objects.all()

        # Фильтрация по активности
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')

        # Поиск по имени
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                models.Q(full_name__icontains=search) |
                models.Q(short_name__icontains=search)
            )

        return queryset

    @action(detail=False, methods=['get'])
    def tree(self, request):
        """
        Возвращает древовидную структуру организаций
        """
        root_nodes = Organization.get_root_nodes()
        serializer = OrganizationTreeSerializer(root_nodes, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_child(self, request, pk=None):
        """
        Добавляет дочернюю организацию
        """
        parent = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            child = parent.add_child(**serializer.validated_data)
            response_serializer = self.get_serializer(child)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def move(self, request, pk=None):
        """
        Перемещает организацию в дереве
        """
        node = self.get_object()
        target_id = request.data.get('target')
        position = request.data.get('position', 'last-child')

        if not target_id:
            return Response(
                {'error': 'Target node ID is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            target = Organization.objects.get(pk=target_id)
            node.move(target, pos=position)
            serializer = self.get_serializer(node)
            return Response(serializer.data)
        except Organization.DoesNotExist:
            return Response(
                {'error': 'Target node not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )