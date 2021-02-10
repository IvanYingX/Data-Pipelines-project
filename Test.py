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
# %%
df_incomplete = pd.read_csv('Data/Dictionaries/Team_Info.csv')
# %%
