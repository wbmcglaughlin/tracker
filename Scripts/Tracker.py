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

    def start(self):
        window = tkinter.Tk()
        window.geometry("500x500")
        window.resizable(0, 0)
        window.title("AA Tracker")

        listbox = tkinter.Listbox(window, height=500, bg="black", font="Helvetica", fg="white")
        results = self.get_advancement_results()

        for idx, advancement in enumerate(self.get_all_advancements()):
            listbox.insert(idx, advancement.replace("minecraft:", ""))
            if results[idx] == AdvancementType.UNCOMPLETED:
                listbox.itemconfig(idx, {'bg': '#ab4e37'})
            elif results[idx] == AdvancementType.PROGRESS:
                listbox.itemconfig(idx, {'bg': '#adaa3d'})
            elif results[idx] == AdvancementType.COMPLETED:
                listbox.itemconfig(idx, {'bg': '#58b038'})

        listbox.pack(anchor="nw")
        window.mainloop()

    def get_current_advancements_file_path(self):
        return self.saves_file_path + "/" + os.listdir(self.saves_file_path)[0] + "/advancements"

    def get_advancements_files(self):
        return os.listdir(self.get_current_advancements_file_path())

    def get_advancement_file(self, index: int):
        return self.get_current_advancements_file_path() + "/" + self.get_advancements_files[index]

    def get_advancements_file_json(self, index: int):
        with open(self.get_advancement_file(index), "r") as file:
            advancements = json.load(file)
            return advancements

    def get_all_advancements(self):
        advancements = self.get_advancements_list()
        all_advancements = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                all_advancements.append(key)

        return all_advancements

    def get_completed_advancements(self, index: int):
        advancements = self.get_advancements_list()
        advancements_file = self.get_advancements_file_json(index)
        completed_advancements = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                if key in advancements_file:
                    if advancements_file[key]["done"]:
                        completed_advancements.append(key)

        return completed_advancements

    def get_progress_advancements(self, index: int):
        advancements = self.get_advancements_list()
        advancements_file = self.get_advancements_file_json(index)
        progress_advancements = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                if key in advancements_file:
                    if not advancements_file[key]["done"]:
                        progress_advancements.append(key)

        return progress_advancements

    def get_progress_advancements_todo(self, index: int):
        advancements = self.get_advancements_list()
        advancements_file = self.get_advancements_file_json(index)
        progress_advancements_toto = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                if key in advancements_file:
                    if not advancements_file[key]["done"]:
                        todo = list(advancements[section]["progress"][adv])
                        for criteria_met in advancements_file[key]["criteria"]:
                            if criteria_met in todo:
                                todo.remove(criteria_met)
                                progress_advancements_toto.append(todo)

        return progress_advancements_toto

    def get_uncompleted_advancements(self, index: int):
        advancements = self.get_advancements_list()
        advancements_file = self.get_advancements_file_json(index)
        uncompleted_advancements = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                if key not in advancements_file:
                    uncompleted_advancements.append(key)

        return uncompleted_advancements

    def get_advancement_results(self, index: int):
        aa = self.get_all_advancements()
        pa = self.get_progress_advancements(index)
        ca = self.get_completed_advancements(index)

        results = [0] * len(aa)

        for idx, advancement in enumerate(aa):
            if advancement in pa:
                results[idx] = int(AdvancementType.PROGRESS)
            elif advancement in ca:
                results[idx] = int(AdvancementType.COMPLETED)

        return results

    @staticmethod
    def get_advancements_list():
        with open("./Information/advancements.json", "r") as advancements_file:
            return json.load(advancements_file)

    def export(self, index: int):
        aa = self.get_all_advancements()
        res = self.get_advancement_results(index)

        export_advancements_to_csv(aa, res)
