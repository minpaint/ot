from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.importer.models import ImportSession
import os

class Command(BaseCommand):
    help = 'Очистка временных файлов и старых сессий импорта'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=7,
            help='Удалить файлы старше указанного количества дней'
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)

        # Удаление старых сессий импорта
        old_sessions = ImportSession.objects.filter(created__lt=cutoff_date)
        count = old_sessions.count()

        for session in old_sessions:
            if session.file and os.path.exists(session.file.path):
                os.remove(session.file.path)

        old_sessions.delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'Удалено {count} старых сессий импорта и их файлов'
            )
        )