from Load.load_df import load_raw
import pandas as pd
from Extract.Extract_Data import extract_team_info
import os
import pickle
import numpy as np

STA_DIR = './Data/Updated/Standings'
df_standings = load_raw(STA_DIR) # Load all standings dataframes in a single dataframe
dict_team = extract_team_info(df_standings)

new_columns = ['City', 'Country', 'Stadium', 'Address', 'Capacity', 'Pitch']

df_team = pd.DataFrame.from_dict(dict_team, orient='index', columns=new_columns)
df_team.index = df_team.index.set_names(['Team'])
df_team.reset_index(inplace=True)
df_team.to_csv('./Data/Extended_Raw/Team_Info.csv')
