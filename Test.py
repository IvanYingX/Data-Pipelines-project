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
df = pd.read_csv('./Data/Dictionaries/Team_Info.csv')
df_no_city = df[df.City.isna()]
print(df_no_city.head(20))
# %%
ROOT = 'https://en.wikipedia.org/wiki/'
URL = ROOT + df_no_city.iloc[1]['Team'].replace(' ','_')
temp_url = urlopen(URL)
temp_bs = BeautifulSoup(temp_url.read(), 'html.parser')
print(temp_bs)
# %%
