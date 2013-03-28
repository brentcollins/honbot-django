import requests
import zipfile
import match
import codecs
import log_parse
from os import remove, path
from django.conf import settings

directory = settings.MEDIA_ROOT


def checkfile(match_id):
    """
    check if match has been parsed before returns bool
    """
    if path.exists(directory + str(match_id) + '.log'):
        return True
    else:
        return False


def get_chat(match_id):
    """
    handles the initial download/check of the .log file
    """
    # get proper url and change to .zip use match first or backup plan with php (slow)
    if not checkfile(match_id):
        if match.checkfile(match_id):
            url = match.get_download(match_id)
            url = url[:-9] + 'zip'
        else:
            try:
                r = requests.get('http://replaydl.heroesofnewerth.com/replay_dl.php?file=&match_id=' + match_id, timeout=2)
                url = r.url[:-9] + 'zip'
            except:
                return None
        # download file
        r = requests.get(url)
        with open(directory + str(match_id)+".zip", "wb") as code:
            code.write(r.content)
        z = zipfile.ZipFile(directory + str(match_id) + '.zip')
        z.extract(z.namelist()[0], directory)
        z.close()
        # cleanup zip
        remove(directory + str(match_id) + '.zip')
    return parse_log(match_id)


def parse_log(match_id):
    """
    damn codecs... open the file already and parse it
    """
    logfile = codecs.open(directory + 'm' + match_id + '.log', encoding='utf-16-le', mode='rb').readlines()
    logfile.pop(0)
    chatter = []
    for line in logfile:
            for word in line.split():
                try:
                    methodToCall = getattr(log_parse, word)
                    chatter.append(methodToCall(line))
                    break
                except AttributeError:
                    #print "Error: " + word + " does not have a function. Match:" + match_id
                    break
    return chatter
