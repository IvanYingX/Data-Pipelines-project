# %% import libraries
import pickle
import os
import pandas as pd
from Data.load_df import load_raw
from Extract.Extract_Data import *
import glob
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from Create_Database import create_standings_database


def get_result(x):
    result = x.split('-')
    if len(result) > 1:
        if result[0] > result[1]:
            return 0
        elif result[0] == result[1]:
            return 1
        else:
            return 2
    else:
        return None


df = pd.read_csv('./Data/Results/bundesliga/Results_1990_bundesliga.csv')
teams = list(df['Home_Team'].unique())

list_standings = ['Team', 'Position', 'Points', 'Win',
                  'Draw', 'Lose', 'Win_Home', 'Win_Away',
                  'Draw_Home', 'Draw_Away',
                  'Lose_Home', 'Lose_Away',
                  'Goals_For', 'Goals_Against',
                  'Streak', 'Streak_Home', 'Streak_Away',
                  'Number_Teams', 'Season', 'Round', 'League']
dict_standings = {x: [] for x in list_standings}
df_standings = pd.DataFrame(dict_standings)
df_standings['Team'] = teams
round_1 = df[df['Round'] == 1]
for _, rows in round_1.iterrows():
    df_standings.loc[df_standings['Team']
                     == rows['Home_Team'],
                     'Round'] = rows['Round'] + 1
    df_standings.loc[df_standings['Team']
                     == rows['Away_Team'],
                     'Round'] = rows['Round'] + 1