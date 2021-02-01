import pickle
import os
import pandas as pd
from Load.load_df import load_raw

# RAW_RES_DIR = './Data/Raw_Data/Results'
TEAM_DIR = './Data/Extended_Raw/Team_Info.csv'
# df_results = load_raw(RAW_RES_DIR)
df_teams = pd.read_csv(TEAM_DIR)
print(df_teams[df_teams.City.isna() & df_teams.Address.isna()])
print(df_teams[df_teams.City.isna()].head(30))
# for i in range(100):
#     new_dict[i] = dict_match[i]
# df_matches = pd.DataFrame.from_dict(new_dict, orient='index')
# print(df_matches)
# new_df = df_results.iloc[:99]
# df_results = new_df.join(df_matches)