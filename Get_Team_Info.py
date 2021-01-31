from Load.load_df import load_raw
import pandas as pd
from Extract.Extract_Data import extract_team_info
import os
import pickle
import numpy as np
RAW_STA_DIR = './Data/Raw_Data/Standings'

df_standings =load_raw(RAW_STA_DIR)
filename = './Data/Extended_Raw/dict_team.pkl'
if os.path.exists(filename):
    with open(filename, "rb") as f:
        dict_team = pickle.load(f)
else:
    dict_team = extract_team_info(df_standings)
new_columns = ['City', 'Country', 'Stadium', 'Address', 'Capacity', 'Pitch']

df_team = pd.DataFrame.from_dict(dict_team, orient='index', columns=new_columns)
df_team.index = df_team.index.set_names(['Team'])
df_team.reset_index(inplace=True)
df_standings.merge(df_team, how='left')

df_standings.to_csv('./Data/Extended_Raw/Extended_Raw_Standings.csv')
