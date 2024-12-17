from bs4 import BeautifulSoup
import requests
from zipfile import ZipFile
import os
import pandas as pd
import json

url = f"https://cricsheet.org/downloads"

LEAGUES = ["ipl", "bbl", "sma", "sat",
           "mlc", "cpl", "psl", "ntb", "lpl", "bpl"]


# for league in LEAGUES:
#     format_url = f"{url}/{league}_json.zip"
#     r = requests.get(format_url)
#     if r.status_code == 200:
#         with open(f"./{league}.zip", 'wb') as zip:
#             zip.write(r.content)

#         with ZipFile(f"{league}.zip", "r") as zip:
#             filenames = zip.namelist()
#             # txt = [x for x in filenames if x.endswith(".txt")]
#             for file in filenames:
#                 with zip.open(file) as zip_file:
#                     content = zip_file.read().decode()
#                 if file.endswith(".txt"):
#                     zip.extract(file, f"./{league}.txt")
#                 print(content)
#                 break
#     break

for league in LEAGUES:
    format_url = f"{url}/{league}_json.zip"

    r = requests.get(format_url)
    if r.status_code == 200:
        with open(f"./data/temp/{league}.zip", 'wb') as zip:
            zip.write(r.content)

    with ZipFile(f"./data/temp/{league}.zip", "r") as zip:
        filenames = zip.namelist()
        # txt = [x for x in filenames if x.endswith(".txt")]
        readme = filenames.index("README.txt")
        with zip.open(filenames[readme]) as zip_file:
            content = zip_file.read().decode()
        
            content_list = content.split("\n")
            meta_content = [x for x in content_list \
                                    if "teams involved in the match." in x][0]
            meta_idx = content_list.index(meta_content)
            print(league, meta_idx)
            content_df = [x.split(" - ") for x in content_list[meta_idx+1:]]
            meta_df = pd.DataFrame(content_df, columns=[
                                    'date', 'team_type', 'league', 'gender', 'cricsheet_id', 'match_teams'])\
                        .replace({None:pd.NA, '':pd.NA}, )\
                        .dropna(how='all', ignore_index=True)
            
            meta_df['date'] = pd.to_datetime(meta_df['date'])
            meta_df = meta_df.sort_values("date", ignore_index=True)
            meta_df.to_csv(f'./data/util/{league}.csv', index=False)



