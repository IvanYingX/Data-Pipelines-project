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
filename = './Data/Extended_Raw/dict_match_2.pkl'
dict_match = {}
if os.path.exists(filename):
    with open(filename, "rb") as f:
        dict_match = pickle.load(f)

# print(len(dict_match))
new_columns = ['Date_New', 'Referee', 'Home_Yellow', 'Home_Red', 'Away_Yellow', 'Away_Red']
df_match = pd.DataFrame.from_dict(dict_match, orient='index', columns=new_columns)
RAW_RES_DIR = './Data/Raw_Data/Results'
df_results = load_raw(RAW_RES_DIR)
df_results_complete = df_results.join(df_match)
df_to_dict = df_results_complete[['Link', 'Date_New', 'Referee', 'Home_Yellow', 'Home_Red', 'Away_Yellow', 'Away_Red']].set_index('Link')
new_dict = df_to_dict.T.to_dict(orient='list')
print(new_dict.keys())
print(len(new_dict))
#%%
filename_2 = './Data/Extended_Raw/dict_match.pkl'
with open(filename_2, 'wb') as pickle_out:
    pickle.dump(new_dict, pickle_out)
# %%
