import re
from hero_id import hero


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
        self.team = []
        self.id = []
        self.psr = []
        self.hero = [None] * 10
        self.items = [[] for i in range(10)]
        self.ability_upgrade = [[] for i in range(10)]

    def finish(self):
        """
        this will do my required math and sorting
        """
        myorder = [None] * 10
        newplayers = [None] * 10
        newitems = [None] * 10
        newteam = [None] * 10
        newability_upgrade = [None] * 10
        newhero = [None] * 10
        newid = [None] * 10
        team1 = []
        name1 = []
        name2 = []
        team2 = []
        for i, p in enumerate(self.psr):
            if self.team[i] == 1:
                team1.append(p)
                name1.append(self.players[i])
            else:
                team2.append(p)
                name2.append(self.players[i])
        count = 0
        while count != 5:
            index = self.players.index(name1[team1.index(max(team1))])
            myorder[index] = count
            count += 1
            team1[team1.index(max(team1))] = 0
        while count != 10:
            index = self.players.index(name2[team2.index(max(team2))])
            myorder[index] = count
            count += 1
            team2[team2.index(max(team2))] = 0
        for i, order in enumerate(myorder):
            newplayers[order] = self.players[i]
            newitems[order] = self.items[i]
            newteam[order] = self.team[i]
            newhero[order] = self.hero[i]
            newid[order] = self.id[i]
            newability_upgrade[order] = self.ability_upgrade[i]
        self.players = newplayers
        self.items = newitems
        self.ability_upgrade = newability_upgrade
        self.team = newteam
        self.hero = newhero
        self.id = newid

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
        psr = int(float(l[-1].split(':')[1]))
        if psr != -1 and len(self.players) != 10:
            name = l[2].split(':')[1][1:-1]
            for letter in name:
                if letter == '[':
                    name = name.split(']')[1]
                else:
                    break
            self.players.append(name)
            self.psr.append(psr)
            self.id.append(int(l[-2].split(':')[1]))
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
        print self.team
        print line
        self.team.append(int(line[-3]))

    def PLAYER_SELECT(self, line):
        """
        PLAYER_SELECT player:6 hero:"Hero_Krixi"
        """
        l = line.split()
        self.hero[int(l[1].split(':')[1])] = hero(l[2].split('"')[1])

    def PLAYER_RANDOM(self, line):
        """
        PLAYER_RANDOM player:5 hero:"Hero_Engineer"
        """
        l = line.split()
        self.hero[int(l[1].split(':')[1])] = hero(l[2].split('"')[1])

    def ITEM_PURCHASE(self, line):
        """
        ITEM_PURCHASE time:0 x:13740 y:13363 z:110 player:3 team:2 item:"Item_LoggersHatchet" cost:225
        """
        l = line.split()
        item = {}
        item['item'] = l[7].split('"')[1]
        item['price'] = int(l[8].split(':')[1])
        item['time'] = int(l[1].split(':')[1])
        self.items[int(l[5].split(':')[1])].append(item)

    def ABILITY_UPGRADE(self, line):
        """
        ABILITY_UPGRADE time:0 x:1662 y:995 z:101 player:1 team:1 name:"Ability_Empath1" level:1 slot:0
        """
        l = line.split()
        a = {}
        a['time'] = int(l[1].split(':')[1])
        ability = l[7].split('"')[1]
        if ability != 'Ability_AttributeBoost':
            ability = int(re.sub("\D", "", ability)[-1:])
        else:
            ability = 5
        a['ability'] = ability
        self.ability_upgrade[int(l[5].split(':')[1])].append(a)
