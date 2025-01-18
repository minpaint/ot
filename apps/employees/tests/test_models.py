from django.test import TestCase
from django.core.exceptions import ValidationError
from apps.organizations.models import Organization
from apps.departments.models import Department
from apps.positions.models import Position
from apps.employees.models import Employee
from apps.documents.models import Document
from django.utils import timezone

class OrganizationModelTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(
            full_name='Test Organization Full Name',
            short_name='Test Org',
            details_ru='Test details in Russian',
            details_by='Test details in Belarusian'
        )

    def test_organization_creation(self):
        self.assertTrue(isinstance(self.org, Organization))
        self.assertEqual(str(self.org), 'Test Org')

    def test_organization_fields(self):
        self.assertEqual(self.org.full_name, 'Test Organization Full Name')
        self.assertEqual(self.org.short_name, 'Test Org')
        self.assertEqual(self.org.details_ru, 'Test details in Russian')
        self.assertEqual(self.org.details_by, 'Test details in Belarusian')

class DepartmentModelTest(TestCase):
    def setUp(self):
        self.org = Organization.objects.create(
            full_name='Test Organization',
            short_name='Test Org'
        )
        self.dept = Department.objects.create(
            organization=self.org,
            name='Test Department',
            description='Test department description'
        )

    def test_department_creation(self):
        self.assertTrue(isinstance(self.dept, Department))
        self.assertEqual(str(self.dept), 'Test Department')

    def test_department_organization_relationship(self):
        self.assertEqual(self.dept.organization, self.org)

class PositionModelTest(TestCase):
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
            name='Test Position',
            description='Test position description'
        )

    def test_position_creation(self):
        self.assertTrue(isinstance(self.pos, Position))
        self.assertEqual(str(self.pos), 'Test Position')

    def test_position_relationships(self):
        self.assertEqual(self.pos.organization, self.org)
        self.assertEqual(self.pos.department, self.dept)

class EmployeeModelTest(TestCase):
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
        self.employee = Employee.objects.create(
            organization=self.org,
            department=self.dept,
            position=self.pos,
            last_name='Test',
            first_name='Employee',
            middle_name='Middle',
            birth_date='1990-01-01',
            phone='+1234567890',
            email='test@example.com'
        )

    def test_employee_creation(self):
        self.assertTrue(isinstance(self.employee, Employee))
        self.assertEqual(str(self.employee), 'Test Employee Middle')

    def test_employee_relationships(self):
        self.assertEqual(self.employee.organization, self.org)
        self.assertEqual(self.employee.department, self.dept)
        self.assertEqual(self.employee.position, self.pos)

    def test_employee_full_name(self):
        self.assertEqual(
            self.employee.get_full_name(),
            'Test Employee Middle'
        )

class DocumentModelTest(TestCase):
    def setUp(self):
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
            document_type='POLICY',
            approval_date=timezone.now().date()
        )

    def test_document_creation(self):
        self.assertTrue(isinstance(self.doc, Document))
        self.assertEqual(str(self.doc), 'Test Document')

    def test_document_relationships(self):
        self.assertEqual(self.doc.organization, self.org)
        self.assertEqual(self.doc.department, self.dept)

    def test_document_status(self):
        self.assertEqual(self.doc.status, 'ACTIVE')
        self.doc.status = 'ARCHIVED'
        self.doc.save()
        self.assertEqual(self.doc.status, 'ARCHIVED')