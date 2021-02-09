import sys
from os import path
import pandas as pd
import os
import pickle
import numpy as np
import urllib
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from urllib.error import HTTPError, URLError
import re


def get_stadium(row):
    city = row['City']
    capacity = row['Capacity']
    pitch = row['Pitch']
    URL = 'https://en.wikipedia.org' + row['Link_Stadium']
    try:
        temp_url = urlopen(URL)
        temp_bs = BeautifulSoup(temp_url.read(), 'html.parser')
    except HTTPError as err:
        if err.code == 404:
            print(row['Link_Stadium'])
            print('Not found')
    except URLError as err:
        print('Bad Request')
    else:
        info_vcard = temp_bs.find('table', {'class': 'infobox vcard'})
        info_geo = temp_bs.find('table', {'class': 'infobox geography vcard'})
        if info_vcard:
            location = info_vcard.find('th', text=re.compile("Location"))
            seats = info_vcard.find('th', text=re.compile("Capacity"))
            surface = info_vcard.find('th', text=re.compile("Surface"))
            if row['City']:
                city = row['City']
            elif location:
                city = location.findNext('td').text
            if row['Capacity']:
                capacity = row['Capacity']
            elif seats:
                capacity = seats.findNext('td').find(text=True)
            if row['Pitch']:
                picth = row['Pitch']
            elif surface:
                pitch = surface.findNext('td').find(text=True)
        elif info_geo:
            location = temp_bs.find('h1', {'id': 'firstHeading'})
            if row['City']:
                city = row['City']
            elif location:
                city = location.text
    return city, capacity, pitch


def create_teamcsv():
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

    team_incomplete = df_team[
            df_team['City'].isna()
            | df_team['Capacity'].isna()
            | df_team['Pitch'].isna()
            ]
    team_incomplete['Link_Stadium'] = None

    ROOT = 'https://en.wikipedia.org/wiki/'
    for index, row in team_incomplete.iterrows():
        URL = ROOT + urllib.parse.quote(row['Team'])
        try:
            temp_url = urlopen(URL)
            temp_bs = BeautifulSoup(temp_url.read(), 'html.parser')
        except HTTPError as err:
            if err.code == 404:
                print(row['Team'])
                print('Not found')
        else:
            info_vcard = temp_bs.find('table', {'class': 'infobox vcard'})
            info_geo = temp_bs.find(
                'table', {'class': 'infobox geography vcard'}
                )
            if info_vcard:
                ground = info_vcard.find('th', text=re.compile("Ground"))
                if ground:
                    row['Link_Stadium'] = ground.findNext('a')['href']
                    (row['City'], row['Capacity'], row['Pitch']) = \
                        get_stadium(row)
            elif info_geo:
                row['City'] = row['Team']

    df_incomplete = pd.concat(
                [df_team, team_incomplete]
                ).drop_duplicates(
                    ['Team'], keep='last')

    df_incomplete.to_csv(
                './Data/Dictionaries/Teams_to_Complete.csv',
                index=False)


def update_teams(df):
    filename = './Data/Dictionaries/dict_team.pkl'
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            dict_team = pickle.load(f)
    else:
        dict_team = {}

    teams = set(list(dict_team.keys()))
    teams_in_df = set(df.Team.unique())
    if (df.City.isna().sum() == 0) & (len(teams) <= len(teams_in_df)):
        return None

    new_teams = {}
    teams_diff = teams - teams_in_df
    for team in teams_diff:
        new_teams[team] = dict_team[team]

    new_columns = ['City', 'Country', 'Stadium',
                   'Address', 'Capacity', 'Pitch']

    df_new_teams = pd.DataFrame.from_dict(new_teams, orient='index',
                                          columns=new_columns)
    df_new_teams.index = df_new_teams.index.set_names(['Team'])
    df_new_teams.reset_index(inplace=True)
    team_incomplete = df_team[df_team['City'].isna()]
    team_incomplete = pd.concat(
            [df_new_teams, team_incomplete]
            ).drop_duplicates(
                ['Team'], keep='last')
    updates = ''
    ROOT = 'https://en.wikipedia.org/wiki/'
    for index, row in team_incomplete.iterrows():
        URL = ROOT + urllib.parse.quote(row['Team'])
        try:
            temp_url = urlopen(URL)
            temp_bs = BeautifulSoup(temp_url.read(), 'html.parser')
        except HTTPError as err:
            if err.code == 404:
                print(row['Team'])
                print('Not found')
        else:
            info_vcard = temp_bs.find('table', {'class': 'infobox vcard'})
            info_geo = temp_bs.find(
                'table', {'class': 'infobox geography vcard'}
                )
            if info_vcard:
                ground = info_vcard.find('th', text=re.compile("Ground"))
                if ground:
                    row['Link_Stadium'] = ground.findNext('a')['href']
                    (row['City'], row['Capacity'], row['Pitch']) = \
                        get_stadium(row)
            elif info_geo:
                row['City'] = row['Team']
            if row['City']:
                updates += f'Updated {row["City"]}\n'

    df_updated = pd.concat(
                [df, team_incomplete]
                ).drop_duplicates(
                    ['Team'], keep='last')

    df_updated.to_csv(
                './Data/Dictionaries/Team_Info.csv',
                index=False)
    return updates


csv_filename = './Data/Dictionaries/Team_Info.csv'
if not os.path.exists(csv_filename):
    csv_incomplete = './Data/Dictionaries/Teams_to_Complete.csv'
    if not os.path.exists(csv_incomplete):
        create_teamcsv()
    else:
        print(f'Go to {csv_incomplete}, manually check, fill it, \
                and save it as {csv_filename}')
else:
    df_team = pd.read_csv(csv_filename)
    update_teams(df_team)