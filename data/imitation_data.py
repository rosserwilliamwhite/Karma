from game.KarmaV2 import Karma, Player
import logging
logger = logging.getLogger(__name__)
import numpy as np

logging.basicConfig(filename='data/karma.log', level=logging.INFO, filemode='w')

def process_data(gdata: dict[str,tuple]):
    row = np.zeros(107, dtype=np.uint8)
    for i, v in enumerate(gdata['phase']):
        row[i] = v
    for i, v in enumerate(gdata['pile'][::-1],1):
        row[i] = v
    for i, v in enumerate(gdata['inplay'],53):
        row[i] = v
    for i, v in enumerate(gdata['bi'],105):
        row[i] = v
    return row

def main():
    N = 1000000
    data = np.zeros((N, 107), dtype=np.uint8)

    i = 0
    names = ('bot','bot')
    while i < N:
        game = Karma(names)
        while not game.win and i < N:
            game.turn()
            row = process_data(game.data)
            data[i,:] = row
            game.nextplayer()
            i += 1
            
    np.savez_compressed('learning/imitation/imitation_demo.npz',state=data[:,:105],action=data[:,105:])

if __name__ == "__main__":
    main()