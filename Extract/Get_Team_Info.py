from load_df import load_leagues
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
                pitch = row['Pitch']
            elif surface:
                pitch = surface.findNext('td').find(text=True)
        elif info_geo:
            location = temp_bs.find('h1', {'id': 'firstHeading'})
            if row['City']:
                city = row['City']
            elif location:
                city = location.text
    return city, capacity, pitch


def get_link(df_team, update=True):
    df_incomplete = df_team[df_team['City'].isna()
                            | df_team['Capacity'].isna()
                            | df_team['Pitch'].isna()]
    df_incomplete['Link_Stadium'] = None
    update_text = ''
    ROOT = 'https://en.wikipedia.org/wiki/'
    for (index, row) in df_incomplete.iterrows():
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
            if row['City'] and update:
                update_text += f'Added {row["City"]} to {row["Team"]}\n'
    if update:
        return df_incomplete, update_text
    else:
        return df_incomplete


def create_teamcsv():
    filename = './Data/Dictionaries/dict_team.pkl'
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            dict_team = pickle.load(f)
    else:
        dict_team = {}

    new_columns = [
        'City',
        'Country',
        'Stadium',
        'Capacity',
        'Pitch',
        ]

    df_team = pd.DataFrame.from_dict(dict_team, orient='index',
                                     columns=new_columns)
    df_team.index = df_team.index.set_names(['Team'])
    df_team.reset_index(inplace=True)

    team_incomplete = get_link(df_team, update=False)

    df_incomplete = pd.concat([df_team,
                              team_incomplete]).drop_duplicates(
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

    teams = set(dict_team.keys())
    teams_in_df = set(df.Home_Team.unique())
    if len(teams_in_df - teams) == 0:
        return None

    teams_diff = teams_in_df - teams
    new_teams = {team: [None] * 5 for team in teams_diff}

    new_columns = [
        'City',
        'Country',
        'Stadium',
        'Capacity',
        'Pitch',
        ]

    df_teams = pd.DataFrame.from_dict(dict_team, orient='index',
                                      columns=new_columns)
    df_teams.index = df_teams.index.set_names(['Team'])
    df_teams.reset_index(inplace=True)
    df_new_teams = pd.DataFrame.from_dict(new_teams, orient='index',
                                          columns=new_columns)
    df_new_teams.index = df_new_teams.index.set_names(['Team'])
    df_new_teams.reset_index(inplace=True)
    #
    # team_incomplete = df_new_teams[df_new_teams['City'].isna()]
    # team_incomplete = pd.concat(
    #         [df_new_teams, team_incomplete]
    #         ).drop_duplicates(
    #             ['Team'], keep='last')

    team_incomplete, updates = get_link(df_new_teams, update=True)

    df_updated = pd.concat([df_teams, team_incomplete]).drop_duplicates(
                            ['Team'], keep='last')

    df_updated.to_csv('./Data/Dictionaries/Team_Info.csv',
                      index=False)
    dict_updated = df_updated.set_index('Team').T.to_dict(orient='list')
    with open(filename, "wb") as f:
        pickle.dump(dict_updated, f)
    return updates


if __name__ == '__main__':
    RES_DIR = './Data/Results_cleaned/*'
    df_results = load_leagues(RES_DIR)
    csv_filename = './Data/Dictionaries/Team_Info.csv'
    if not os.path.exists(csv_filename):
        csv_incomplete = './Data/Dictionaries/Teams_to_Complete.csv'
        if not os.path.exists(csv_incomplete):
            create_teamcsv()
        else:
            print(f'Go to {csv_incomplete}, manually check, fill it, \
                    and save it as {csv_filename}')
    else:
        updates = update_teams(df_results)
        if updates is None:
            print('No updates were made for the team information')
        else:
            print(updates)
