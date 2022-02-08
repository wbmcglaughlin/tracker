import csv
import pandas as pd
import openpyxl
import xlsxwriter


def export_advancements_to_csv(advancements_list, results):
    total_advancements_len = len(advancements_list)

    df = pd.DataFrame({'advancements': advancements_list,
                       'result': results})

    writer = pd.ExcelWriter(path="./advancements.xlsx", engine='xlsxwriter')

    df.to_excel(writer, index=False, sheet_name="Advancements")
    df.to_excel(writer, index=False, sheet_name="PP")

    workbook = writer.book
    worksheet = writer.sheets['Advancements']

    uncompleted = workbook.add_format({'bg_color': '#FFC7CE'})
    progress = workbook.add_format({'bg_color': '#FFEB9C'})
    completed = workbook.add_format({'bg_color': '#C6EFCE'})

    worksheet.conditional_format(1, 1, 80, 1, {'type':     'cell',
                                               'criteria': '=',
                                               'value':    0,
                                               'format':   uncompleted})
    worksheet.conditional_format(1, 1, 80, 1, {'type': 'cell',
                                               'criteria': '=',
                                               'value': 1,
                                               'format': progress})
    worksheet.conditional_format(1, 1, 80, 1, {'type': 'cell',
                                               'criteria': '=',
                                               'value': 2,
                                               'format': completed})

    writer.save()
