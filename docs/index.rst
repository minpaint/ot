Employee Directory Documentation
============================

Employee Directory - это система управления сотрудниками и документами организации.

.. toctree::
   :maxdepth: 2
   :caption: Содержание:

   installation
   configuration
   usage/index
   api/index
   development/index
   deployment
   changelog

Возможности
----------
* Управление организациями, подразделениями и должностями
* Учет сотрудников
* Управление документами и контроль ознакомления
* Импорт/экспорт данных
* API для интеграции

Требования
---------
* Python 3.8+
* Django 4.2+
* PostgreSQL 12+

Быстрый старт
------------
1. Установите проект::

    pip install -r requirements.txt

2. Настройте базу данных::

    python manage.py migrate

3. Создайте суперпользователя::

    python manage.py createsuperuser

4. Запустите сервер разработки::

    python manage.py runserver

Индексы и таблицы
---------------
* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`