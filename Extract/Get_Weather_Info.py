import os
import os.path
import pandas as pd
import sys
sys.path.append('..')
from Data.load_df import load_raw


def clean_cities(x):
    if len(x.split(',')) > 1:
        return x.split(',')[-2]
    return x


team_df = pd.read_csv('./Data/Dictionaries/Team_Info.csv')
standings_df = load_raw('./Data/Updated/Standings')
standings_2 = pd.merge(left=standings_df, right=team_df, on='Team')
dict_league = standings_2.League.unique().sorted()
team_df['City'] = team_df['City'].apply(clean_cities)
cities = team_df.City.unique()
print(len(cities))
