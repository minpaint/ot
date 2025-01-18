import pytest
from rest_framework.test import APIClient
from .factories import UserFactory

@pytest.fixture
def user():
    """Фикстура для создания пользователя"""
    return UserFactory()

@pytest.fixture
def api_client(user):
    """Фикстура для создания авторизованного API клиента"""
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def unauthorized_client():
    """Фикстура для создания неавторизованного API клиента"""
    return APIClient()