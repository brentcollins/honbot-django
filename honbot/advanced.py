import requests
import zipfile
import codecs
import magic
from match import checkfile, get_download
from os import remove, path
from django.conf import settings

directory = settings.MEDIA_ROOT


def main(match_id):
    """
    handles the initial download/check of the .log file
    """
    # get proper url and change to .zip use match first or backup plan with php (slow)
    if path.exists(directory + 'm' + str(match_id) + '.log'):
        return parse(match_id)
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
        return parse(match_id)
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
            return parse(match_id)
        except:
            return None


def parse(match_id):
    logfile = codecs.open(directory + 'm' + match_id + '.log', encoding='utf-16-le', mode='rb').readlines()
    data = magic.Magic(match_id)
    data.INFO_DATE(logfile.pop(0))
    for line in logfile:
        for word in line.split():
            try:
                methodToCall = getattr(data, word)
                methodToCall(line)
                break
            except AttributeError:
                #print "Error: " + word + " does not have a function. Match:" + match_id
                break
    return data
