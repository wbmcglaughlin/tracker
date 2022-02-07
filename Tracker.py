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
        return self.get_current_advancements_file_path() + "/" + get_advancement_file_string()

    def get_advancements_file_json(self):
        with open(self.get_advancement_file(), "r") as file:
            advancements = json.load(file)
            return advancements

    @staticmethod
    def get_advancement_file_string():
        return "61d477fb-3c0b-434c-a434-52c9e63fc634.json"
