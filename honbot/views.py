from django.shortcuts import render_to_response
from django.template import Context, loader
from django.conf import settings
from honbot import models
from django.http import HttpResponse
import urllib2
import json


def home(request):
    return render_to_response('home.html')


def players(request, name):
    """
    controls the player show
    """
    #url = 'http://api.heroesofnewerth.com/player_statistics/ranked/nickname/' + name + '/?token=' + settings.TOKEN
    #data = urllib2.urlopen(url).read()
    data = ('{"account_id":"3258111","rnk_games_played":"1156","rnk_wins":"591","rnk_losses":"565","rnk_concedes":"497","rnk_concedevotes":"508","rnk_buybacks":"17","rnk_discos":"14","rnk_kicked":"1","rnk_amm_solo_rating":"1500.000","rnk_amm_solo_count":"0","rnk_amm_solo_conf":"0.00","rnk_amm_solo_prov":"0","rnk_amm_solo_pset":"0","rnk_amm_team_rating":"1657.779","rnk_amm_team_count":"1156","rnk_amm_team_conf":"0.00","rnk_amm_team_prov":"1156","rnk_amm_team_pset":"127","rnk_herokills":"4829","rnk_herodmg":"10983948","rnk_heroexp":"5891945","rnk_herokillsgold":"2688387","rnk_heroassists":"8858","rnk_deaths":"5320","rnk_goldlost2death":"1482323","rnk_secs_dead":"798659","rnk_teamcreepkills":"71890","rnk_teamcreepdmg":"27671232","rnk_teamcreepexp":"6586508","rnk_teamcreepgold":"2625687","rnk_neutralcreepkills":"22810","rnk_neutralcreepdmg":"15073572","rnk_neutralcreepexp":"1577750","rnk_neutralcreepgold":"926257","rnk_bdmg":"891580","rnk_bdmgexp":"0","rnk_razed":"764","rnk_bgold":"1398557","rnk_denies":"11424","rnk_exp_denied":"515173","rnk_gold":"8880281","rnk_gold_spent":"8927868","rnk_exp":"14082660","rnk_actions":"4777187","rnk_secs":"2373469","rnk_consumables":"4800","rnk_wards":"2073","rnk_em_played":"0","rnk_level":"28","rnk_level_exp":"40640","rnk_min_exp":"40500","rnk_max_exp":"43399","rnk_time_earning_exp":"2367463","rnk_bloodlust":"85","rnk_doublekill":"501","rnk_triplekill":"51","rnk_quadkill":"2","rnk_annihilation":"0","rnk_ks3":"438","rnk_ks4":"252","rnk_ks5":"149","rnk_ks6":"90","rnk_ks7":"52","rnk_ks8":"24","rnk_ks9":"13","rnk_ks10":"6","rnk_ks15":"1","rnk_smackdown":"53","rnk_humiliation":"5","rnk_nemesis":"7487","rnk_retribution":"75"}')
    statsdict = json.loads(data)
    s = playerMath(statsdict)
    t = loader.get_template('player.html')
    c = Context({'player_id': name, 'stats': s,  'test': statsdict})
    return HttpResponse(t.render(c))


def playerMath(data):
    """
    This will get all the right information for the players view and store it in dict
    returns dict
    """
    stats = {}
    stats['matches'] = data['rnk_games_played'] #matches
    stats['wins'] = int(data['rnk_wins']) #wins
    stats['losses'] = int(data['rnk_losses']) #losses
    stats['mmr'] = int(float(data['rnk_amm_team_rating'])) #mmr
    stats['winpercent'] = str(int(float(stats['wins']) / float(stats['matches']) * 100)) + '%' #win percent
    stats['kills'] = int(data['rnk_herokills'])
    return stats
