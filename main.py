import json
from Scripts.Tracker import Tracker
from Scripts.Export import export_advancements_to_csv

# meaningless comment

if __name__ == '__main__':

    with open("./Information/config.json", "r") as config_file:
        config = json.load(config_file)

    saves_file_path = config["saves"]

    tracker = Tracker(saves_file_path)

    aa = tracker.get_all_advancements
    ua = tracker.get_uncompleted_advancements
    pa = tracker.get_progress_advancements
    ca = tracker.get_completed_advancements

    export_advancements_to_csv(aa, ua, pa, ca)
