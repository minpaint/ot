from django.db.models import Q
from ..models import Organization

class OrganizationService:
    @staticmethod
    def get_organization_tree(org_id=None):
        """Получает дерево организаций"""
        if org_id:
            org = Organization.objects.get(pk=org_id)
            return org.get_descendants()
        return Organization.objects.all()

    @staticmethod
    def search_organizations(query):
        """Поиск организаций"""
        return Organization.objects.filter(
            Q(full_name__icontains=query) |
            Q(short_name__icontains=query)
        )

    @staticmethod
    def move_organization(org_id, new_parent_id=None):
        """Перемещает организацию в дереве"""
        org = Organization.objects.get(pk=org_id)
        if new_parent_id:
            new_parent = Organization.objects.get(pk=new_parent_id)
            org.move(new_parent)
        else:
            org.move(None)  # Перемещение в корень
        return org