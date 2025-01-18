from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Document
from .serializers import DocumentSerializer
from apps.core.permissions import HasOrganizationPermission

class DocumentViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с документами"""
    permission_classes = [IsAuthenticated, HasOrganizationPermission]
    serializer_class = DocumentSerializer

    def get_queryset(self):
        """
        Возвращает queryset документов в зависимости от прав пользователя
        """
        user = self.request.user
        if user.is_superuser:
            return Document.objects.all()
        return Document.objects.filter(organization__in=user.organizations.all())

    def perform_create(self, serializer):
        """
        Привязываем создаваемый документ к организации пользователя
        """
        if not self.request.user.is_superuser and self.request.user.organizations.count() == 1:
            serializer.save(organization=self.request.user.organizations.first())
        else:
            serializer.save()