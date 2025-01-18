# Справочник сотрудников

Система управления справочниками сотрудников с иерархической структурой.

## Установка

1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать окружение: `source venv/bin/activate` (Linux) или `venv\Scripts\activate` (Windows)
4. Установить зависимости: `pip install -r requirements/development.txt`
5. Создать файл .env и настроить переменные окружения
6. Выполнить миграции: `python manage.py migrate`
7. Создать суперпользователя: `python manage.py createsuperuser`
8. Запустить сервер: `python manage.py runserver`

## Структура проекта

- `apps/` - приложения проекта
- `config/` - настройки проекта
- `templates/` - шаблоны
- `static/` - статические файлы
- `media/` - загружаемые файлы
- `requirements/` - зависимости проекта