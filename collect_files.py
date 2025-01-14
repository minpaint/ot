import os
import sqlite3
from datetime import datetime

def should_skip_directory(dirname):
    """Проверяет, нужно ли пропустить директорию"""
    # Список директорий для пропуска
    skip_dirs = {'venv', '.idea', '.git', '.vs', '.pytest_cache', '__pycache__'}
    return dirname.startswith('.') or dirname in skip_dirs


def read_file_content(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Ошибка чтения файла: {str(e)}"


def get_tables_from_sqlite(db_path):
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Получаем список всех таблиц
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()

        result = []
        for table in tables:
            table_name = table[0]
            result.append(f"\n=== Таблица: {table_name} ===\n")

            # Получаем все данные из таблицы
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()

            # Получаем имена столбцов
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = [col[1] for col in cursor.fetchall()]
            result.append("Columns: " + ", ".join(columns))

            # Добавляем данные
            for row in rows:
                result.append(str(row))

        conn.close()
        return "\n".join(result)
    except Exception as e:
        return f"Ошибка чтения базы данных: {str(e)}"


def main():
    root_dir = r'd:\YandexDisk\OT_online'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    db_path = os.path.join(root_dir, 'db.sqlite3')

    # Создаем директорию для выходных файлов
    output_dir = os.path.join(root_dir, f'content_collection_{timestamp}')
    os.makedirs(output_dir, exist_ok=True)

    # Создаем один файл для вывода
    output_file = os.path.join(output_dir, 'output.txt')

    # Получаем все файлы для анализа
    all_files = []
    for root, dirs, files in os.walk(root_dir):
        dirs[:] = [d for d in dirs if not should_skip_directory(d)]
        for file in files:
            if file != 'db.sqlite3' and not file.endswith('.txt'):
                all_files.append(os.path.join(root, file))

    # Записываем содержимое в один файл
    with open(output_file, 'w', encoding='utf-8') as out_file:
        # Заголовок файла
        out_file.write(f"{'='*50}\n")
        out_file.write(f"СБОРКА ДАННЫХ\n")
        out_file.write(f"{'='*50}\n\n")

        # Добавляем содержимое базы данных
        out_file.write("СОДЕРЖИМОЕ БАЗЫ ДАННЫХ\n")
        out_file.write("=" * 50 + "\n")
        out_file.write(get_tables_from_sqlite(db_path))
        out_file.write("\n\n" + "=" * 50 + "\n\n")

        # Записываем содержимое файлов
        out_file.write(f"СОДЕРЖИМОЕ ФАЙЛОВ\n")
        out_file.write("=" * 50 + "\n")

        for file_path in all_files:
            out_file.write("\n\n" + "=" * 30 + "\n")
            out_file.write(f"ФАЙЛ: {file_path}\n")
            out_file.write("=" * 30 + "\n")
            out_file.write(read_file_content(file_path))

    print(f"Файл создан: {output_file}")


if __name__ == "__main__":
    main()