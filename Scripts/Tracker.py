import os
import json
from Scripts.Export import export_advancements_to_csv
import tkinter
from enum import IntEnum


class AdvancementType(IntEnum):
    UNCOMPLETED = 0,
    PROGRESS = 1,
    COMPLETED = 2


class Tracker:
    def __init__(self, saves_file_path: str):
        self.saves_file_path = saves_file_path
        self.all_advancements = []
        self.completed_advancements = []
        self.progress_advancements = []
        self.progress_advancements_toto = []
        self.uncompleted_advancements = []

    def start(self):
        window = tkinter.Tk()
        window.geometry("500x500")
        window.resizable(0, 0)
        window.title("AA Tracker")

        listbox = tkinter.Listbox(window, height=500, width=500, bg="black", font="Helvetica", fg="white")

        results = self.get_advancement_results()

        for idx, advancement in enumerate(self.get_all_advancements):
            listbox.insert(idx, advancement)
            if results[idx] == AdvancementType.UNCOMPLETED:
                listbox.itemconfig(idx, {'bg': '#ab4e37'})
            elif results[idx] == AdvancementType.PROGRESS:
                listbox.itemconfig(idx, {'bg': '#adaa3d'})
            elif results[idx] == AdvancementType.COMPLETED:
                listbox.itemconfig(idx, {'bg': '#58b038'})

        listbox.pack()
        window.mainloop()

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

    @property
    def get_all_advancements(self):
        advancements = self.get_advancements_list()
        self.all_advancements = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                self.all_advancements.append(key)

        return self.all_advancements

    @property
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

    def get_advancement_results(self):
        aa = self.get_all_advancements
        pa = self.get_progress_advancements
        ca = self.get_completed_advancements

        results = [0] * len(aa)

        for idx, advancement in enumerate(aa):
            if advancement in pa:
                results[idx] = int(AdvancementType.PROGRESS)
            elif advancement in ca:
                results[idx] = int(AdvancementType.COMPLETED)

        return results

    @staticmethod
    def get_advancement_file_string():
        return "61d477fb-3c0b-434c-a434-52c9e63fc634.json"

    @staticmethod
    def get_advancements_list():
        with open("./Information/advancements.json", "r") as advancements_file:
            return json.load(advancements_file)

    def export(self):
        aa = self.get_all_advancements
        res = self.get_advancement_results

        export_advancements_to_csv(aa, res)
