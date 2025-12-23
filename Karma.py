# Pure python?
import random

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
    
    if discard == []:
        discard.append(player['hand'][0])
        player['hand'].pop(0)
    else:
        # find the index of the first number that is greater than the last in deck
        greater = [i for i, card in enumerate(player['hand']) if card >= discard[-1]]
        if greater != []:
            # put down the lowest card
            lowest = player['hand'][greater[0]]
            indices = [i for i, card in enumerate(player['hand']) if card == lowest]
            discard += player['hand'][indices[0]:indices[-1]+1]
            del player['hand'][indices[0]:indices[-1]+1]
        elif card_index[2] in player['hand']:
            # play a 2 
            discard.append(card_index[2])
            player['hand'].remove(card_index[2])
        else:
            # pick up
            player['hand'] += discard
            discard = []
            return

    # if a quad discard and go again
    if len(discard) > 3:
        if discard[-4:] == discard[-1] * 4:
            discard = []
            go(deck, discard, player)
    # if a ten clear discard and go again
    if discard[-1] == card_index[10]:
        discard = []
        go(deck, discard, player)
    # if unsucessful play, pick up
    # fill cards otherwise
    while len(player['hand']) < 3 and deck != []:
        player['hand'].append(deck[0])
        deck.pop(0)
    player['hand'].sort()


while deck != []:
    # take turns
    for p, player in enumerate(players):
        print(f'Player {p} start')
        print(player['hand'])
        go(deck, discard, player)
        print('Discard:')
        print(discard)
        print(f'Player {p} end')
        print(player['hand'])