from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
                          urlencode(
                              OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200')),
                                          access_token=response['access_token'],
                                          v=5.131)), None))

    resp = requests.get(api_url)
    if resp.status_code != 200:
        return
    data = resp.json()['response'][0]
    data_sex = {
        1: UserProfile.FEMALE,
        2: UserProfile.MALE,
        0: None
    }

    user.userprofile.gender = data_sex[data['sex']]
    if data['about']:
        user.userprofile.about = data['about']

    bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()
    age = timezone.now().date().year - bdate.year

    if data['photo_200']:
        user.userprofile.photo = data['photo_200']

    if age < 100:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.age = age
    user.save()
