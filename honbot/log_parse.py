def PLAYER_CHAT(line):
    """
    returns dict of chat line, two types of chat, one before start and after
    works perfect now ladies
    """
    chat = {}
    chat['msg'] = ''
    l = line.split()
    if l[0][0] == 'p':
        chat['player'] = l[0].split(':')[1]
        chat['target'] = l[1].split(':')[1][1:-1]
        chat['time'] = None
        for word in l[2:]:
            chat['msg'] = chat['msg'] + word + ' '
    else:
        chat['time'] = l[0].split(':')[1]
        chat['player'] = l[1].split(':')[1]
        chat['target'] = l[2].split(':')[1][1:-1]
        for word in l[3:]:
            chat['msg'] = chat['msg'] + word + ' '
    chat['msg'] = chat['msg'][5:-2]
    return chat


def PLAYER_CONNECT(line):
    """
    PLAYER_CONNECT player:0 name:"NAMENAMENAME" id:3252583 psr:1522.0000
    returns the player name as I don't believe I need any other data. Players connect in order
    """
    l = line.split()
    return l[2].split(':')[1][1:-1]
