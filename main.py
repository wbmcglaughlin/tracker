import json
import os
from Scripts.Tracker import Tracker


if __name__ == '__main__':
    with open("./Information/config.json", "r") as config_file:
        config = json.load(config_file)

    saves_file_path = config["saves"]

    tracker = Tracker(saves_file_path)
    tracker.start()


