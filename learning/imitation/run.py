from game.KarmaV2 import Karma, Player
import torch
import numpy as np
import logging
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logging.basicConfig(filename='learning/imitation/run.log', level=logging.INFO, filemode='w')
    net = torch.load('learning/imitation/imitation.pt', weights_only=False)
    info = ('bot',net)
    for i in range(100):
        game = Karma(info)
        game.run()