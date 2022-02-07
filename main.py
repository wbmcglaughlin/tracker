import json
from Scripts.Tracker import Tracker

# meaningless comment

if __name__ == '__main__':

    with open("./Information/config.json", "r") as config_file:
        config = json.load(config_file)

    saves_file_path = config["saves"]

    tracker = Tracker(saves_file_path)
    print(tracker.get_completed_advancements())
    print(tracker.get_progress_advancements())