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
        return matches[:results]
    else:
        matches = []
        return matches


def checkfile(match_id):
    """
    check if match has been parsed before returns bool
    """
    if not os.path.exists(directory + str(match_id) + '.json'):
        print match_id
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
    for x in range(0, count):
        match = {}
        match['match_id'] = int(data[0][x]['match_id'])
        players = []
        for j in range(0 + (10 * x), 9 + (10 * x)):
            player = {}
            player['id'] = data[1][j]['account_id']
            player['s1'] = data[1][j]['slot_1']
            player['s2'] = data[1][j]['slot_2']
            player['s3'] = data[1][j]['slot_3']
            player['s4'] = data[1][j]['slot_4']
            player['s5'] = data[1][j]['slot_5']
            player['s6'] = data[1][j]['slot_6']
            player['kills'] = data[2][j]['herokills']
            player['deaths'] = data[2][j]['deaths']
            player['assists'] = data[2][j]['heroassists']
            player['herodmg'] = data[2][j]['herodmg']
            player['hero'] = data[2][j]['hero_id']
            player['win'] = data[2][j]['wins']
            players.append(player)
        match['players'] = players
        match_save(match, match['match_id'])
        print match['match_id']
        print match
    return match


def get_player_from_matches(history, account_id):
    """
    this takes a list of matches and returns that player's stats in that match
    """
    matches = []
    for m in history:
        raw = load_match(m[0])
        for x in raw['players']:
            if int(x['id']) == int(account_id):
                x['match_id'] = m[0]
                x['winloss'] = m[1]
                matches.append(x)
                break
    return matches
