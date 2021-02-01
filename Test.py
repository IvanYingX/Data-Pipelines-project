import pickle
import os
import pandas as pd
from Load.load_df import load_raw

RAW_STA_DIR = './Data/Raw_Data/Standings'
df_standings = load_raw(RAW_STA_DIR)
print(len(set(df_standings['Team'])))
print(df_standings.shape)
filename = './Data/Extended_Raw/dict_team.pkl'
if os.path.exists(filename):
    with open(filename, "rb") as f:
        dict_team = pickle.load(f)
print(set(dict_team) - set(df_standings['Team']))
# print(len(df_standings.set_index('Link').T.to_dict('list').keys()))