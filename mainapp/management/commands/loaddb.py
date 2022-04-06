import json
from django.core.management.base import BaseCommand
from mainapp.management.utils import loaddb


class Command(BaseCommand):
    """load db dump"""

    def handle(self, *args, **options):

        loaddb()
