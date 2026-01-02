import random
import math
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
def referee(who):
    global discard
    global players
    # enforce rule
    if discard[-1] > discard[-2]:
        # player must pick up the discard
        players[who]['hand'].append(discard)
        discard = []
        return 0
    elif list(players[who].values()) == [[],[],[]]:
        return 1
    
def go(who, bi):
    player = players[who]
    inplay = player['hand'] if player['hand'] else player['known'] if player['known'] else player['unknown'] 
    # start, end maps 0 to 1 to 0 to len(inplay)
    # take floor of decimal 
    bind = [round(bi[0]*len(inplay)), round(bi[1]*len(inplay))]
    discard.append(inplay[bind[0]:bind[1]]) if bind[0] != bind[1] else discard
    

# should just work by inputing start, stop

# start game (deal)
players, draw = deal()
discard = []
# give hand (inplay)

# player tries something based on hand (go)
# referee checks play and adjusts accordingly (referee)
# win if player has no cards (referee)

print(players[0])
go(0,[0,0.3])