from django.core.management.base import BaseCommand
from django.urls import get_resolver

class Command(BaseCommand):
    help = 'Mostrar todas las URLs del proyecto'

    def handle(self, *args, **kwargs):
        urls = get_resolver().url_patterns
        for url in urls:
            self.stdout.write(str(url))