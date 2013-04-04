

class Magic:
    def __init__(self, match_id):
        self.date = "FUCK"
        self.time = ''
        self.match_id = match_id
        self.server = ''
        self.version = ''
        self.map = ''
        self.mode = ''
        self.players = []
        self.spectators = []

    def INFO_DATE(self, line):
        """
        [u'\ufeffINFO_DATE', u'date:"2013/30/03"', u'time:"17:14:52"']
        """
        d = line.split()
        self.date = d[1].split(':')[1][1:-1]
        self.time = d[2].split('"')[1]

    def INFO_SERVER(self, line):
        """
        INFO_SERVER name:"USE 21"
        """
        self.server = line.split('"')[1]

    def INFO_GAME(self, line):
        """
        INFO_GAME name:"Heroes of Newerth" version:"3.0.6.0"
        """
        self.version = line.split('"')[-2]

    def INFO_MAP(self, line):
        """
        INFO_MAP name:"caldavar" version:"0.0.0"
        """
        self.map = line.split('"')[1]

    def INFO_SETTINGS(self, line):
        """
        INFO_SETTINGS mode:"Mode_Normal" options:"Option_None"
        """
        self.mode = line.split('"')[1]

    def PLAYER_CHAT(self, line):
        """
        returns dict of chat line, two types of chat, one before start and after
        works perfect now ladies
        """
        pass

    def PLAYER_CONNECT(self, line):
        """
        PLAYER_CONNECT player:0 name:"NAMENAMENAME" id:3252583 psr:1522.0000
        spectators too
        PLAYER_CONNECT time:1617600 player:13 name:"[bMcE]Smexystyle`" id:7399320 psr:-1.0000
        """
        l = line.split()
        if len(l) == 5:
            name = l[2].split(':')[1][1:-1]
            for letter in name:
                if letter == '[':
                    name = name.split(']')[1]
                else:
                    break
            self.players.append(name)
        else:
            name = l[3].split(':')[1][1:-1]
            for letter in name:
                if letter == '[':
                    name = name.split(']')[1]
                else:
                    break
            self.spectators.append(name)

    def PLAYER_TEAM_CHANGE(self, line):
        """
        PLAYER_TEAM_CHANGE player:0 team:1
        """
