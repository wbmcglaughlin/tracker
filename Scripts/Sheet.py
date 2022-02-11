from hashlib import new
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import json
from pprint import pprint


class Sheet:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                      "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("cloud-auth.json", self.scope)
        self.client = gspread.authorize(self.creds)

    # Create the Google sheet (only want to do if it doesn't already exist)
    def create_tracker_sheet(self):
        ss = self.client.create(self.name)  # spreadsheet object

        with open("./Information/config.json", "r") as file:
            config = json.load(file)
            for user in config["users_email"]:
                ss.share(user, perm_type='user',
                         role='writer')

        # Populate First Tab
        worksheet = ss.get_worksheet(0)
        advancement_list = []
        dict = {
            self.name: advancement_list}
        for player in range(self.players):
            dict[player] = ['No'] * len(advancement_list)
            
        df = pd.DataFrame(dict)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print(df)

        # Add a tab for the 6 'progress' advancements
        nether_prog_list = []
        ss.add_worksheet("Explore Nether", nether_prog_list)
        mobs_prog_list = []
        ss.add_worksheet("Mobs", mobs_prog_list)
        biomes_prog_list = []
        ss.add_worksheet("Biomes", biomes_prog_list)
        breed_animal_prog_list = []
        ss.add_worksheet("Breed Animals", breed_animal_prog_list)
        food_prog_list = []
        ss.add_worksheet("Food", food_prog_list)
        cats_prog_list = []
        ss.add_worksheet("Cats", cats_prog_list)

    # Add a worksheet (tab) to the spreadsheet
    def add_worksheet(self, name, progress_list):
        ss = self.client.open(self.name)
        worksheet = ss.add_worksheet(title=name, rows="50", cols="20")

        dict = {
            name: progress_list}
        for player in range(self.players):
            dict[player] = ['No'] * len(progress_list)
            
        df = pd.DataFrame(dict)
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
      
    # TODO: update sheet at the proper tab
    def update_tracker_sheet(self, row, content):
        sheet = self.client.open(self.name).worksheet('Explore Nether')
        sheet.delete_rows(row)
        sheet.insert_row(content, row)

    # for testing
    def display_advancements_tab(self):
        sheet = self.client.open(self.name).sheet1
        data = sheet.get_all_records()
        pprint(data)


# new_sheet = Sheet("tester", players=3)

# # new_sheet.display_advancements_tab()

# # header = ['Explore Nether', 1, 2, 3]
# # new_sheet.update_tracker_sheet(1, header)

# new_sheet.create_tracker_sheet()
# nether_list = ['biome 1', 'biome 2', 'biome 3', 'biome 4']
# new_sheet.add_worksheet("Explore Nether 2", nether_list)
                        



# ============ NOTES ===============
# get row: sheet.row_values(row)
# get col: sheet.col_values(col)
# get cell: sheet.cell(1, 2).value
# insert row: sheet.insert_row(list, row number) - pushes everything down doesnt override
# delete row: delete_rows
# update: update_cell(2, 3, value)

