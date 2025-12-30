import random
# long numpy array to store previous cards, phase, hand
# choose which cards to play out of hand

# deal
def deal():
    draw = list(range(0,13)) * 4 # repeat 0-12 4 times
    random.shuffle(draw)
    old_draw = draw

    p1 = draw[0:9]
    p2 = draw[9:18]
    draw = draw[18:]
    # initialise hands
    players = [p1, p2]
    for i, player in enumerate(players):
        known = player[0:6]; known.sort()
        unknown = player[6:9]
        player = {'hand': known[0:3], 'known': known[3:6], 'unknown': unknown}
        players[i] = player
    return players, draw

# construct referee
def referee(bi, draw, discard, players, who):
    # enforce rules
    return draw, discard, players

# should just work by inputing start, stop

# start game
# give hand
# player tries something based on hand
# referee checks play and adjusts accordingly
# win if player has no cards