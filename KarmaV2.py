import random

class Player:
    def __init__(self,  name: str):
        self.name = name
        if self.name not in ['will','bot']:
            print('Invalid input type!')
            quit()
        self.hand = self.known = self.unknown = []
        self.win = False

    def inplay(self):
        inplay = self.hand if self.hand else self.known if self.known else self.unknown
        inplay.sort()
        return inplay

    def getbi(self, pile):
        print(f"Pile: {pile}")
        print(f"In play: {self.inplay()}")
        if self.name == 'will':
            bi_list = input("Input bi separated by spaces: ").split()
            bi_floated = [int(num) for num in bi_list]
            return tuple(bi_floated)
        elif self.name == 'bot':
            i = [i for i, c in enumerate(self.inplay()) if c > pile[-1]]
            i = i[0] if len(i) != 0 else 0
            return (i, i+1)
        

class Karma:
    def __init__(self, names: tuple = ('bot','bot')):
        two = 1
        ten = two + 13
        self.pack = list(range(two, ten)) * 4
        random.shuffle(self.pack)  # repeat 0-12 4 times
        self.draw = self.pack[len(names) * 9 :]
        self.deal(names)
        self.pile = self.oldpile = []
        self.whosturn = 0
        self.win = False

        ranks = [2,3,4,5,6,7,8,9,'J','Q','K','A',10]
        self.index = dict(zip(ranks, list(range(two,ten))))

    def deal(self, names):
        self.players = []
        for i, name in enumerate(names):
            player = Player(name)
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
        self.added = inplay[bi[0] : bi[1]]
        del inplay[bi[0] : bi[1]]
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
        self.refill()
        self.checkwin(player)
        if outcome == "bomb":
            self.pile = []
            self.turn()

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
    names = ('will','bot')
    game = Karma(names)
    game.run()
