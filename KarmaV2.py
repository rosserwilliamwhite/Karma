import random
import math
import functools

# long numpy array to store previous cards, phase, hand
# choose which cards to play out of hand

class Player:
    # player has a hand, known and unknown
    def __init__(self):
        self.hand = self.known = self.unknown = []
        self.win = False

    def inplay(self) -> list:
        return self.hand if self.hand else self.known if self.known else self.unknown
    
    def getbi(self) -> tuple:
        # depends on if bot or else
        return (0,0)

class Karma:
    def __init__(self, n_players: int):
        self.pack = random.shuffle(list(range(0,13)) * 4) # repeat 0-12 4 times
        self.draw = self.pack[n_players*9:]
        self.deal(n_players)
        self.discard = []

    def deal(self, n_players) -> None:
        self.players = []
        for i in range(n_players):
            player = Player()
            hand_start = i*9; known_start = i*9+3; unknown_start = i*9+6
            player.hand = self.pack[hand_start:hand_start+2]
            player.known = self.pack[known_start:known_start+2]
            player.unknown = self.pack[unknown_start:unknown_start+2]
            self.players.append(player)

    # Turn methods
    def play(self, player: Player, bi: tuple) -> None:
        inplay = player.inplay()
        ind = [round(bi[0]*len(inplay)), round(bi[1]*len(inplay))]
        # TODO remove players cards
        self.discard = self.discard + inplay[ind[0]:ind[1]] if ind[0] != ind[1] else self.discard
    
    def referee(self, player: Player) -> None:
        if self.discard[-1] > self.discard[-2]:
            player.hand.append(self.discard)
            self.discard = []
        elif player.hand == [] and player.known == [] and player.unknown == []:
            player.win = True
        # TODO other rules

    def governor(self, player: Player, outcome: str) -> str:
        if outcome == 'fail':
            self.fail()
        elif outcome == 'bomb':
            self.bomb()
            # TODO its the same players turn again
        # TODO returns next player, same player or win

    def turn(self, who: int) -> str:
        bi = player.getbi()
        player = self.players(who)
        self.play(self, player, bi)
        outcome = self.referee(self, player)
        return self.governor(self, player, outcome) 
    
    # Game control
    def run(self):
        who = 0
        win = self.turn(who)
        while not win:
            win, who = self.turn(who)


# construct referee  
# should just work by inputing start, stop

game = Karma()
# choose player to go
# get bi
# turn
# repeat

