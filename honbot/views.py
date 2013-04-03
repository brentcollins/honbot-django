from django.shortcuts import render_to_response
from django.template import Context, loader
from django.http import HttpResponse
import match
import player
import api_call
import chat


def v404(request):
    return render_to_response('error.html')


def home(request):
    return render_to_response('home.html')


def chat_view(request, match_id):
    logs = chat.get_chat(match_id)
    if logs is not None:
        t = loader.get_template('chat.html')
        c = Context({'logs': logs})
        return HttpResponse(t.render(c))
    else:
        t = loader.get_template('error.html')
        c = Context({'id': match_id})
        return HttpResponse(t.render(c))


def match_view(request, match_id):
    mid = int(match_id)
    stats = match.match(mid)
    if stats is not None:
        t = loader.get_template('match.html')
        c = Context({'match_id': mid, 'stats': stats})
        return HttpResponse(t.render(c))
    else:
        t = loader.get_template('error.html')
        c = Context({'id': match_id})
        return HttpResponse(t.render(c))


def history(request, name):
    url = '/player_statistics/ranked/nickname/' + name
    data = api_call.get_json(url)
    if data is not None:
        statsdict = data
        s = player.player_math(statsdict)
        ### Get Match history ### api.heroesofnewerth.com/match_history/ranked/accountid/123456/?token=yourtoken
        url = '/match_history/ranked/nickname/' + name
        data = api_call.get_json(url)
        history = []
        if data is not None:
            history = match.recent_matches(data, 25)
        ### Get Match History Data ###
        history_detail = player.match_history_data(history, s['id'])
        ### deliver to view ###
        t = loader.get_template('history.html')
        c = Context({'nick': name, 'stats': s, 'mdata': history_detail})
        return HttpResponse(t.render(c))
    else:
        t = loader.get_template('error.html')
        c = Context({'id': name})
        return HttpResponse(t.render(c))


def players(request, name):
    """
    controls the player show
    """
    while "undefined" in name:
        name = name[:-10]
    url = '/player_statistics/ranked/nickname/' + name
    data = api_call.get_json(url)
    if data is not None:
        statsdict = data
        s = player.player_math(statsdict)
        ### Get Match history ### api.heroesofnewerth.com/match_history/ranked/accountid/123456/?token=yourtoken
        url = '/match_history/ranked/nickname/' + name
        data = api_call.get_json(url)
        history = []
        if data is not None:
            history = match.recent_matches(data, 9)
        ### Get Match History Data ###
        history_detail = player.match_history_data(history, s['id'])
        ### deliver to view ###
        t = loader.get_template('player.html')
        c = Context({'nick': name, 'stats': s, 'mdata': history_detail})
        return HttpResponse(t.render(c))
    else:
        t = loader.get_template('error.html')
        c = Context({'id': name})
        return HttpResponse(t.render(c))
