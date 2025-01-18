from django.core.management.base import BaseCommand
from apps.importer.services import ImportService

class Command(BaseCommand):
    help = 'Импорт данных из Excel файла'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к Excel файлу')
        parser.add_argument(
            '--type',
            type=str,
            choices=['organization', 'department', 'position', 'employee'],
            required=True,
            help='Тип импортируемых данных'
        )

    def handle(self, *args, **options):
        file_path = options['file_path']
        content_type = options['type']

        try:
            import_session = ImportService.create_import_session({
                'file': open(file_path, 'rb'),
                'content_type': content_type
            })
            ImportService.process_import(import_session.id)

            self.stdout.write(
                self.style.SUCCESS(f'Импорт успешно завершен. ID сессии: {import_session.id}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при импорте: {str(e)}')
            )