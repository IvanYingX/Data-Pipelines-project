# %% import libraries
import pickle
import os
import pandas as pd
from Data.load_df import load_raw
from Extract.Extract_Data import *
import glob
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
# %% loading dataframes to update
filename = './Data/Dictionaries/dict_team.pkl'
if os.path.exists(filename):
    with open(filename, "rb") as f:
        dict_team = pickle.load(f)
else:
    dict_team = {}

new_columns = ['City', 'Country', 'Stadium',
               'Address', 'Capacity', 'Pitch']

df_team = pd.DataFrame.from_dict(dict_team, orient='index',
                                 columns=new_columns)
df_team.index = df_team.index.set_names(['Team'])
df_team.reset_index(inplace=True)
# %%
df_incomplete = pd.read_csv('Data/Dictionaries/Teams_to_Complete.csv')
# %%
