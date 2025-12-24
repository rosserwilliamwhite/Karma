# Pure python?
import random
import sys

# Initialise
# Organise cards

# Always:
# Quad or ten clear and go again
# On turn place a card
# Lower than previous, pick up

# Phase 1
# If successful turn and hand less than three pick up

# Phase 2
# put down from known hand

# Phase 3
# put down randomly






def go(deck, discard, player):
    # always
    fail = 0
    # fill cards otherwise
    while len(player['hand']) < 3 and deck != []:
        player['hand'].append(deck.pop(0))

    player['hand'].sort()

    inplay = player['hand'] if player['hand'] else player['known'] if player['known'] else player['unknown']
    
    if not inplay:
        return 1


    if discard == []:
        lowest = inplay[0]
        indices = [i for i, card in enumerate(inplay) if card == lowest]
        discard += inplay[indices[0]:indices[-1]+1]
        del inplay[indices[0]:indices[-1]+1]
    else:
        greater = [i for i, card in enumerate(inplay) if card >= discard[-1]]
        # try hand
        if player['hand']: 
            if greater: 
                lowest = player['hand'][greater[0]]
                indices = [i for i, card in enumerate(player['hand']) if card == lowest]
                discard += player['hand'][indices[0]:indices[-1]+1]
                del player['hand'][indices[0]:indices[-1]+1]
            else:
                fail = 1
        # try known
        elif player['known']:
            if greater:
                lowest = player['known'][greater[0]]
                index = player['known'].index(lowest)
                discard.append(player['known'][index])
                del player['known'][index]
            else:
                fail = 1
        elif player['unknown']:
            discard.append(player['unknown'].pop(0))
            # check for fail
            if discard[-2] > discard[-1]:
                player['hand'] += discard
                discard.clear()
                player['hand'].sort()
                return 0
        else:
            return 1

        # check for fail
        if fail:
            # try play a 2 
            if card_index[2] in player['hand']:
                discard.append(card_index[2])
                player['hand'].remove(card_index[2])
            # pick up
            else:
                player['hand'] += discard
                discard.clear()
                player['hand'].sort()
                return 0

    

    # if a quad discard and go again
    if len(discard) > 3:
        if discard[-4:] == [discard[-1]] * 4:
            discard.clear()
            go(deck, discard, player)
            inplay = player['hand'] if player['hand'] else player['known'] if player['known'] else player['unknown']
            if not inplay:
                return 1

    if not discard:
        print('ruhroh')
        print(players[0])
        print(players[1])
        1

    # if a ten clear discard and go again
    if discard[-1] == card_index[10]:
        discard.clear()
        go(deck, discard, player)

    
    return 0



card_map = [2, 3, 4, 5, 6, 7, 8, 9, 'J', 'Q', 'K', 'A', 10]
card_index = { val: i for i, val in enumerate(card_map)}




# someone goes first
wins = []
for k in range(100):
    deck = list(range(0,13)) * 4 # repeat 0-12 4 times
    random.shuffle(deck)
    old_deck = deck

    p1 = deck[0:9]
    p2 = deck[9:18]
    deck = deck[18:]
    discard = []

    # initialise hands
    players = [p1, p2]
    for i, player in enumerate(players):
        known = player[0:6]; known.sort()
        unknown = player[6:9]
        player = {'hand': known[0:3], 'known': known[3:6], 'unknown': unknown}
        players[i] = player
        
    turn = 0
    win = 0
    p = 0
    while turn < 1000 and not win:
        player = players[p]
        # take turns
        print(f'Player {p}') 
        print(f'Hand: {player['hand']} Known: {player['known']}')
        win = go(deck, discard, player)
        if win:
            print(f'player {p} won')
            wins.append(p)
        print('Discard:')
        print(discard)
        turn += 1
        p = 0 if p else 1
print(wins)
