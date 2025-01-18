import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from ..models import ImportSession
from ..services.import_handler import ImportService

@pytest.mark.django_db
class TestImport:
    def test_create_import_session(self):
        """Тест создания сессии импорта"""
        content = b'test,data\n1,2,3'
        file = SimpleUploadedFile('test.csv', content)

        import_session = ImportSession.objects.create(
            file=file,
            content_type_id=1
        )

        assert isinstance(import_session, ImportSession)
        assert import_session.status == 'pending'

    def test_import_process(self, mocker):
        """Тест процесса импорта"""
        mock_process = mocker.patch.object(ImportService, 'process_import')
        content = b'test,data\n1,2,3'
        file = SimpleUploadedFile('test.csv', content)

        import_session = ImportSession.objects.create(
            file=file,
            content_type_id=1
        )

        ImportService.process_import(import_session.id)
        mock_process.assert_called_once_with(import_session.id)

@pytest.mark.django_db
class TestImportAPI:
    def test_start_import(self, api_client):
        """Тест начала импорта через API"""
        content = b'test,data\n1,2,3'
        file = SimpleUploadedFile('test.csv', content)

        url = reverse('api:import')
        data = {
            'file': file,
            'content_type': 1
        }
        response = api_client.post(url, data, format='multipart')

        assert response.status_code == status.HTTP_200_OK
        assert 'import_id' in response.data

    def test_import_status(self, api_client):
        """Тест получения статуса импорта"""
        content = b'test,data\n1,2,3'
        file = SimpleUploadedFile('test.csv', content)

        import_session = ImportSession.objects.create(
            file=file,
            content_type_id=1,
            status='processing',
            processed_rows=50,
            total_rows=100
        )

        url = reverse('api:import-status', kwargs={'pk': import_session.pk})
        response = api_client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'processing'
        assert response.data['processed_rows'] == 50
        assert response.data['total_rows'] == 100