import random

class Player:
    def __init__(self,  name: str):
        self.name = name
        if self.name not in ['will','bot']:
            raise Exception('Invalid input type!')
        self.hand = {}
        self.hand['private'] = self.hand['public'] = self.hand['hidden'] = []
        self.hmap = ['private', 'public', 'hidden']
        self.win = False
        self.phase = 0

    def inplay(self):
        self.phase = 0 if self.hand['private'] else 1 if self.hand['public'] else 2
        inplay = self.hand[self.hmap[self.phase]]
        if self.phase == 2:
            return [cmap_inv[10]+1] * len(inplay)
        inplay.sort()
        return inplay
    
    @staticmethod
    def move(pile, inplay, movetype: str):
        higher = [i for i, c in enumerate(inplay) if c >= pile[-1]]
        if higher == []: 
            return [0]
        if movetype == 'single':
            return [higher[0]]
        elif movetype == 'multi':
            i = [i for i in higher if inplay[i] == inplay[higher[0]]]
            return i
        
    @staticmethod
    def iseasy(pile):
        easy = pile == []
        if not easy:
            easy = pile[-1] == cmap_inv[2]
        return easy
    
    @staticmethod
    def moveeasy(inplay):
        i = [i for i, c in enumerate(inplay) if c == inplay[0]]
        return i
    
    def botmove(self, pile, inplay):
        if self.phase == 0:
            if Player.iseasy(pile) == True:
                i = Player.moveeasy(inplay)
            else:
                if pile[-1] <= cmap_inv['J']:
                    i = Player.move(pile, inplay, 'multi')
                else:
                    i = Player.move(pile, inplay, 'single')
        elif self.phase == 1:
            if Player.iseasy(pile) == True:
                i = [0]
            else:
                i = Player.move(pile, inplay, 'single')
        elif self.phase == 2:
            i = [0]
        return i
    
    def getbi(self, pile, inplay):
        print(f"Pile: {[cmap[c] for c in pile]}")
        converted_hand = {k: [cmap[c] for c in v] for k, v in self.hand.items()}
        print(converted_hand)
        if self.name == 'will':
            bi_list = input("Input bi separated by spaces: ").split()
            bi_floated = [int(num)-1 for num in bi_list]
            return tuple(bi_floated)
        elif self.name == 'bot':
            i = self.botmove(pile, inplay)
            return (i[0], i[-1])
        

class Karma:
    def __init__(self, names: tuple = ('bot','bot')):
        card_range = list(range(1, 14))
        self.pack = card_range * 4
        random.shuffle(self.pack)  # repeat 0-12 4 times
        self.draw = self.pack[len(names) * 9 :]
        self.deal(names)
        self.pile = []
        self.whosturn = 0
        self.win = False

        global cmap, cmap_inv
        ranks = [3,4,5,6,7,8,9,'J','Q','K','A',2,10]
        cmap = dict(zip(card_range, ranks))
        cmap[card_range[-1]+1] = 'X'
        cmap_inv = {v: k for k, v in cmap.items()}
        self.index = dict(zip(ranks, card_range))

    def deal(self, names):
        self.players = []
        for i, name in enumerate(names):
            player = Player(name)
            player.hand['hidden'] = self.draw[i * 9 : i * 9 + 3]
            shown = self.draw[i * 9 + 3 : i * 9 + 9]
            shown.sort()
            player.hand['private'] = shown[0:3]
            player.hand['public'] = shown[3:6]
            self.players.append(player)

    # Turn methods
    def getplayer(self) -> Player:
        return self.players[self.whosturn]        

    def refill(self):
        player = self.getplayer() 
        while len(player.hand['private']) < 3 and self.draw != []:
            player.hand['private'].append(self.draw[0])
            del self.draw[0]

    def rulebook(self, move) -> str: 
        if move == []:
            return "fail"
        elif len(set(move)) > 1:
            return "fail"

        if self.pile != []:
            last = self.pile[-1]
            if last > move[0] and last != self.index[2]:
                return 'fail'
            
        if self.players[self.whosturn].phase > 0:
            if len(move) > 1:
                return 'fail'
            
        if move[0] == self.index[10]:
            return 'bomb'
        if len(self.pile + move) >= 4:
            if len(set(list(self.pile + move)[-4:])) == 1:
                return 'bomb'
        return "success"

    def nextplayer(self):
        self.whosturn += 1
        self.whosturn = self.whosturn % len(self.players)


    def checkwin(self, player: Player):
        if list(player.hand.values()) == [[],[],[]]:
            self.win = True
            print(f"Player {self.whosturn} won!")

    def referee(self, player: Player, bi: tuple) -> int:
        inplay = player.hand[player.hmap[player.phase]]
        # see what the player wants to do
        move = inplay[bi[0] : bi[1]+1]
        
        print(f"Move: {[cmap[c] for c in move]}")
        
        # check its validity
        outcome = self.rulebook(move)
        print(outcome)
        # do the control
        if outcome == "fail":
            del inplay[bi[0] : bi[1]+1]
            player.hand['private'] += self.pile + move
            self.pile = []
            return

        # successful move
        del inplay[bi[0] : bi[1]+1]
        self.pile += move
        self.refill()
        self.checkwin(player) 
        if outcome == "bomb" and not self.win:
            self.pile = []
            self.turn()        

    def turn(self):
        player: Player = self.getplayer()
        inplay = player.inplay()
        print(f"Player{self.whosturn} turn (phase {player.phase})")
        bi = player.getbi(self.pile, inplay)
        self.referee(player, bi)
        

    # Game control
    def run(self):
        while not self.win:
            self.turn()
            self.nextplayer()

if __name__ == "__main__":
    names = ('bot','bot')
    for i in range(100):
        game = Karma(names)
        game.run()
