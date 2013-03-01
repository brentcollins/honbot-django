from django.http import HttpResponse
from honbot.models import Names
from django.template import Context, loader


def playerShow(request, player_id):
    t = loader.get_template('honbot/playerShow.html')
    c = Context({'player_id': player_id})
    return HttpResponse(t.render(c))