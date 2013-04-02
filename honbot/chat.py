import requests
import zipfile
import codecs
from match import checkfile, get_download
from log_parse import PLAYER_CHAT, PLAYER_CONNECT
from os import remove
from django.conf import settings
from time import strftime, gmtime

directory = settings.MEDIA_ROOT


def get_chat(match_id):
    """
    handles the initial download/check of the .log file
    """
    # get proper url and change to .zip use match first or backup plan with php (slow)
    if checkfile(match_id):
        url = get_download(match_id)
        url = url[:-9] + 'zip'
        # download file
        r = requests.get(url)
        if r.status_code == 404:
            return None
        with open(directory + str(match_id)+".zip", "wb") as code:
            code.write(r.content)
        z = zipfile.ZipFile(directory + str(match_id) + '.zip')
        z.extract(z.namelist()[0], directory)
        z.close()
        # cleanup zip
        remove(directory + str(match_id) + '.zip')
        return parse_chat_from_log(match_id)
    else:
        # this method is janky. hence all the 404 checks to back out quickly if things go south
        try:
            r = requests.get('http://replaydl.heroesofnewerth.com/replay_dl.php?file=&match_id=' + match_id, timeout=2)
            if r.status_code == 404:
                return None
            url = r.url[:-9] + 'zip'
            r = requests.get(url)
            if r.status_code == 404:
                return None
            with open(directory + str(match_id)+".zip", "wb") as code:
                code.write(r.content)
            z = zipfile.ZipFile(directory + str(match_id) + '.zip')
            z.extract(z.namelist()[0], directory)
            z.close()
            # cleanup zip
            remove(directory + str(match_id) + '.zip')
            return parse_chat_from_log(match_id)
        except:
            return None


def parse_chat_from_log(match_id):
    """
    damn codecs... open the file already and parse it
    """
    logfile = codecs.open(directory + 'm' + match_id + '.log', encoding='utf-16-le', mode='rb').readlines()
    logfile.pop(0)
    chatter = []
    players = []
    team = []
    # have log_parse access data
    for line in logfile:
        word = line.split()[0]
        if word == "PLAYER_CHAT":
            chatter.append(PLAYER_CHAT(line[12:]))
        elif word == "PLAYER_CONNECT":
            players.append(PLAYER_CONNECT(line))
        elif word == "PLAYER_TEAM_CHANGE":
            if line[-3] == '2':
                team.append('Hellborne')
            else:
                team.append('Legion')
    # validation on player # because of S2
    if chatter[-1]['player'] == 10:
        for player in chatter:
            player['player'] = int(player['player']) - 1
    # set player name and team name. change time from ms to datetime
    for chat in chatter:
        if chat['target'] == "team":
            chat['target'] = team[int(chat['player'])]
        else:
            chat['target'] = "All"
        chat['name'] = players[int(chat['player'])]
        if chat['time'] is not None:
            if int(chat['time']) < 3599999:
                chat['time'] = strftime('%M:%S', gmtime(int(chat['time']) // 1000))
            else:
                chat['time'] = strftime('%H:%M:%S', gmtime(int(chat['time']) // 1000))
        else:
            chat['time'] = "Lobby"
    return chatter
