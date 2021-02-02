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
list_standings = ['Position', 'Team', 'Points', 'Round', 'Win', 'Draw', 'Lose',
                    'Goals_For', 'Goals_Against', 'Number_Teams', 'Year', 'League'] 
list_results = ['Home_Team', 'Away_Team', 'Result', 'Date', 'Link', 'Year', 'Round', 'League']
dict_standings = {x:[] for x in list_standings}
dict_results = {x:[] for x in list_results}
#%% Extracting the current situation of the dataframes
first_year = df_results.Year.min()
final_year = df_results.Year.max()
last_round_df = df_results[df_results['Year'] == final_year].Round.max()
league = df_standings.League.unique()
if len(league) != 1:
    raise ValueError('There is a problem with this csv. There are more than 1 league')
league = league[0]

#%% Extracting the current actual situation
driver = accept_cookies(year = '', league = league)
current_year = extract_current_year(driver)
current_round = extract_rounds(driver)
driver.quit()
#%% Comparing the current situation with the current dataframe`
if final_year != current_year:
    for year in range(final_year, current_year):
        driver = accept_cookies(year = year, league=league)
        last_round_final_year = extract_rounds(driver)
        driver.quit()
        for r in range(last_round_df + 1, last_round_final_year + 1):
            print(f'\tAccesing data from round {r} of year {year} of {league}') 
            subset_results = df_results[(df_results['Year'] == year) & (df_results['Round'] == r)]
            subset_standings = df_standings[(df_standings['Year'] == year) & (df_standings['Round'] == r)]            
            driver = accept_cookies(year = year, league = league, round = r)
            standings = extract_standing(driver)
            results = extract_results(driver)
            if standings == None or results == None: 
                    print(f'------------------------------------------------------')
                    print(f'!!!\tRound {round} does not exist on year {year}\t!!!')
                    print(f'------------------------------------------------------')
                    driver.quit()
                    continue

            driver.quit()
            for i, key in enumerate(list_standings[:-2]):
                dict_standings[key].extend(standings[i])

            dict_standings['Year'].extend([year] * len(standings[0]))
            dict_standings['League'].extend([league] * len(standings[0]))

            for i, key in enumerate(list_results[:-3]):
                dict_results[key].extend(results[i])

            dict_results['Year'].extend([year] * len(results[0]))
            dict_results['Round'].extend([round] * len(results[0]))
            dict_results['League'].extend([league] * len(results[0]))

            new_df_results = pd.DataFrame(dict_results)
            new_df_standings = pd.DataFrame(dict_standings)

            df_diff_results = subset_results.merge(new_df_results, indicator = True,
                            how='right').loc[lambda x : x['_merge']!='both']
            df_diff_standings = subset_standings.merge(new_df_standings, indicator = True,
                             how='right').loc[lambda x : x['_merge']!='both']
        last_round_df = 0

if last_round_df != current_round:
    for r in range(last_round_df + 1, current_round + 1):
        print(f'\tAccesing data from round {r} of year {current_year} of {league}') 
        subset_results = df_results[(df_results['Year'] == current_year) & (df_results['Round'] == r)]
        subset_standings = df_standings[(df_standings['Year'] == current_year) & (df_standings['Round'] == r)]            
        driver = accept_cookies(year = current_year, league = league, round = r)
        standings = extract_standing(driver)
        results = extract_results(driver)
        if standings == None or results == None: 
                print(f'------------------------------------------------------')
                print(f'!!!\tRound {r} does not exist on year {current_year}\t!!!')
                print(f'------------------------------------------------------')
                driver.quit()
                continue

        driver.quit()
        for i, key in enumerate(list_standings[:-2]):
            dict_standings[key].extend(standings[i])

        dict_standings['Year'].extend([current_year] * len(standings[0]))
        dict_standings['League'].extend([league] * len(standings[0]))

        for i, key in enumerate(list_results[:-3]):
            dict_results[key].extend(results[i])

        dict_results['Year'].extend([current_year] * len(results[0]))
        dict_results['Round'].extend([r] * len(results[0]))
        dict_results['League'].extend([league] * len(results[0]))

        new_df_results = pd.DataFrame(dict_results)
        new_df_standings = pd.DataFrame(dict_standings)

        df_diff_results = subset_results.merge(new_df_results, indicator = True,
                        how='right').loc[lambda x : x['_merge']!='both']
        df_diff_standings = subset_standings.merge(new_df_standings, indicator = True,
                            how='right').loc[lambda x : x['_merge']!='both']
        print(df_diff_results)



#%%

