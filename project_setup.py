import os


def fix_wsgi():
    """
    Исправляет файл config/wsgi.py, добавляя определение WSGI application.
    """
    wsgi_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config', 'wsgi.py')

    wsgi_content = """
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()
"""
    try:
        with open(wsgi_path, 'w') as f:
            f.write(wsgi_content)
        print(f"Файл {wsgi_path} успешно исправлен.")
    except Exception as e:
        print(f"Ошибка при исправлении файла: {e}")


if __name__ == '__main__':
    fix_wsgi()