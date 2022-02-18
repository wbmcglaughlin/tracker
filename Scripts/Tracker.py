import os
import glob
import json
import time
from tqdm import tqdm

import pandas
from tkinter import *
from Scripts.Export import export_advancements_to_csv
from Scripts.Sheet import Sheet
from enum import IntEnum
import pandas as pd


class AdvancementType(IntEnum):
    """
    Advancement status class
    """
    UNCOMPLETED = 0,
    PROGRESS = 1,
    COMPLETED = 2


class Tracker:
    """
    A class that tracks the advancements for a minecraft world
    """
    def __init__(self, saves_file_path: str):
        """
    
        :param saves_file_path: file path where the world saves are located
        """
        self.saves_file_path = saves_file_path
        self.world_name = None
        self.sheet = None
        self.old_ctime = self.get_ctime_list()

        self.is_tracking = False

    def start(self):
        """
        runs the tracker, waits for file change and then updates
        :return:
        """
        self.get_current_advancements_file_path()

        # Create and Populate Google Sheet
        self.sheet = Sheet(self.world_name, self.get_player_count())
        self.sheet.create_tracker_sheet(self.get_advancement_results_df())

        # Add a tab for the 6 'progress' advancements -
        self.sheet.add_worksheet("Explore Nether", self.get_progress_advancement_by_name_df("explore_nether"), 1)
        self.sheet.add_worksheet("Mobs", self.get_progress_advancement_by_name_df("kill_all_mobs"), 2)
        self.sheet.add_worksheet("Biomes", self.get_progress_advancement_by_name_df("adventuring_time"), 3)
        self.sheet.add_worksheet("Breed Animals", self.get_progress_advancement_by_name_df("bred_all_animals"), 4)
        self.sheet.add_worksheet("Food", self.get_progress_advancement_by_name_df("balanced_diet"), 5)
        self.sheet.add_worksheet("Cats", self.get_progress_advancement_by_name_df("complete_catalogue"), 6)

        self.is_tracking = True

        while self.is_tracking:
            adv_df = self.get_advancement_results_df()

            # Update the tracker sheet with the new data
            self.sheet.update_worksheet("Sheet1", adv_df)

            if self.old_ctime == self.get_ctime_list():
                for _ in tqdm(range(20), desc="Waiting For Change"):
                    time.sleep(1)
            else:
                self.sheet.update_worksheet("Explore Nether", self.get_progress_advancement_by_name_df("explore_nether"))
                self.sheet.update_worksheet("Mobs", self.get_progress_advancement_by_name_df("kill_all_mobs"))
                self.sheet.update_worksheet("Biomes", self.get_progress_advancement_by_name_df("adventuring_time"))
                self.sheet.update_worksheet("Breed Animals", self.get_progress_advancement_by_name_df("bred_all_animals"))
                self.sheet.update_worksheet("Food", self.get_progress_advancement_by_name_df("balanced_diet"))
                self.sheet.update_worksheet("Cats", self.get_progress_advancement_by_name_df("complete_catalogue"))

                self.old_ctime = self.get_ctime_list()

                for _ in tqdm(range(60)):
                    time.sleep(1)

    def get_current_advancements_file_path(self):
        """
        returns the latest worlds advancements file path
        :return:
        """
        lst = glob.glob(self.saves_file_path + "/*")
        world_path = max(lst, key=os.path.getctime)
        self.world_name = world_path.split("/")[-1]
        return world_path + "/advancements"

    def get_advancements_files(self):
        """
        returns a list of the players advancements files
        :return:
        """
        return os.listdir(self.get_current_advancements_file_path())

    def get_player_count(self):
        """
        returns a count of the number of players that have joined the world
        :return:
        """
        return len(self.get_advancements_files())

    def get_advancement_file(self, index: int):
        """
        returns player (index)'s advancements
        :param index:
        :return:
        """

        return self.get_current_advancements_file_path() + "/" + self.get_advancements_files()[index]

    def get_advancements_file_json(self, index: int):
        """
        returns the advancements file as a json string
        :param index:
        :return:
        """
        with open(self.get_advancement_file(index), "r") as file:
            advancements = json.load(file)
            return advancements

    def get_all_advancements(self):
        """
        returns a list of all advancements
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
        returns a list of all completed advancements for a player
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
        returns a list of all progress advancements for a player
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
        returns a list of what remaining progress advancement conditions need to be fulfilled
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
        returns a list of all uncompleted advancements (not including progress advancements)
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
        returns a list of advancement results
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

    def get_advancement_results_df(self):
        """
        returns a dataframe with all results
        :return:
        """
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

        adv_df = pd.DataFrame({"advancements": self.get_all_advancements()})

        for idx, res in enumerate(current_results):
            adv_df.insert(idx + 1, f'player: {idx}', res, True)

        adv_df.insert(1 + len(current_results), f'results', adv_status, True)

        return adv_df

    def get_progress_advancement_by_name(self, name: str):
        """
        returns a list of a progress advancements requirements
        :param name:
        :return:
        """
        advancements = self.get_advancements_list()
        progress = None

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["progress"]):
                if str(adv) == name:
                    progress = advancements[section]["progress"][adv]

        return progress

    def get_progress_advancement_by_name_df(self, name: str):
        """
        returns a dataframe containing a progress advancements results
        :param name:
        :return:
        """
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

        for i in range(self.get_player_count()):
            res = []
            for prog in all_progress:
                if len(progress_todo_per_player[i]) == 0:
                    res.append(0)
                else:
                    if prog in progress_todo_per_player[i]:
                        res.append(0)
                    else:
                        res.append(1)

            results.append(res)

        df = pandas.DataFrame({'type': all_progress})

        for idx, res in enumerate(results):
            df.insert(idx + 1, f'player: {idx}', res, True)

        return df

    def get_all_progress_advancements_df(self):
        """
        returns a list of dataframes of all progress advancements
        :return:
        """
        advancements = self.get_advancements_list()
        df = []

        for section in advancements["sections"]:
            for idx, adv in enumerate(advancements[section]["progress"]):
                df.append(self.get_progress_advancement_by_name_df(adv))

        return df

    def get_ctime_list(self):
        lst = glob.glob(self.saves_file_path + "/*")
        return [os.path.getctime(ls) for ls in lst]

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