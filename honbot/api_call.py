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
        count = 0
        try:
            raw = requests.get(url, timeout=0.8)
        except requests.exceptions.Timeout:
            count += 1
            raw = requests.get(url, timeout=2)
        if raw.status_code == 429 and count < 20:
            count += 1
            sleep(0.2)
        elif raw.status_code == 200:
            break
        else:
            return None
    print count
    return raw.json()
