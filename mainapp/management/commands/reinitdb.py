

from time import sleep
from django.conf import settings


from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.db import connections, connection

import os

from mainapp.management.utils import create_authapp_user
from mainapp.management.utils import ask_yn, is_authapp_user_exist
from mainapp.management.utils import dumpdb, loaddb


def make_dump(db_path, **options):
    if os.path.exists(db_path):
        dumpdb(**options)
    else:
        msg = f"! Db {db_path} is not exists. Skip dump step. Continue?"
        if not ask_yn(msg):
            exit()


def delete_db(db_path):
    if os.path.exists(db_path):
        os.remove(db_path)


def restart_db_connection():
    for conn in connections.all():
        conn.close_if_unusable_or_obsolete()


def create_db():
    call_command("makemigrations")
    call_command("migrate")


class Command(BaseCommand):

    def handle(self, *app_labels, **options):

        if not settings.configured:
            settings._setup()

        databases = settings.DATABASES
        if "sqlite" in databases["default"]["ENGINE"]:
            db_path = databases["default"]["NAME"]
            print(db_path)

            msg = """### Warning! ###
This action will delete database"
"Continue?"""

            if ask_yn(msg):
                make_dump(db_path, **options)
                delete_db(db_path)
                restart_db_connection()
                create_db()
                loaddb()

    # if not is_authapp_user_exist("user"):
    #     create_authapp_user("user", "1", "user@test.ru")
