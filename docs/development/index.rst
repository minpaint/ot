Руководство разработчика
====================

.. toctree::
   :maxdepth: 2

   architecture
   coding_standards
   testing
   documentation
   contributing

Архитектура проекта
-----------------
Проект построен на Django и следует принципам:

* Модульность
* Расширяемость
* Тестируемость
* Безопасность

Основные компоненты:

1. Core - базовые модели и утилиты
2. Organizations - управление организациями
3. Employees - управление сотрудниками
4. Documents - управление документами
5. API - REST API
6. Frontend - шаблоны и статические файлы

Стандарты кодирования
-------------------
1. Python:

   * PEP 8
   * Type hints
   * Docstrings в формате Google
   * Black для форматирования

2. JavaScript:

   * ESLint
   * Prettier
   * ES6+ синтаксис

3. HTML/CSS:

   * Bootstrap 5
   * BEM методология
   * SCSS

Процесс разработки
----------------
1. Создание ветки::

    git checkout -b feature/new-feature

2. Разработка и тестирование
3. Создание pull request
4. Code review
5. Merge в main

Тестирование
----------
1. Модульные тесты::

    python manage.py test

2. Coverage отчет::

    coverage run manage.py test
    coverage report

3. Линтеры::

    flake8
    black .
    isort .

Документация
----------
1. Docstrings для Python кода
2. JSDoc для JavaScript
3. Sphinx для документации
4. README.md в каждом приложении

Развертывание
-----------
1. Staging::

    make deploy-staging

2. Production::

    make deploy-production

CI/CD
-----
GitHub Actions выполняет:

1. Линтинг
2. Тесты
3. Сборку документации
4. Деплой на staging
5. Деплой на production