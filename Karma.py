# Pure python?
import random

# forget about which card to play
# How much of the lowest should they play?
# 1 of 2 and face cards



def go_bot1(deck, discard, player):
    ''' Dummy bot, just plays the most of the lowest ranking card '''
    # always
    fail = 0
    inplay = player['hand'] if player['hand'] else player['known'] if player['known'] else player['unknown']
    
    if not inplay:
        return 1


    if discard == []:
        # play the most of the lowest card
        lowest = inplay[0]
        indices = [i for i, card in enumerate(inplay) if card == lowest]
        discard += inplay[indices[0]:indices[-1]+1]
        del inplay[indices[0]:indices[-1]+1]
    else:
        # play the most of the next highest card
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

    # if a quad discard and go again
    if len(discard) > 3:
        if discard[-4:] == [discard[-1]] * 4:
            discard.clear()
            # fill cards otherwise
            while len(player['hand']) < 3 and deck != []:
                player['hand'].append(deck.pop(0))

            player['hand'].sort()
            win = go_bot1(deck, discard, player)
            if win:
                return 1

    # if a ten clear discard and go again
    if discard[-1] == card_index[10]:
        discard.clear()
        # fill cards otherwise
        while len(player['hand']) < 3 and deck != []:
            player['hand'].append(deck.pop(0))

        player['hand'].sort()
        win = go_bot1(deck, discard, player)
        if win:
            return 1
    
    # fill cards otherwise
    while len(player['hand']) < 3 and deck != []:
        player['hand'].append(deck.pop(0))

    player['hand'].sort()

def go_bot2(deck, discard, player):
    ''' Ensure that twos are played less often '''
    # always
    fail = 0
    inplay = player['hand'] if player['hand'] else player['known'] if player['known'] else player['unknown']
    
    if not inplay:
        return 1

    if discard == []:
        # play the most of the lowest card
        lowest = inplay[0]
        if lowest == 0:
            # ensure that 2 is not played
            # find the next highest card that isn't a zero
            # find the first card that isn't a zero
            nonzeros = [i for i, card in enumerate(inplay) if card != 0]
            lowest = nonzeros[0]

        indices = [i for i, card in enumerate(inplay) if card == lowest]
        discard += inplay[indices[0]:indices[-1]+1]
        del inplay[indices[0]:indices[-1]+1]
    else:
        # play the most of the next highest card
        if discard[-1] != 0:
            greater = [i for i, card in enumerate(inplay) if card >= discard[-1]]
        elif discard == 0:
            # ensure zero is not unecessarily played
            greater = [i for i, card in enumerate(inplay) if card > discard[-1]]
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

    # if a quad discard and go again
    if len(discard) > 3:
        if discard[-4:] == [discard[-1]] * 4:
            discard.clear()
            # fill cards otherwise
            while len(player['hand']) < 3 and deck != []:
                player['hand'].append(deck.pop(0))

            player['hand'].sort()
            win = go_bot2(deck, discard, player)
            if win:
                return 1

    # if a ten clear discard and go again
    if discard[-1] == card_index[10]:
        discard.clear()
        # fill cards otherwise
        while len(player['hand']) < 3 and deck != []:
            player['hand'].append(deck.pop(0))

        player['hand'].sort()
        win = go_bot2(deck, discard, player)
        if win:
            return 1
    
    # fill cards otherwise
    while len(player['hand']) < 3 and deck != []:
        player['hand'].append(deck.pop(0))

    player['hand'].sort()

def go_bot3(deck, discard, player):
    ''' 
    From a mapping find the closest card to play and play it 
    mapping from [2, 3, 4, 5, 6, 7, 8, 9, J, Q, K, A] 
              to [3, 3, 4, 5, 6, 7, 8, 9, J, Q, K, A] then [2, 10]
    
    '''

    # always
    fail = 0
    inplay = player['hand'] if player['hand'] else player['known'] if player['known'] else player['unknown']
    
    if not inplay:
        return 1

    if discard == []:
        # play the most of the lowest card
        lowest = inplay[0]
        if lowest == 0:
            # ensure that 2 is not played
            # find the next highest card that isn't a zero
            # find the first card that isn't a zero
            nonzeros = [i for i, card in enumerate(inplay) if card != 0]
            lowest = nonzeros[0]

        indices = [i for i, card in enumerate(inplay) if card == lowest]
        discard += inplay[indices[0]:indices[-1]+1]
        del inplay[indices[0]:indices[-1]+1]
    else:
        # play the most of the next highest card
        if discard[-1] != 0:
            greater = [i for i, card in enumerate(inplay) if card >= discard[-1]]
        elif discard == 0:
            # ensure zero is not unecessarily played
            greater = [i for i, card in enumerate(inplay) if card > discard[-1]]
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

    # if a quad discard and go again
    if len(discard) > 3:
        if discard[-4:] == [discard[-1]] * 4:
            discard.clear()
            # fill cards otherwise
            while len(player['hand']) < 3 and deck != []:
                player['hand'].append(deck.pop(0))

            player['hand'].sort()
            win = go_bot2(deck, discard, player)
            if win:
                return 1

    # if a ten clear discard and go again
    if discard[-1] == card_index[10]:
        discard.clear()
        # fill cards otherwise
        while len(player['hand']) < 3 and deck != []:
            player['hand'].append(deck.pop(0))

        player['hand'].sort()
        win = go_bot2(deck, discard, player)
        if win:
            return 1
    
    # fill cards otherwise
    while len(player['hand']) < 3 and deck != []:
        player['hand'].append(deck.pop(0))

    player['hand'].sort()

def deal():
    deck = list(range(0,13)) * 4 # repeat 0-12 4 times
    random.shuffle(deck)
    old_deck = deck

    p1 = deck[0:9]
    p2 = deck[9:18]
    deck = deck[18:]
    # initialise hands
    players = [p1, p2]
    for i, player in enumerate(players):
        known = player[0:6]; known.sort()
        unknown = player[6:9]
        player = {'hand': known[0:3], 'known': known[3:6], 'unknown': unknown}
        players[i] = player
    return players, deck

def botbot_game():
    card_map = [2, 3, 4, 5, 6, 7, 8, 9, 'J', 'Q', 'K', 'A', 10]
    global card_index
    card_index = { val: i for i, val in enumerate(card_map)}
    # someone goes first
    wins = []
    for k in range(100):
        print('New Game:')
        players, deck = deal()
        discard = []

        turn = 0
        win = 0
        p = 0
        while turn < 1000 and not win:
            player = players[p]
            # take turns
            print(f'Player {p}') 
            print(f'Hand: {player['hand']} Known: {player['known']}')
            win = go_bot1(deck, discard, player)
            if win:
                # print(f'player {p} won')
                wins.append(p)
            print('Discard:')
            print(discard)
            turn += 1
            p = 0 if p else 1
    print(f'Player 0 won {wins.count(0)/len(wins)*100:.2f}% of the time')

botbot_game()

