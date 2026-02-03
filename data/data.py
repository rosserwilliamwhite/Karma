import game.KarmaV2 as ka
import logging
logger = logging.getLogger(__name__)

logging.basicConfig(filename='karma.log', level=logging.INFO)

names = ('bot','bot')
for i in range(2):
    game = ka.Karma(names)
    game.run()