import gspread
import pandas
from oauth2client.service_account import ServiceAccountCredentials
from gspread_dataframe import set_with_dataframe
from gspread_formatting import *
import json

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


class CellColor:
    def __init__(self):
        self.RED = Color(0.96, 0.73, 0.48)
        self.ORANGE = Color(0.9, 0.96, 0.48)
        self.GREEN = Color(0.56, 0.95, 0.48)


# todo: fix to many requests error
class Sheet:
    def __init__(self, name, players):
        self.name = name
        self.players = players
        self.scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                      "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        self.creds = ServiceAccountCredentials.from_json_keyfile_name("cloud-auth.json", self.scope)
        self.client = gspread.authorize(self.creds)
        self.CellColor = CellColor()

    # Create the Google sheet (only want to do if it doesn't already exist)
    def create_tracker_sheet(self, data_frame: pandas.DataFrame):
        if self.client.open(self.name):
            ss = self.client.open(self.name)
        else:
            ss = self.client.create(self.name)  # spreadsheet object

        try:
            with open("./Information/config.json", "r") as file:
                config = json.load(file)
                for user in config["users_email"]:
                    ss.share(user, perm_type='user',
                             role='writer')
        except Exception as e:
            print(e)

        # Populate First Tab
        self.add_formatting(ss.sheet1)
        set_with_dataframe(ss.sheet1, data_frame)

    # Add a worksheet (tab) to the spreadsheet
    def add_worksheet(self, name, progress_list: pandas.DataFrame, index: int):
        ss = self.client.open(self.name)
        try:
            worksheet = ss.add_worksheet(title=name, rows="50", cols="20")
        except:
            print("Worksheet Exists")
            worksheet = ss.get_worksheet(index)

        self.add_formatting(worksheet)
        set_with_dataframe(worksheet, progress_list)

    def update_worksheet(self, tab, data: pandas.DataFrame):
        worksheet = self.client.open(self.name).worksheet(tab)
        set_with_dataframe(worksheet, data)

    def add_formatting(self, worksheet):
        rule1 = ConditionalFormatRule(
            ranges=[GridRange.from_a1_range('A:E81', worksheet)],
            booleanRule=BooleanRule(
                condition=BooleanCondition('NUMBER_EQ', ['0']),
                format=CellFormat(backgroundColor=self.CellColor.RED)
            )
        )
        rule2 = ConditionalFormatRule(
            ranges=[GridRange.from_a1_range('A:E81', worksheet)],
            booleanRule=BooleanRule(
                condition=BooleanCondition('NUMBER_EQ', ['1']),
                format=CellFormat(backgroundColor=self.CellColor.ORANGE)
            )
        )
        rule3 = ConditionalFormatRule(
            ranges=[GridRange.from_a1_range('A:E81', worksheet)],
            booleanRule=BooleanRule(
                condition=BooleanCondition('NUMBER_EQ', ['2']),
                format=CellFormat(backgroundColor=self.CellColor.GREEN)
            )
        )

        rules = get_conditional_format_rules(worksheet)

        rules.clear()
        rules.append(rule1)
        rules.append(rule2)
        rules.append(rule3)
        rules.save()

    # for testing
    def display_advancements_tab(self):
        sheet = self.client.open(self.name).sheet1
        data = sheet.get_all_records()


def excel_style(row, col):
    """ Convert given row and column number to an Excel-style cell name. """
    result = []
    while col:
        col, rem = divmod(col-1, 26)
        result[:0] = LETTERS[rem]
    return ''.join(result) + str(row)
