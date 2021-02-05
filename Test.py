#%% import libraries
import pickle
import os
import pandas as pd
from Data.load_df import load_raw
from Extract.Extract_Data import *
import glob
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
#%% loading dataframes to update
RES_DIR = './Data/Updated/Results'
STA_DIR = './Data/Updated/Standings'
df_standings = load_raw(STA_DIR)
df_results = load_raw(RES_DIR)
df_team = pd.read_csv('./Data/Dictionaries/Team_Info.csv')
df_match = pd.read_csv('./Data/Dictionaries/Match_Info.csv')
# %%
print(df_standings.shape)
print(df_results.shape)
print(df_team.shape)
print(df_match.shape)
