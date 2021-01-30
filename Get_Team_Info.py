from Load.load_df import load_raw
import pandas as pd
from Extract.Extract_Data import extract_team_info#
import csv
RAW_STA_DIR = './Data/Standings'
RAW_RES_DIR = './Data/Results'

df_results, df_standings = load_raw(RAW_RES_DIR, RAW_STA_DIR)
# dict_team = extract_team_info(df_standings)
columns = ['Team', 'City', 'Country', 'Stadium', 'Address', 'Capacity', 'Pitch']
# team_df = pd.DataFrame.from_dict(dict_team, orient='index')
# team_df.to_csv("Teams_info.csv")

team_df = pd.read_csv('Teams_info.csv', names=columns, header=0)

print(team_df.head())
dict_l = team_df.set_index('Team').to_dict(orient='list')
print(dict_l)
# print(df_standings['Team'].map(dict_l))