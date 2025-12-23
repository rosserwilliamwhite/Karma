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


card_map = [2, 3, 4, 5, 6, 7, 8, 9, 'J', 'Q', 'K', 'A', 10]
card_index = { val: i for i, val in enumerate(card_map)}


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

# someone goes first



def go(deck, discard, player):
    # always
    fail = 0
    inplay = player['hand'] if player['hand'] else player['known'] if player['known'] else player['unknown']
    
    if not inplay:
        print('Won')
        sys.exit()


    if discard == []:
        discard.append(inplay[0])
        inplay.pop(0)
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
                return
        else:
            print('won')
            sys.exit()

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
                return

    # if a quad discard and go again
    if len(discard) > 3:
        if discard[-4:] == discard[-1] * 4:
            discard.clear()
            go(deck, discard, player)

    # if a ten clear discard and go again
    if discard[-1] == card_index[10]:
        discard.clear()
        go(deck, discard, player)

    # fill cards otherwise
    while len(player['hand']) < 3 and deck != []:
        player['hand'].append(deck.pop(0))

    player['hand'].sort()

turn = 0
while turn < 1000:
    # take turns
    for p, player in enumerate(players):
        print(f'Player {p}') 
        print(f'Hand: {player['hand']} Known: {player['known']}')
        go(deck, discard, player)
        print('Discard:')
        print(discard)
        turn += 1

