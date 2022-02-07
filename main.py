import json
import Tracker


if __name__ == '__main__':

    with open("./config.json", "r") as config_file:
        config = json.load(config_file)

    saves_file_path = config["saves"]

    tracker = Tracker.Tracker(saves_file_path)
    print(tracker.get_advancements_file_json())