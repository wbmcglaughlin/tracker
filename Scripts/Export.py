import csv
import pandas as pd
import openpyxl
from enum import Enum


class AdvancementType(Enum):
    UNCOMPLETED = 0,
    PROGRESS = 1,
    COMPLETED = 2


def export_advancements_to_csv(advancements_list, uncompleted_advancements, progress_advancements,
                               completed_advancements):
    total_advancements_len = len(advancements_list)
    results = [AdvancementType.UNCOMPLETED] * total_advancements_len

    for idx, advancement in enumerate(advancements_list):
        if advancement in progress_advancements:
            results[idx] = AdvancementType.PROGRESS
        elif advancement in completed_advancements:
            results[idx] = AdvancementType.COMPLETED

    df = pd.DataFrame({'advancements': advancements_list,
                       'result': results})

    df.to_excel("./advancements.xlsx", index=False)
