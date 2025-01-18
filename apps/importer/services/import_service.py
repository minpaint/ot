import pandas as pd
from django.db import transaction
from ..models import ImportSession
from apps.organizations.models import Organization
from apps.departments.models import Department
from apps.positions.models import Position
from apps.employees.models import Employee

class ImportService:
    CONTENT_TYPE_MAPPING = {
        'organization': Organization,
        'department': Department,
        'position': Position,
        'employee': Employee
    }

    @staticmethod
    def create_import_session(data):
        """Создает сессию импорта"""
        return ImportSession.objects.create(
            file=data['file'],
            content_type=data['content_type']
        )

    @staticmethod
    def process_import(import_session_id):
        """Обрабатывает импорт данных"""
        import_session = ImportSession.objects.get(pk=import_session_id)
        import_session.status = 'processing'
        import_session.save()

        try:
            df = pd.read_excel(import_session.file.path)
            total_rows = len(df)
            import_session.total_rows = total_rows
            import_session.save()

            with transaction.atomic():
                for index, row in df.iterrows():
                    try:
                        ImportService._process_row(
                            row, 
                            import_session.content_type
                        )
                        import_session.processed_rows = index + 1
                        import_session.save()
                    except Exception as e:
                        import_session.add_error(index + 1, str(e))

            import_session.status = 'completed'

        except Exception as e:
            import_session.status = 'failed'
            import_session.add_error(0, str(e))

        finally:
            import_session.save()

    @staticmethod
    def _process_row(row, content_type):
        """Обрабатывает одну строку данных"""
        model_class = ImportService.CONTENT_TYPE_MAPPING[content_type]
        data = row.to_dict()

        # Обработка связанных полей
        if 'organization' in data:
            data['organization_id'] = Organization.objects.get(
                short_name=data.pop('organization')
            ).id

        if 'department' in data:
            data['department_id'] = Department.objects.get(
                name=data.pop('department')
            ).id

        if 'position' in data:
            data['position_id'] = Position.objects.get(
                name=data.pop('position')
            ).id

        # Создание или обновление записи
        instance, created = model_class.objects.update_or_create(
            defaults=data,
            **{model_class.IMPORT_KEY_FIELD: data[model_class.IMPORT_KEY_FIELD]}
        )
        return instance

    @staticmethod
    def get_import_template(model_name):
        """Возвращает шаблон для импорта"""
        model_class = ImportService.CONTENT_TYPE_MAPPING[model_name]
        df = pd.DataFrame(columns=model_class.IMPORT_FIELDS)

        # Создаем файл Excel
        output = pd.ExcelWriter('template.xlsx', engine='openpyxl')
        df.to_excel(output, index=False)
        output.save()

        with open('template.xlsx', 'rb') as f:
            content = f.read()

        return content