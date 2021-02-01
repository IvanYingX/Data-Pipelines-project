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
ROOT_URL = "https://www.besoccer.com/"
TEST_RES_DIR = './Data/Raw_Data/Results/Results_Raw_1990_2020_bundesliga.csv'
df_results = pd.read_csv(TEST_RES_DIR)
TEST_STA_DIR = './Data/Raw_Data/Standings/Standings_Raw_1990_2020_bundesliga.csv'
df_standings = pd.read_csv(TEST_STA_DIR)
#%% Extracting the current situation of the dataframes
first_year = df_results.Year.min()
final_year = df_results.Year.max()
last_round_df = df_results[df_results['Year'] == final_year].Round.max()
league = df_standings.League.unique()
if len(league) != 1:
    raise ValueError('There is a problem with this csv. There are more than 1 league')
league = league[0]
driver = accept_cookies(year = final_year, league=league)
last_round_final_year = extract_rounds(driver)
#%% Extracting the current actual situation
driver = accept_cookies(year = '', league = league)
current_year = extract_current_year(driver)
current_round = extract_rounds(driver)
driver.quit()



# %%
