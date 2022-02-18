import json
import os
import logging
import multiprocessing
from Scripts.Gui import Gui


if __name__ == '__main__':
    os.chdir("/Users/willmcglaughlin/PycharmProjects/AllAdvancementsTracker")

    logging.basicConfig(level=logging.INFO,
                        format='[%(name)s] %(levelname)s - %(message)s')

    gui = Gui(500, 300)
    gui.show()


