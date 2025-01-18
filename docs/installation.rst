Установка
=========

Требования к системе
------------------
* Python 3.8+
* PostgreSQL 12+
* Git
* virtualenv (рекомендуется)

Подготовка окружения
------------------
1. Создайте виртуальное окружение::

    python -m venv venv

2. Активируйте виртуальное окружение:

   Windows::

    venv\Scripts\activate

   Linux/MacOS::

    source venv/bin/activate

Установка проекта
---------------
1. Клонируйте репозиторий::

    git clone https://github.com/your-company/employee-directory.git
    cd employee-directory

2. Установите зависимости::

    pip install -r requirements.txt

3. Создайте файл .env на основе .env.example::

    cp .env.example .env

4. Отредактируйте .env, указав настройки базы данных и другие параметры.

Настройка базы данных
-------------------
1. Создайте базу данных PostgreSQL::

    createdb employee_directory

2. Примените миграции::

    python manage.py migrate

3. Создайте суперпользователя::

    python manage.py createsuperuser

4. Загрузите начальные данные (опционально)::

    python manage.py loaddata initial_data

Проверка установки
----------------
1. Запустите сервер разработки::

    python manage.py runserver

2. Откройте в браузере http://localhost:8000/

3. Войдите в административный интерфейс http://localhost:8000/admin/

Возможные проблемы
----------------
1. Ошибка подключения к базе данных:

   * Проверьте настройки в .env
   * Убедитесь, что PostgreSQL запущен
   * Проверьте права доступа к базе данных

2. Ошибки при установке зависимостей:

   * Обновите pip: pip install --upgrade pip
   * Установите необходимые системные библиотеки
   * На Windows может потребоваться установка Visual C++ Build Tools

3. Статические файлы не отображаются:

   * Выполните: python manage.py collectstatic
   * Проверьте настройки STATIC_ROOT и STATIC_URL