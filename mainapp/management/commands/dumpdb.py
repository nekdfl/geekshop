
from textwrap import indent
from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):

    def handle(self, *app_labels, **options):
        call_command("dumpdata",
                     indent=2,
                     output="fulldb.json",
                     exclude=["auth"])
