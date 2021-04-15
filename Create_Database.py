from Extract.Extract_Data import *
import os
import pandas as pd
from tqdm import tqdm
from urllib.error import HTTPError


def create_database(year_1, year_2, leagues):
    '''
    Scrape the webpage to populate databases that gathers information
    about the standing and the results tables from year_1 to year_2
    in a specific league
    Parameters
    ----------
    year_1: int
        Initial year to start the scraping from
    year_2: int
        Initial year to finish the scraping at
    leagues: str or list
        league(s) to extract the data from
    '''
    if type(leagues) is not list:
        leagues = [leagues]
    for league in leagues:
        os.makedirs(f"./Data/Results/{league}", exist_ok=True)

    list_results = ['Home_Team', 'Away_Team', 'Result',
                    'Link', 'Season', 'Round', 'League']
    dict_results = {x: [] for x in list_results}
    df_results = pd.DataFrame(dict_results)
    ROOT_DIR = "https://www.besoccer.com/competition/scores/"

    for league in leagues:
        for year in range(year_1, year_2 + 1):
            df_results.to_csv(f"./Data/Results/{league}/"
                              + f"Results_{year}_{league}.csv",
                              index=False)
            print(f'Accesing data from year {year} of {league}')
            URL = ROOT_DIR + league + '/' + str(year)
            try:
                year_url = urlopen(URL)
            except HTTPError as exception:
                if exception.code == 404:
                    print('The page does not exist')
                elif exception.code == 302:
                    print('The specified year or league does not exist')
                os.remove(f"./Data/Results/{league}/"
                          + f"Results_{year}_{league}.csv")
                continue  # Skip to the next year

            year_bs = BeautifulSoup(year_url.read(), 'html.parser')
            num_rounds = extract_rounds(year_bs)
            if num_rounds == 0:
                print(f'No available data for year {year} on {league}')
                print('Skipping to the next year')
                continue

            for round in tqdm(range(1, num_rounds + 1)):
                URL += "/group1/round" + str(round)
                round_url = urlopen(URL)
                round_bs = BeautifulSoup(round_url.read(), 'html.parser')
                results = extract_results(round_bs)

                if results is None:
                    print(f'-------------------------------------------------')
                    print(f'!!!\tRound {round} does not'
                          + f'exist on year {year}\t!!!''')
                    print(f'-------------------------------------------------')
                    continue

                for i, key in enumerate(list_results[:-3]):
                    dict_results[key].extend(results[i])

                dict_results['Season'].extend([year] * len(results[0]))
                dict_results['Round'].extend([round] * len(results[0]))
                dict_results['League'].extend([league] * len(results[0]))

            new_df_results = pd.DataFrame(dict_results)
            mask = new_df_results['Result'].map(lambda x: ':' not in x,
                                                na_action=None)
            new_df_results = new_df_results[mask]
            new_df_results.to_csv(
                    f"./Data/Results/{league}/"
                    + f"Results_{year}_{league}.csv",
                    mode='w', header=True, index=False)
            for key in dict_results:
                dict_results[key].clear()
