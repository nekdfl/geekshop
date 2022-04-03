from django.core.management.base import BaseCommand
from mainapp.management.utils import dumpdb


class Command(BaseCommand):
    """Make dump full db exclude 'auth' model"""

    def handle(self, *app_labels, **options):
        print("Make dump exlude auth user model")
        dumpdb(self,  **options)
