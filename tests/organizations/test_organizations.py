import pytest
from django.urls import reverse
from rest_framework import status
from ..models import Organization
from .factories import OrganizationFactory

@pytest.mark.django_db
class TestOrganization:
    def test_create_organization(self):
        """Тест создания организации"""
        org = OrganizationFactory()
        assert isinstance(org, Organization)
        assert org.pk is not None

    def test_organization_str(self):
        """Тест строкового представления"""
        org = OrganizationFactory()
        assert str(org) == org.short_name

    def test_organization_tree(self):
        """Тест дерева организаций"""
        parent = OrganizationFactory()
        child1 = OrganizationFactory(parent=parent)
        child2 = OrganizationFactory(parent=parent)

        assert parent.get_children().count() == 2
        assert child1.get_parent() == parent
        assert child2.get_parent() == parent

@pytest.mark.django_db
class TestOrganizationAPI:
    def test_list_organizations(self, api_client):
        """Тест получения списка организаций"""
        OrganizationFactory.create_batch(3)
        url = reverse('api:organization-list')
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 3

    def test_create_organization_api(self, api_client):
        """Тест создания организации через API"""
        url = reverse('api:organization-list')
        data = {
            'full_name': 'Test Organization',
            'short_name': 'TestOrg',
            'details_ru': 'Test Details'
        }
        response = api_client.post(url, data)

        assert response.status_code == status.HTTP_201_CREATED
        assert Organization.objects.count() == 1

    def test_update_organization(self, api_client):
        """Тест обновления организации"""
        org = OrganizationFactory()
        url = reverse('api:organization-detail', kwargs={'pk': org.pk})
        data = {'short_name': 'Updated Name'}

        response = api_client.patch(url, data)
        org.refresh_from_db()

        assert response.status_code == status.HTTP_200_OK
        assert org.short_name == 'Updated Name'

    def test_delete_organization(self, api_client):
        """Тест удаления организации"""
        org = OrganizationFactory()
        url = reverse('api:organization-detail', kwargs={'pk': org.pk})

        response = api_client.delete(url)

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Organization.objects.count() == 0