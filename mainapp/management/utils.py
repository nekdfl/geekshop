
from authapp.models import User as AuthUser
from django.contrib.auth.models import User as SuperUser
from django.core.management import call_command
from django.conf import settings

FULL_DB_JSON_PATH = "mainapp/fixtures/fulldb.json"


def get_auth_user_model():
    if not settings.configured:
        settings._setup()

    return settings.AUTH_USER_MODEL


def is_authapp_user_exist(login):
    if AuthUser.objects.get(username=login):
        return True
    return False


def create_authapp_user(login, password, email):
    pass
    # print(
    #     f"create authapp user witn login: '{login}' and password: '{password}'")
    # authuser = AuthUser(username=login, email=email, password=password)
    # authuser.save()


def create_super_user(login, password, email):
    print(
        f"create super user witn login: '{login}' and password: '{password}'")
    superuser = SuperUser(username=login, password=password, active=True)
    superuser.save()


def ask_yn(msg):
    return ask(msg) == "y"


def ask(msg, question="y/n: "):
    print(msg)
    answer = input(question)
    return answer


def add_auth_user_excl_list(exclude_list):
    """exclude auth user model from dump"""
    pass
    exclude_list.append(get_auth_user_model())


def dumpdb(**options):
    """make dump of db to fixture"""
    pass
    # call_command("dumpdata",
    #              indent=2,
    #              output=FULL_DB_JSON_PATH,
    #              **options)


def loaddb():
    """load dump to db from fixture"""
    call_command("loaddata", FULL_DB_JSON_PATH)
