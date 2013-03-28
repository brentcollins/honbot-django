import requests


def get_chat(match_id):
    try:
        r = requests.get('http://replaydl.heroesofnewerth.com/replay_dl.php?file=&match_id=' + match_id, timeout=2)
    except:
        return None
    url = r.url[:-9] + 'zip'
    return url
