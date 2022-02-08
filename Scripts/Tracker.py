import os
import json


class Tracker:
    def __init__(self, saves_file_path: str):
        self.saves_file_path = saves_file_path
        self.completed_advancements = []
        self.progress_advancements = []
        self.progress_advancements_toto = []
        self.uncompleted_advancements = []

    def get_current_advancements_file_path(self):
        return self.saves_file_path + "/" + os.listdir(self.saves_file_path)[0] + "/advancements"

    def get_advancements_files(self):
        return os.listdir(self.get_current_advancements_file_path())

    def get_advancement_file(self):
        return self.get_current_advancements_file_path() + "/" + self.get_advancement_file_string()

    def get_advancements_file_json(self):
        with open(self.get_advancement_file(), "r") as file:
            advancements = json.load(file)
            return advancements

    @ property
    def get_completed_advancements(self):
        advancements = self.get_advancements_list()
        advancements_file = self.get_advancements_file_json()
        self.completed_advancements = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                if key in advancements_file:
                    if advancements_file[key]["done"]:
                        self.completed_advancements.append(key)

        return self.completed_advancements

    @property
    def get_progress_advancements(self):
        advancements = self.get_advancements_list()
        advancements_file = self.get_advancements_file_json()
        self.progress_advancements = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                if key in advancements_file:
                    if not advancements_file[key]["done"]:
                        self.progress_advancements.append(key)

        return self.progress_advancements

    @property
    def get_progress_advancements_todo(self):
        advancements = self.get_advancements_list()
        advancements_file = self.get_advancements_file_json()
        self.progress_advancements_toto = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                if key in advancements_file:
                    if not advancements_file[key]["done"]:
                        todo = list(advancements[section]["progress"][adv])
                        for criteria_met in advancements_file[key]["criteria"]:
                            if criteria_met in todo:
                                todo.remove(criteria_met)
                                self.progress_advancements_toto.append(todo)

        return self.progress_advancements_toto

    @property
    def get_uncompleted_advancements(self):
        advancements = self.get_advancements_list()
        advancements_file = self.get_advancements_file_json()
        self.uncompleted_advancements = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                if key not in advancements_file:
                    self.uncompleted_advancements.append(key)

        return self.uncompleted_advancements

    @staticmethod
    def get_advancement_file_string():
        return "61d477fb-3c0b-434c-a434-52c9e63fc634.json"

    @staticmethod
    def get_advancements_list():
        with open("./Information/advancements.json", "r") as advancements_file:
            return json.load(advancements_file)

