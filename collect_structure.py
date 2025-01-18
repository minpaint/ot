import os
from pathlib import Path

def collect_project_paths(base_dir: Path, ignore_patterns: set = None) -> dict:
    """
    Собирает пути файлов и папок в проекте, исключая служебные файлы/директории

    Args:
        base_dir: Базовая директория проекта
        ignore_patterns: Паттерны для игнорирования файлов/папок

    Returns:
        dict: Словарь с путями {'directories': [...], 'files': [...]}
    """
    if ignore_patterns is None:
        ignore_patterns = {
            # Служебные директории
            '__pycache__',
            '.git',
            '.idea',
            '.vscode',
            'venv',
            'env',
            'node_modules',
            # Служебные файлы
            '.gitignore',
            '.env',
            '.DS_Store',
            'desktop.ini',
            # Временные файлы
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '.Python',
            '*.so',
            # Кэш и логи
            '*.log',
            '*.sqlite3',
            '*.db',
            # Компилированные файлы
            '*.mo',
            '*.pot',
            # Локальные настройки
            'local_settings.py'
        }

    project_paths = {
        'directories': [],
        'files': []
    }

    try:
        for root, dirs, files in os.walk(base_dir):
            # Фильтруем директории
            dirs[:] = [d for d in dirs if not any(
                pattern in d for pattern in ignore_patterns if '*' not in pattern
            )]

            # Добавляем отфильтрованные директории
            for dir_name in dirs:
                dir_path = Path(root) / dir_name
                rel_path = dir_path.relative_to(base_dir)
                project_paths['directories'].append(str(rel_path))

            # Фильтруем и добавляем файлы
            for file_name in files:
                # Пропускаем файлы по паттернам
                if any(file_name.endswith(pattern.replace('*', ''))
                       for pattern in ignore_patterns if '*' in pattern):
                    continue

                if any(pattern in file_name
                       for pattern in ignore_patterns if '*' not in pattern):
                    continue

                file_path = Path(root) / file_name
                rel_path = file_path.relative_to(base_dir)
                project_paths['files'].append(str(rel_path))

        # Сортируем пути для удобства
        project_paths['directories'].sort()
        project_paths['files'].sort()

        return project_paths

    except Exception as e:
        print(f"Ошибка при сборе путей проекта: {str(e)}")
        return project_paths


def print_project_structure(paths: dict):
    """
    Выводит структуру проекта в консоль

    Args:
        paths: Словарь с путями проекта
    """
    print("\nСтруктура проекта:")
    print("\nДиректории:")
    for dir_path in paths['directories']:
        print(f"  📁 {dir_path}")

    print("\nФайлы:")
    for file_path in paths['files']:
        print(f"  📄 {file_path}")


def save_project_structure(paths: dict, output_file: str = 'project_structure.txt'):
    """
    Сохраняет структуру проекта в файл

    Args:
        paths: Словарь с путями проекта
        output_file: Имя файла для сохранения
    """
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("Структура проекта\n\n")

            f.write("Директории:\n")
            for dir_path in paths['directories']:
                f.write(f"  {dir_path}\n")

            f.write("\nФайлы:\n")
            for file_path in paths['files']:
                f.write(f"  {file_path}\n")

        print(f"\nСтруктура проекта сохранена в файл: {output_file}")

    except Exception as e:
        print(f"Ошибка при сохранении структуры проекта: {str(e)}")


def main():
    # Получаем текущую директорию
    base_dir = Path.cwd()

    print(f"Сканирование директории: {base_dir}")

    # Собираем пути
    project_paths = collect_project_paths(base_dir)

    # Выводим в консоль
    print_project_structure(project_paths)

    # Сохраняем в файл
    save_project_structure(project_paths)


if __name__ == "__main__":
    main()