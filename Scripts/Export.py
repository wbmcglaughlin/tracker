import csv
import pandas as pd


def export_advancements_to_csv(advancements_list, uncompleted_advancements, progress_advancements,
                               completed_advancements):
    total_advancements_len = len(advancements_list)
    print(f'Completed Advancements:   {len(completed_advancements)}/{total_advancements_len}\n'
          f'Progress Advancements:    {len(progress_advancements)}/{total_advancements_len}\n'
          f'Uncompleted Advancements: {len(uncompleted_advancements)}/{total_advancements_len}\n')

    df = pd.DataFrame({'uncompleted': uncompleted_advancements +
                                      [None] * (total_advancements_len - len(uncompleted_advancements)),
                       'progress': progress_advancements +
                                   [None] * (total_advancements_len - len(progress_advancements)),
                       'completed': completed_advancements +
                                    [None] * (total_advancements_len - len(completed_advancements))})

    df.to_csv("./advancements.csv", index=False)
