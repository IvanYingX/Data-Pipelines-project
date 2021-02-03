#%% import libraries
import pickle
import os
import pandas as pd
from Load.load_df import load_raw
from Extract.Extract_Data import *
import glob
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
#%% loading dataframes to update
filename = './Data/Extended_Raw/dict_match.pkl'

if os.path.exists(filename):
    with open(filename, "rb") as f:
        dict_match = pickle.load(f)

print(len(dict_match))

RAW_RES_DIR = './Data/Raw_Data/Results'
df_results = load_raw(RAW_RES_DIR)
print(df_results.shape)