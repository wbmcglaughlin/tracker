import Tracker


if __name__ == '__main__':
    saves_file_path = "/Users/willmcglaughlin/Applications/MultiMC.app/Data/instances/LAN/.minecraft/saves"

    tracker = Tracker.Tracker(saves_file_path)
    print(tracker.get_advancements_file_json())