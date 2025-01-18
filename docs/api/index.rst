API Reference
============

.. toctree::
   :maxdepth: 2

   models
   views
   serializers
   permissions
   filters

Общая информация
--------------
API построено на Django REST Framework и предоставляет следующие возможности:

* CRUD операции для всех основных моделей
* Фильтрация и поиск
* Пагинация
* Аутентификация по токену
* Документация в формате OpenAPI (Swagger)

Аутентификация
------------
API поддерживает следующие методы аутентификации:

1. Token Authentication::

    Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

2. Session Authentication (для браузерного API)

Примеры использования
------------------
Получение списка организаций::

    GET /api/v1/organizations/
    Authorization: Token YOUR_TOKEN

Создание сотрудника::

    POST /api/v1/employees/
    Authorization: Token YOUR_TOKEN
    Content-Type: application/json

    {
        "organization": 1,
        "department": 2,
        "position": 3,
        "last_name": "Иванов",
        "first_name": "Иван",
        "middle_name": "Иванович",
        "birth_date": "1990-01-01",
        "phone": "+1234567890",
        "email": "ivanov@example.com"
    }

Пагинация
--------
По умолчанию API возвращает по 10 записей на страницу::

    {
        "count": 100,
        "next": "http://example.com/api/v1/employees/?page=2",
        "previous": null,
        "results": [...]
    }

Фильтрация
---------
Поддерживаются следующие параметры фильтрации:

* ?search - полнотекстовый поиск
* ?organization - фильтр по организации
* ?department - фильтр по подразделению
* ?created_after - записи после даты
* ?created_before - записи до даты

Обработка ошибок
--------------
API возвращает стандартные HTTP коды состояния:

* 200 - успешный запрос
* 201 - успешное создание
* 400 - ошибка в запросе
* 401 - не авторизован
* 403 - доступ запрещен
* 404 - не найдено
* 500 - внутренняя ошибка сервера

Ограничения
---------
* Rate limiting: 1000 запросов в час
* Максимальный размер запроса: 10MB
* Таймаут соединения: 30 секунд