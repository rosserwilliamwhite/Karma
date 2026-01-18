import random

class Player:
    # TODO add bots and player
    def __init__(self):
        self.hand = self.known = self.unknown = []
        self.win = False

    def inplay(self):
        return self.hand if self.hand else self.known if self.known else self.unknown

    def getbi(self, pile):
        print(f"Pile: {pile}")
        print(f"In play: {self.inplay()}")
        bi_list = input("Input bi separated by spaces: ").split()
        bi_floated = [float(num) for num in bi_list]
        return tuple(bi_floated)

class Karma:
    # TODO initialise from list of player types
    def __init__(self, n_players: int = 2):
        two = 1
        ten = two + 13
        self.pack = list(range(two, ten)) * 4
        random.shuffle(self.pack)  # repeat 0-12 4 times
        self.draw = self.pack[n_players * 9 :]
        self.deal(n_players)
        self.pile = self.oldpile = []
        self.whosturn = 0
        self.win = False

        ranks = [2,3,4,5,6,7,8,9,'J','Q','K','A',10]
        self.index = dict(zip(ranks, list(range(two,ten))))

    def deal(self, n_players):
        self.players = []
        for i in range(n_players):
            player = Player()
            player.unknown = self.draw[i * 9 : i * 9 + 3]
            shown = self.draw[i * 9 + 3 : i * 9 + 9]
            shown.sort()
            player.hand = shown[0:3]
            player.known = shown[3:6]
            self.players.append(player)

    # Turn methods
    def getplayer(self) -> Player:
        return self.players[self.whosturn]

    def play(self, player: Player, bi: tuple):
        # TODO add control for known, unknown (can't choose multiple)
        inplay = player.inplay()
        ind = [round(bi[0] * len(inplay)), round(bi[1] * len(inplay))]
        print(f"Equivalent was {ind}")
        self.added = inplay[ind[0] : ind[1]]
        del inplay[ind[0] : ind[1]]
        print(f"Added: {self.added}")
        self.oldpile = self.pile
        self.pile += self.added

    def refill(self):
        player = self.getplayer()
        if self.draw != [] and len(player.hand) < 3:
            while len(player.hand) < 3:
                player.hand.append(self.draw[0])
                del self.draw[0]

    def rulebook(self) -> str:
        if self.added == []:
            return "fail"
        elif len(set(self.added)) > 1:
            return "fail"

        if self.oldpile != []:
            if self.oldpile[-1] > self.added[0]:
                return 'fail'
            
        if self.pile[-1] == self.index[10]:
            return 'bomb'
        if len(self.pile) >= 4:
            if len(set(self.pile[-4:])) == 1:
                return 'bomb'
        return "success"

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
        self.refill()
        self.checkwin(player)

    def turn(self):
        print(f"Player{self.whosturn} turn")
        player: Player = self.getplayer()
        bi = player.getbi(self.pile)
        self.play(player, bi)
        outcome = self.rulebook()
        self.referee(player, outcome)
        self.nextplayer()

    # Game control
    def run(self):
        while not self.win:
            self.turn()

if __name__ == "__main__":
    game = Karma()
    game.run()
