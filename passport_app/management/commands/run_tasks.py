from django.core.management.base import BaseCommand
from passport_app.tasks import tasks

class Command(BaseCommand):
    help = 'Run custom tasks!'

    def handle(self, *args, **options):
        tasks()