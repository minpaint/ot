from django.test import TestCase
from apps.organizations.forms import OrganizationForm
from apps.employees.forms import EmployeeForm
from apps.documents.forms import DocumentForm
from apps.organizations.models import Organization
from apps.departments.models import Department
from apps.positions.models import Position
from django.core.files.uploadedfile import SimpleUploadedFile

class OrganizationFormTest(TestCase):
    def test_organization_form_valid(self):
        form_data = {
            'full_name': 'Test Organization Full Name',
            'short_name': 'Test Org',
            'details_ru': 'Test details in Russian',
            'details_by': 'Test details in Belarusian'
        }
        form = OrganizationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_organization_form_invalid(self):
        form_data = {
            'full_name': '',  # Обязательное поле
            'short_name': 'Test Org'
        }
        form = OrganizationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('full_name' in form.errors)

class EmployeeFormTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(
            full_name='Test Organization',
            short_name='Test Org'
        )
        self.dept = Department.objects.create(
            organization=self.org,
            name='Test Department'
        )
        self.pos = Position.objects.create(
            organization=self.org,
            department=self.dept,
            name='Test Position'
        )

    def test_employee_form_valid(self):
        form_data = {
            'organization': self.org.id,
            'department': self.dept.id,
            'position': self.pos.id,
            'last_name': 'Test',
            'first_name': 'Employee',
            'middle_name': 'Middle',
            'birth_date': '1990-01-01',
            'phone': '+1234567890',
            'email': 'test@example.com'
        }
        photo = SimpleUploadedFile(
            "test_photo.jpg",
            b"file_content",
            content_type="image/jpeg"
        )
        form = EmployeeForm(data=form_data, files={'photo': photo})
        self.assertTrue(form.is_valid())

    def test_employee_form_invalid(self):
        form_data = {
            'organization': self.org.id,
            'department': self.dept.id,
            'position': self.pos.id,
            'last_name': '',  # Обязательное поле
            'first_name': 'Employee',
            'email': 'invalid_email'  # Неверный формат email
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('last_name' in form.errors)
        self.assertTrue('email' in form.errors)

class DocumentFormTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(
            full_name='Test Organization',
            short_name='Test Org'
        )
        self.dept = Department.objects.create(
            organization=self.org,
            name='Test Department'
        )

    def test_document_form_valid(self):
        form_data = {
            'organization': self.org.id,
            'department': self.dept.id,
            'name': 'Test Document',
            'description': 'Test document description',
            'document_type': 'POLICY',
            'status': 'ACTIVE',
            'approval_date': '2023-01-01'
        }
        file = SimpleUploadedFile(
            "test_doc.pdf",
            b"file_content",
            content_type="application/pdf"
        )
        form = DocumentForm(data=form_data, files={'file': file})
        self.assertTrue(form.is_valid())

    def test_document_form_invalid(self):
        form_data = {
            'organization': self.org.id,
            'department': self.dept.id,
            'name': '',  # Обязательное поле
            'document_type': 'INVALID_TYPE'  # Неверный тип документа
        }
        form = DocumentForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('name' in form.errors)
        self.assertTrue('document_type' in form.errors)