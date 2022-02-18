import json
import os
import multiprocessing
from Scripts.Tracker import Tracker


if __name__ == '__main__':
    os.chdir("/Users/willmcglaughlin/PycharmProjects/AllAdvancementsTracker")

    multiprocessing.freeze_support()

    with open("./Information/config.json", "r") as config_file:
        config = json.load(config_file)

    saves_file_path = config["saves"]

    tracker = Tracker(saves_file_path)
    tracker.start()


