import requests
from time import sleep
from django.conf import settings


def get_json(endpoint):
    """
     returns json data for requested digg endpoint
    """
    url = ''.join(['http://api.heroesofnewerth.com', endpoint, '/?token=%s' % settings.TOKEN])
    raw = ''
    while True:
        raw = requests.get(url)
        if raw.status_code == 429:
            sleep(0.3)
        elif raw.status_code == 200:
            break
        else:
            return None
    return raw.json()
