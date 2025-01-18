from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from apps.organizations.models import Organization
from apps.departments.models import Department
from apps.positions.models import Position
from apps.employees.models import Employee
from apps.documents.models import Document

# ... (предыдущие тесты остаются без изменений)

class DocumentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.org = Organization.objects.create(
            full_name='Test Organization',
            short_name='Test Org'
        )
        self.dept = Department.objects.create(
            organization=self.org,
            name='Test Department'
        )
        self.doc = Document.objects.create(
            organization=self.org,
            department=self.dept,
            name='Test Document',
            description='Test document description',
            document_type='POLICY'
        )

    def test_document_list_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('documents:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_list.html')
        self.assertContains(response, 'Test Document')
        self.assertContains(response, 'Test Department')

        # Проверка фильтрации
        response = self.client.get(f"{reverse('documents:list')}?department={self.dept.id}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Document')

        response = self.client.get(f"{reverse('documents:list')}?search=Test")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Document')

        # Проверка пагинации
        for i in range(11):  # Создаем дополнительные документы
            Document.objects.create(
                organization=self.org,
                department=self.dept,
                name=f'Test Document {i}',
                document_type='POLICY'
            )
        response = self.client.get(reverse('documents:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertEqual(len(response.context['documents']), 10)

    def test_document_detail_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('documents:detail', args=[self.doc.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_detail.html')
        self.assertContains(response, 'Test Document')
        self.assertContains(response, 'Test document description')
        self.assertContains(response, 'Test Department')

    def test_document_create_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('documents:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_form.html')

        # Тест создания документа
        data = {
            'organization': self.org.id,
            'department': self.dept.id,
            'name': 'New Test Document',
            'description': 'New test document description',
            'document_type': 'POLICY',
            'status': 'ACTIVE'
        }
        response = self.client.post(reverse('documents:create'), data)
        self.assertEqual(response.status_code, 302)  # Редирект после создания
        self.assertTrue(
            Document.objects.filter(name='New Test Document').exists()
        )

    def test_document_update_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('documents:update', args=[self.doc.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'documents/document_form.html')

        # Тест обновления документа
        data = {
            'organization': self.org.id,
            'department': self.dept.id,
            'name': 'Updated Test Document',
            'description': 'Updated test document description',
            'document_type': 'POLICY',
            'status': 'ACTIVE'
        }
        response = self.client.post(
            reverse('documents:update', args=[self.doc.pk]),
            data
        )
        self.assertEqual(response.status_code, 302)  # Редирект после обновления
        self.doc.refresh_from_db()
        self.assertEqual(self.doc.name, 'Updated Test Document')

    def test_document_delete_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(
            reverse('documents:delete', args=[self.doc.pk])
        )
        self.assertEqual(response.status_code, 302)  # Редирект после удаления
        self.assertFalse(
            Document.objects.filter(pk=self.doc.pk).exists()
        )

    def test_document_download_view(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('documents:download', args=[self.doc.pk])
        )
        self.assertEqual(response.status_code, 200)
        # Проверка заголовков ответа для скачивания файла
        self.assertEqual(
            response['Content-Disposition'],
            f'attachment; filename="{self.doc.name}.pdf"'
        )

    def test_unauthorized_access(self):
        # Тест доступа без авторизации
        response = self.client.get(reverse('documents:list'))
        self.assertEqual(response.status_code, 302)  # Редирект на страницу входа
        self.assertRedirects(
            response, 
            f'/login/?next={reverse("documents:list")}'
        )