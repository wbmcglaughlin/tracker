import os
import json


class Tracker:
    def __init__(self, saves_file_path: str):
        self.saves_file_path = saves_file_path

    def get_current_advancements_file_path(self):
        return self.saves_file_path + "/" + os.listdir(self.saves_file_path)[-1] + "/advancements"

    def get_advancements_files(self):
        return os.listdir(self.get_current_advancements_file_path())

    def get_advancement_file(self):
        return self.get_current_advancements_file_path() + "/" + self.get_advancement_file_string()

    def get_advancements_file_json(self):
        with open(self.get_advancement_file(), "r") as file:
            advancements = json.load(file)
            return advancements

    def get_completed_advancements(self):
        advancements = self.get_advancements_list()
        advancements_file = self.get_advancements_file_json()
        for section in advancements["sections"]:
            for adv in advancements[section]:
                key = "minecraft:" + section + "/" + adv
                if key in advancements_file:
                    if advancements_file[key]["done"]:
                        print(key + " : done")
                    else:
                        print(key + " : progress")

    @staticmethod
    def get_advancement_file_string():
        return "61d477fb-3c0b-434c-a434-52c9e63fc634.json"

    @staticmethod
    def get_advancements_list():
        with open("./advancements.json", "r") as advancements_file:
            return json.load(advancements_file)
