from django.core.management.base import BaseCommand
from apps.exporter.services import ExportService

class Command(BaseCommand):
    help = 'Экспорт данных в Excel файл'

    def add_arguments(self, parser):
        parser.add_argument('output_path', type=str, help='Путь для сохранения Excel файла')
        parser.add_argument(
            '--type',
            type=str,
            choices=['organization', 'department', 'position', 'employee'],
            required=True,
            help='Тип экспортируемых данных'
        )

    def handle(self, *args, **options):
        output_path = options['output_path']
        content_type = options['type']

        try:
            ExportService.export_data(content_type, output_path)
            self.stdout.write(
                self.style.SUCCESS(f'Данные успешно экспортированы в файл: {output_path}')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка при экспорте: {str(e)}')
            )