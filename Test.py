# %% import libraries
import pickle
import os
import pandas as pd
from Data.load_df import load_raw
from Extract.Extract_Data import *
import glob
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def clean_cities(x):
    '''
    DOCSTRING
    '''
    if len(x.split(',')) > 1:
        print(x.split(',')[-2].strip())
        return x.split(',')[-2].strip()
    print(x.strip())
    return x


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
team_df = pd.read_csv('./Data/Dictionaries/Team_Info.csv')
standings_df = load_raw('./Data/Updated/Standings')
standings_2 = pd.merge(left=standings_df, right=team_df, on='Team')
# %%
leagues = [
        'premier_league', 'primera_division',
        'serie_a', 'ligue_1', 'bundesliga',
        'eredivisie', 'primeira_liga',
        'championship', 'segunda_division',
        'serie_b', 'ligue_2', '2_liga',
        'eerste_divisie', 'segunda_liga'
        ]
country = ['England', 'Spain', 'Italy', 'France', 'Germany', 'Netherlands', 'Portugal',
           'England', 'Spain', 'Italy', 'France', 'Germany', 'Netherlands', 'Portugal']
dict_countries = {x: y for x, y in zip(leagues, country)}
standings_2.drop(['Country'], axis=1, inplace=True)
standings_2['Country'] = standings_2['League'].map(dict_countries)

# %%
team_df = standings_2.drop_duplicates(subset=['Team'])[['Team', 'City', 'Country', 'Stadium', 'Capacity', 'Pitch']]
team_df['City'] = team_df['City'].apply(clean_cities)
dict_team = team_df.set_index('Team').T.to_dict(orient='list')
with open(filename, 'wb') as pickle_out:
    pickle.dump(dict_team, pickle_out)

team_df.to_csv('./Data/Dictionaries/Team_Info.csv', index=False)
# %%
