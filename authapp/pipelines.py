import base64
from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.conf import settings
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'vk-oauth2':
        return

    api_url = urlunparse(('http', 'api.vk.com', 'method/users.get', None,
                          urlencode(
                              OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'photo_200', 'personal')),
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
        photo_reponse = requests.get(data['photo_200'])
        filename = base64.urlsafe_b64encode('user-{user.pk}'.encode('ascii')).decode('ascii')
        path_photo = f'user_avatar/{filename}.jpeg'

        with open(f'{settings.MEDIA_ROOT}/{path_photo}', 'wb') as ph:
            ph.write(photo_reponse.content)

        user.image = path_photo
    if age < 5:
        user.delete()
        raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    user.age = age
    if data['personal']['langs'] and len(data['personal']['langs'][0]) > 0:
        user.userprofile.language = data['personal']['langs'][0]
    user.save()
