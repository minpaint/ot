import pandas as pd
from celery import shared_task
from django.contrib.contenttypes.models import ContentType
from ..models import ImportSession


@shared_task
def handle_import(import_session_id):
    """
    Обработчик загрузки внешних данных
    """
    session = ImportSession.objects.get(id=import_session_id)

    try:
        # Обновляем статус
        session.status = 'processing'
        session.save()

        # Читаем Excel файл
        df = pd.read_excel(session.file.path)
        session.total_rows = len(df)
        session.save()

        # Получаем модель для импорта
        model = session.content_type.model_class()

        # Обрабатываем данные
        errors = []
        processed = 0

        for index, row in df.iterrows():
            try:
                # Обработка данных в зависимости от модели
                data = process_row(model, row)

                # Создаем или обновляем запись
                instance, created = model.objects.update_or_create(
                    **data.get('lookup', {}),
                    defaults=data.get('defaults', {})
                )

                processed += 1
                session.processed_rows = processed
                session.save()

            except Exception as e:
                errors.append({
                    'row': index + 2,  # +2 because Excel starts from 1 and header row
                    'error': str(e),
                    'data': row.to_dict()
                })

        # Сохраняем статус и возможные ошибки
        session.status = 'completed' if not errors else 'failed'
        session.errors = {'errors': errors}
        session.save()

    except Exception as e:
        session.status = 'failed'
        session.errors = {'error': str(e)}
        session.save()


def process_row(model, row):
    """
    Обработка данных строки в зависимости от модели
    """
    model_name = model._meta.model_name

    if model_name == 'organization':
        return process_organization(row)
    elif model_name == 'department':
        return process_department(row)
    elif model_name == 'position':
        return process_position(row)
    elif model_name == 'employee':
        return process_employee(row)
    elif model_name == 'document':
        return process_document(row)

    raise ValueError(f'Неподдерживаемая модель: {model_name}')


def process_organization(row):
    """Обработка данных организации"""
    return {
        'lookup': {
            'full_name': row['Полное наименование']
        },
        'defaults': {
            'short_name': row['Сокращенное наименование'],
            'details_ru': row['Реквизиты на русском'],
            'name_by': row['Наименование на белорусском'],
            'details_by': row['Реквизиты на белорусском']
        }
    }


def process_department(row):
    """Обработка данных подразделения"""
    return {
        'lookup': {
            'name': row['Наименование'],
            'organization__full_name': row['Организация']
        },
        'defaults': {
            'short_name': row['Сокращенное наименование']
        }
    }


def process_position(row):
    """Обработка данных должности"""
    return {
        'lookup': {
            'name': row['Наименование должности'],
            'organization__full_name': row['Организация'],
            'department__name': row['Подразделение']
        },
        'defaults': {
            'division': row['Отдел'],
            'safety_instructions': row['Охрана безопасности'],
            'electrical_safety_group': row['Группа электробезопасности'],
            'internship_period': row['Срок стажировки'],
            'contract_instructions': row['Инструкции договора'],
            'is_safety_responsible': row['Ответственный за ОТ'].lower() == 'да',
            'is_electrical_personnel': row['Электротехнический персонал'].lower() == 'да'
        }
    }


def process_employee(row):
    """Обработка данных сотрудника"""
    return {
        'lookup': {
            'last_name': row['Фамилия'],
            'first_name': row['Имя'],
            'middle_name': row['Отчество'],
            'organization__full_name': row['Организация']
        },
        'defaults': {
            'full_name_dative': row['ФИО в дательном падеже'],
            'birth_date': pd.to_datetime(row['Дата рождения']).date(),
            'department__name': row['Подразделение'],
            'position__name': row['Должность'],
            'is_contractor': row['Внешний работник'].lower() == 'да',
            'address': row['Адрес'],
            'phone': row['Телефон'],
            'email': row['Email']
        }
    }


def process_document(row):
    """Обработка данных документа"""
    return {
        'lookup': {
            'name': row['Название документа'],
            'organization__full_name': row['Организация']
        },
        'defaults': {
            'department__name': row['Подразделение'],
            'approval_date': pd.to_datetime(row['Дата утверждения']).date()
        }
    }