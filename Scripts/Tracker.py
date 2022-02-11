import os
import json
import time

import pandas

from Scripts.Export import export_advancements_to_csv
from Scripts.Sheet import Sheet
from enum import IntEnum
import pandas as pd


class AdvancementType(IntEnum):
    UNCOMPLETED = 0,
    PROGRESS = 1,
    COMPLETED = 2


class Tracker:
    """
    A class that tracks the advancements for a minecraft world

    ...

    Attributes
    ----------
    saves_file_path : str
        file path where the world saves are located
    world_name : str
        world name of current world

    Methods
    -------
    start():
        starts the tracker
    get_current_advancements_file_path():
        returns advancements file path of most recent world
    get_advancements_files():
        returns a list ofz all player's advancement files
    get_advancement_file(index: int):
        returns path to advancement file for given index
    todo continue listing
    """
    def __init__(self, saves_file_path: str):
        self.saves_file_path = saves_file_path
        self.world_name = None
        self.sheet = None

        self.is_tracking = False
        pandas.set_option('display.max_rows', 80)

    def start(self):
        """

        :return:
        """
        self.get_current_advancements_file_path()

        # Create and Populate Google Sheet
        self.sheet = Sheet(self.world_name, 3)
        self.sheet.create_tracker_sheet(self.get_all_advancements())

         # Add a tab for the 6 'progress' advancements -
        self.sheet.add_worksheet("Explore Nether", self.get_all_progress_advancements_df(0))
        self.sheet.add_worksheet("Mobs", self.get_all_progress_advancements_df(1))
        self.sheet.add_worksheet("Biomes", self.get_all_progress_advancements_df(2))
        self.sheet.add_worksheet("Breed Animals", self.get_all_progress_advancements_df(3))
        self.sheet.add_worksheet("Food", self.get_all_progress_advancements_df(4))
        self.sheet.add_worksheet("Cats", self.get_all_progress_advancements_df(5))

        self.is_tracking = True

        while self.is_tracking:
            current_results = []
            for i in range(self.get_player_count()):
                current_results.append(self.get_advancement_results(i))

            results = []
            for i in range(len(self.get_all_advancements())):
                res = []
                for arr in current_results:
                    res.append(arr[i])
                results.append(res)

            adv_status = []
            for res in results:
                if AdvancementType.COMPLETED in res:
                    adv_status.append(AdvancementType.COMPLETED)
                elif AdvancementType.PROGRESS in res:
                    adv_status.append(AdvancementType.PROGRESS)
                else:
                    adv_status.append(AdvancementType.UNCOMPLETED)

            adv_df = pd.DataFrame({"advancements": self.get_all_advancements(),
                                   "results": results,
                                   "status": adv_status})

            print(adv_df.sort_values(by="status"), '\n')

            print(self.get_all_progress_advancements_df())

            self.is_tracking = False

    def get_current_advancements_file_path(self):
        """

        :return:
        """
        self.world_name = "AA -> Stevo + Pablo + Will"# os.listdir(self.saves_file_path)[0]
        return self.saves_file_path + "/" + self.world_name + "/advancements"

    def get_advancements_files(self):
        """

        :return:
        """
        return os.listdir(self.get_current_advancements_file_path())

    def get_player_count(self):
        """

        :return:
        """
        return len(self.get_advancements_files())

    def get_advancement_file(self, index: int):
        """

        :param index:
        :return:
        """

        return self.get_current_advancements_file_path() + "/" + self.get_advancements_files()[index]

    def get_advancements_file_json(self, index: int):
        """

        :param index:
        :return:
        """
        with open(self.get_advancement_file(index), "r") as file:
            advancements = json.load(file)
            return advancements

    def get_all_advancements(self):
        """

        :return:
        """
        advancements = self.get_advancements_list()
        all_advancements = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["advancements"]):
                key = "minecraft:" + section + "/" + adv
                all_advancements.append(key)

        return all_advancements

    def get_completed_advancements(self, index: int):
        """

        :param index:
        :return:
        """
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
        """

        :param index:
        :return:
        """
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
        """

        :param index:
        :return:
        """
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
        """

        :param index:
        :return:
        """
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
        """

        :param index:
        :return:
        """
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

    def get_progress_advancement_by_name(self, name: str):
        advancements = self.get_advancements_list()
        progress = None

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["progress"]):
                if str(adv) == name:
                    progress = advancements[section]["progress"][adv]

        return progress

    def get_progress_advancement_by_name_df(self, name: str):
        all_progress = self.get_progress_advancement_by_name(name)
        results = []

        progress_todo_per_player = []
        for i in range(self.get_player_count()):

            prog_adv = self.get_progress_advancements(i)
            prog_adv_todo = self.get_progress_advancements_todo(i)
            hold = []
            for idx, prog in enumerate(prog_adv):
                if prog.__contains__(name):  # todo - better way to do this
                    hold = prog_adv_todo[idx]

            progress_todo_per_player.append(hold)

        for prog in all_progress:
            res = []
            for i in range(self.get_player_count()):
                if len(progress_todo_per_player[i]) == 0:
                    res.append(0)
                else:
                    if prog in progress_todo_per_player[i]:
                        res.append(0)
                    else:
                        res.append(1)

            results.append(res)

        df = pandas.DataFrame({'type': all_progress,
                               'results': results})

        return df

    def get_all_progress_advancements_df(self):
        advancements = self.get_advancements_list()
        df = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["progress"]):
                df.append(self.get_progress_advancement_by_name_df(adv))

        return df

    @staticmethod
    def get_advancements_list():
        """

        :return:
        """
        with open("./Information/advancements.json", "r") as advancements_file:
            return json.load(advancements_file)

    def export(self, index: int):
        """

        :param index:
        :return:
        """
        aa = self.get_all_advancements()
        res = self.get_advancement_results(index)

        export_advancements_to_csv(aa, res)