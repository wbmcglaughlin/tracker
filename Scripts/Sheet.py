from hashlib import new
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from pprint import pprint

class Sheet:
  def __init__(self, name):
    self.name = name
    self.scope = ["https://spreadsheets.google.com/feeds","https://www.googleapis.com/auth/spreadsheets","https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    self.creds = ServiceAccountCredentials.from_json_keyfile_name("cloud-auth.json", self.scope)
    self.client = gspread.authorize(self.creds)

  # Create the google sheet (only want to do if it doesn't already exist)
  def create_tracker_sheet(self):
    ss = self.client.create(self.name) # spreadsheet object
    ss.share('tmstephens111@gmail.com', perm_type='user', role='writer') # do this for everyone who needs to see the sheet (or can do manually in sheets)

  # Add a worksheet (tab) to the spreadsheet
  def add_worksheet(self, name, progress_list, players):
    ss = self.client.open(self.name)
    worksheet = ss.add_worksheet(title=name, rows="50", cols="20")

    cols = len(progress_list)
    worksheet.update(f'A2:A{cols + 1}', progress_list) # set the columns TODO: fix this. can't update columns using a list i think

    header = list(range(1, players)) 
    header.insert(0, name) 
    worksheet.update(f'A1:A{players + 1}', header)
  
  # TODO: update sheet at the proper tab
  def update_tracker_sheet(self, row, content):
    sheet = self.client.open(self.name).worksheet('Explore Nether')
    sheet.delete_rows(row)
    sheet.insert_row(content, row)

  # for testing 
  def display_Advancements_tab(self):
    sheet = self.client.open(self.name).sheet1
    data = sheet.get_all_records()
    pprint(data)

new_sheet = Sheet("test")

# new_sheet.display_Advancements_tab()

# header = ['Explore Nether', 1, 2, 3]
# new_sheet.update_tracker_sheet(1, header)

# new_sheet.create_tracker_sheet()
nether_list = ['biome 1', 'biome 2', 'biome 3']
new_sheet.add_worksheet("Explore Nether 2", nether_list, 3)


# get row: sheet.row_values(row)
# get col: sheet.col_values(col)
# get cell: sheet.cell(1, 2).value
# insert row: sheet.insert_row(list, row number) - pushes everything down doesnt override
# delete row: delete_rows
# update: update_cell(2, 3, value)

 # writing a pandas df to sheets
    # df = pd.DataFrame()
    # worksheet.update([df.columns.values.toList()] + df.values.toList())
