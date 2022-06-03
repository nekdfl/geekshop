"""
utils for settings. Some functions for work with settings over enviroment.
"""

import os
from distutils.util import strtobool
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent


def create_env_file(envfilepath):
    with open(envfilepath, 'w+', encoding='utf-8') as envfile:
        print(".env does not exists! Creating it with SECRET_KEY... \n please wait")
        from django.core.management import utils
        new_secret_key = utils.get_random_secret_key()
        secret_key = f"## DJANGO secret key \nSECRET_KEY={new_secret_key}\n"
        settings_tempalte = """#
## django mode settings
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG=False
# set production mode on real server. Read geekshop settigs.py
PRODUCTION=False
##VK OAUTH SETTINGS
#VK OUATH API
#VK_OAUTH2_KEY=
#VK_OAUTH2_SECRET=
## database settings
#DB_NAME=geekshop
#DB_USER=postgres
## email settings
# used in email message for activation url
#DOMAIN_NAME=http:/mysupersite.ru
## django mail settings
#EMAIL_HOST=smtpmailserverdomain.ru
#EMAIL_PORT=465
#EMAIL_HOST_USER=user@domain.ru
#EMAIL_HOST_PASSWORD=
#EMAIL_USE_SSL=True
#EMAIL_TIMEOUT=60
## memcache settings
#MEMCACHE_SERVER = 
#MEMCACHE_PORT =
#cache settings
#CACHE_MIDDLEWARE_SECONDS=120
#CACHE_MIDDLEWARE_KEY_PREFIX='geekshop'
#LOW_CACHE=True
##\n"""
        envfile.write(secret_key)
        envfile.write(settings_tempalte)
        print(".env was created. Check it.")


def get_bool_from_env(key, default_value):
    # env_value = os.environ.get(key, default_value)
    # str_value = strtobool(env_value)
    # bool_value = bool(str_value)
    # return  bool_value
    return bool(strtobool(str(os.environ.get(key, default_value))))


ENV_FILE = os.path.join(BASE_DIR, '.env')
if os.path.exists(ENV_FILE) and os.path.isfile(ENV_FILE):
    load_dotenv(ENV_FILE)
else:
    create_env_file(ENV_FILE)
    load_dotenv(ENV_FILE)
