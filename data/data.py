from game.KarmaV2 import Karma, Player
import logging
logger = logging.getLogger(__name__)
import numpy as np

logging.basicConfig(filename='data/karma.log', level=logging.INFO, filemode='w')

N = 1000000

data = np.zeros((N, 106), dtype=np.uint8)
def process_data(gdata: dict[str,tuple]):
    row = np.zeros(106, dtype=np.uint8)
    for i, v in enumerate(gdata['pile']):
        row[i] = v
    for i, v in enumerate(gdata['inplay'],52):
        row[i] = v
    for i, v in enumerate(gdata['phase'],104):
        row[i] = v
    return row

i = 0
names = ('bot','bot')
for i in range(100000):
    game = Karma(names)
    while not game.win and i < N:
        game.turn()
        row = process_data(game.data)
        data[i,:] = row
        game.nextplayer()
        i += 1
np.savez_compressed('imitation_data.npz',state=data[:,:104],action=data[:,104:])