import os
import json


directory = 'match/'


def match(match_id):
    return 5


def recent_matches(match_json, results):
    """
    returns specifed number of recent matches and win loss status as bool
    """
    if match_json[0]['win_loss_history'] is not None:
        data = match_json[0]['win_loss_history'].split('|')
        matches = []
        temp = []
        for i in data:
            temp = i.split('/')
            if temp[0] != '':
                if temp[1] == 'W':
                    temp[1] = True
                else:
                    temp[1] = False
                matches.append(temp)
        matches.reverse()
        return matches[:results]
    else:
        matches = []
        return matches


def checkfile(match_id):
    """
    check if match has been parsed before returns bool
    """
    if not os.path.exists(directory + str(match_id) + '.json'):
        return False
    else:
        return True


def match_save(data, match_id):
    """
    save match to directory in json format
    """
    with open(directory + str(match_id) + '.json', 'w') as f:
        json.dump(data, f, ensure_ascii=False)


def load_match(match_id):
    """
    open match from directory and return json
    """
    with open(directory + str(match_id) + '.json', 'rb') as f:
        data = json.load(f)
    return data


def multimatch(data, count):
    """
    pass this multimatch api results and the number of matches. it will parse and save the useful bits
    """
    allmatches = {}
    listomatic = []
    for m in data[0]:
        match = {}
        players = {}
        listomatic.append(int(m['match_id']))
        match['match_id'] = m['match_id']
        match['players'] = players
        allmatches[m['match_id']] = match
    for m in data[2]:
        player = {}
        player['id'] = m['account_id']
        player['kills'] = m['herokills']
        player['deaths'] = m['deaths']
        player['assists'] = m['heroassists']
        player['herodmg'] = m['herodmg']
        player['hero'] = m['hero_id']
        player['win'] = bool(int(m['wins']))
        allmatches[m['match_id']]['players'][m['account_id']] = player
    # for m in data[1]:
    #     player['s1'] = m['slot_1']
    #     player['s2'] = m['slot_2']
    #     player['s3'] = m['slot_3']
    #     player['s4'] = m['slot_4']
    #     player['s5'] = m['slot_5']
    #     player['s6'] = m['slot_6']
    # print allmatches
    #print json.dumps(allmatches)
    for m in listomatic:
        match_save(allmatches[str(m)], m)
    #     match['players'] = players
    #     match_save(match, match['match_id'])
    return match


def get_player_from_matches(history, account_id):
    """
    this takes a list of matches and returns that player's stats in that match
    """
    matches = []
    for m in history:
        temp = {}
        raw = load_match(m[0])
        temp = raw['players'][str(account_id)]
        temp['match_id'] = m[0]
        matches.append(temp)
    return matches
