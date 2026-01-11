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

    def inplay(self):
        return self.hand if self.hand else self.known if self.known else self.unknown

    def getbi(self, pile):
        print(f'Pile: {pile}')
        print(f'In play: {self.inplay()}')
        bi_list = input("Input bi separated by spaces: ").split()
        bi_floated = [float(num) for num in bi_list]
        return tuple(bi_floated)

class Karma:
    def __init__(self, n_players: int = 2):
        self.pack = list(range(0, 13)) * 4
        random.shuffle(self.pack)  # repeat 0-12 4 times
        self.draw = self.pack[n_players * 9 :]
        self.deal(n_players)
        self.pile = self.oldpile = []
        self.whosturn = 0
        self.win = False

    def deal(self, n_players):
        # TODO debug: players only have two cards
        self.players = []
        for i in range(n_players):
            player = Player()
            hand_start = i * 9; known_start = i * 9 + 3; unknown_start = i * 9 + 6
            player.hand = self.pack[hand_start : hand_start + 2]
            player.known = self.pack[known_start : known_start + 2]
            player.unknown = self.pack[unknown_start : unknown_start + 2]
            self.players.append(player)

    # Turn methods
    def getplayer(self) -> Player:
        return self.players[self.whosturn]

    def play(self, player: Player, bi: tuple):
        # TODO debug behaviour is weird
        inplay = player.inplay()
        ind = [round(bi[0] * len(inplay)), round(bi[1] * len(inplay))]
        del inplay[ind[0] : ind[1]]
        self.added = inplay[ind[0] : ind[1]]
        print(f'Added: {self.added}')
        self.oldpile = self.pile
        self.pile += self.added

    def rulebook(self, player: Player):
        if self.added == []:
            return 'fail'
        elif len(set(self.added)) > 1:
            return 'fail'

        if self.oldpile != []:
            if self.oldpile[-1] > self.added[0]:
                player.hand.append(self.pile)
                self.pile = []
        # TODO other rules 
        return 'success'  
    
    def nextplayer(self):
        self.whosturn = (self.whosturn + 1) % len(self.players)

    def checkwin(self, player: Player):
        if player.hand == [] and player.known == [] and player.unknown == []:
            player.win = True
            print(f"Player {self.whosturn} won!")

    def referee(self, player: Player, outcome: str) -> int:
        print(outcome)
        if outcome == "fail":
            player.hand += self.pile
            self.pile = []
        elif outcome == "bomb":
            self.pile = []
            self.turn()
        # TODO player refill
        self.checkwin(player)
        
    def turn(self):
        player: Player = self.getplayer()
        bi = player.getbi(self.pile)
        self.play(player, bi)
        outcome = self.rulebook(player)
        self.referee(player, outcome)
        self.nextplayer()   

    # Game control
    def run(self):
        while not self.win:
            self.turn()

# construct referee
# should just work by inputing start, stop

game = Karma()
# to check valid play, before checking any other rules check if pile[old_pile_len:] is not all the same
game.run()