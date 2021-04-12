import pickle
import os
import pandas as pd
from Data_Load.load_df import load_raw
from Extract.Extract_Data import *
import glob
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def update_database(RES_DIR, is_file=False):
    """Takes the files in RES_DIR and and checks if there is any
    available update. If there is, it appends the available update to the
    'Update' folder.

    If the chosen files don't have the latest year, it looks
    for the last available year in the file and its corresponding
    last round. That way, it can start the search in the next
    round, and if it was the last round of that year, the search
    will start on the first round of the following year.
    Parameters
    ----------
    RES_DIR: str
        Directory of the results file. The file has to be a csv
    """

    df_results = pd.read_csv(RES_DIR)

    list_results = ['Home_Team', 'Away_Team', 'Result', 'Link',
                    'Season', 'Round', 'League']

    updated_list = []
    # Last year available in the dataset
    final_year = df_results.Season[0]
    # Last round available in the last year of the dataset
    last_round_df = df_results.Round[0]
    # League corresponding to the dataset
    league = df_results.League[0]
    # Start the scraping, we need to see the current actual year and round
    ROOT_DIR = "https://www.besoccer.com/"
    # If we pass a single file to the function, we just want to see if that
    # file is up to date rather than checking that the directoty has the
    # latest year
    if is_file:
        URL = (ROOT_DIR + league + str(final_year))
        year_url = urlopen(URL)
        year_bs = BeautifulSoup(year_url.read(), 'html.parser')
        last_round = extract_rounds(year_bs)
        if last_round != last_round_df:
            for r in range(last_round_df, last_round + 1):
                URL = (ROOT_DIR + league + str(final_year)
                       + "/group1/round" + str(r))
                round_url = urlopen(URL)
                round_bs = BeautifulSoup(round_url.read(), 'html.parser')
                results = extract_results(round_bs)
                dict_results = {x: [] for x in list_results}
                if results is None:
                    print(f'------------------------------------------------')
                    print(f'!!!\tRound {r} does not '
                          + f'exist on year {final_year}\t!!!')
                    print(f'------------------------------------------------')
                    continue
                for i, key in enumerate(list_results[:-3]):
                    dict_results[key].extend(results[i])
                subset_results = df_results[(df_results['Season']
                                             == final_year)
                                            & (df_results['Round'] == r)]
                dict_results['Season'].extend([final_year] * len(results[0]))
                dict_results['Round'].extend([r] * len(results[0]))
                dict_results['League'].extend([league] * len(results[0]))
                new_df_results = pd.DataFrame(dict_results)
                mask = new_df_results['Result'].map(lambda x: ':' not in x,
                                                    na_action=None)
                new_df_results = new_df_results[mask]
                df_diff_results = subset_results.merge(
                                new_df_results, indicator=True,
                                how='right').loc[
                                lambda x: x['_merge'] != 'both']
                df_diff_results = df_diff_results.drop(['_merge'], axis=1)
                df_diff_results.to_csv(RES_DIR, mode='a', header=False,
                                       index=False)
    URL = (ROOT_DIR + league)
    year_url = urlopen(URL)
    year_bs = BeautifulSoup(year_url.read(), 'html.parser')
    current_year = extract_current_year(year_bs)
    list_results = df_results.columns

    # If the final year of our database is lower than the current
    # actual year we need to extract the rounds from the final
    # year that has not been extracted
    if final_year != current_year:
        dest_res_file = (f'./Data/Results/{league}/Results'
                         + f'_{final_year}_{league}')
        if not os.path.exists(dest_res_file):
            df_results = pd.DataFrame(list_results)
            df_results.to_csv(dest_res_file, index=False)
        else:
            df_results = pd.read_csv(dest_res_file)

        for year in range(final_year, current_year):
            URL = ROOT_DIR + league + str(year)
            year_url = urlopen(URL)
            year_bs = BeautifulSoup(year_url.read(), 'html.parser')
            last_round_final_year = extract_rounds(year_bs)
            for r in range(last_round_df + 1, last_round_final_year + 1):
                print(f'''\tAccesing data from round {r} of year {year}
                      of {league}''')
                subset_results = df_results[(df_results['Season'] == year)
                                            & (df_results['Round'] == r)]
                URL = (ROOT_DIR + league + str(year)
                       + "/group1/round" + str(r))
                round_url = urlopen(URL)
                round_bs = BeautifulSoup(round_url.read(), 'html.parser')
                results = extract_results(round_bs)
                dict_results = {x: [] for x in list_results}
                if results is None:
                    print(f'------------------------------------------------')
                    print(f'!!!\tRound {r} does not exist on year {year}\t!!!')
                    print(f'------------------------------------------------')
                    continue
                for i, key in enumerate(list_results[:-3]):
                    dict_results[key].extend(results[i])

                dict_results['Season'].extend([year] * len(results[0]))
                dict_results['Round'].extend([r] * len(results[0]))
                dict_results['League'].extend([league] * len(results[0]))
                new_df_results = pd.DataFrame(dict_results)
                mask = new_df_results['Result'].map(lambda x: ':' not in x,
                                                    na_action=None)
                new_df_results = new_df_results[mask]
                df_diff_results = subset_results.merge(
                                new_df_results, indicator=True,
                                how='right').loc[
                                lambda x: x['_merge'] != 'both']
                df_diff_results = df_diff_results.drop(['_merge'], axis=1)
                df_diff_results.to_csv(dest_res_file, mode='a', header=False,
                                       index=False)
        last_round_df = 0

        current_round = extract_rounds(year_bs)
        for r in range(last_round_df, current_round + 1):
            print(f"Accesing data from: \tround {r} \n\t\t\tyear"
                  + f" {current_year} \n\t\t\tleague {league}")
            subset_results = df_results[
                                    (df_results['Season'] == current_year)
                                    & (df_results['Round'] == r)
                                ]
            URL = (ROOT_DIR + league + str(year)
                            + "/group1/round" + str(r))
            round_url = urlopen(URL)
            round_bs = BeautifulSoup(round_url.read(), 'html.parser')
            results = extract_results(round_bs)
            dict_results = {x: [] for x in list_results}
            if results is None:
                print(f'----------------------------------------------------')
                print(f'''!!!\tRound {r} does not exist on year
                        {current_year}\t!!!''')
                print(f'----------------------------------------------------')
                continue

            for i, key in enumerate(list_results[:-3]):
                dict_results[key].extend(results[i])

            dict_results['Season'].extend([current_year] * len(results[0]))
            dict_results['Round'].extend([r] * len(results[0]))
            dict_results['League'].extend([league] * len(results[0]))

            new_df_results = pd.DataFrame(dict_results)
            mask = new_df_results['Result'].map(lambda x: ':' not in x,
                                                na_action=None)
            new_df_results = new_df_results[mask]

            # Take only those matches that are already included
            df_diff_results = subset_results.merge(
                            new_df_results, indicator=True,
                            how='right').loc[lambda x: x['_merge'] != 'both']
            df_diff_results = df_diff_results.drop(['_merge'], axis=1)
            df_diff_results.to_csv(dest_res_file, mode='a', header=False,
                                   index=False)


if __name__ == '__main__':
    """This will take the CSV files that were updated yesterday to check for
    new updates today.

    Don't change these values unless you haven't created an updated
    file, or you need to overwrite the updated files.
    """
    files = []
    leagues_list = glob.glob('./Data/Results/*')
    for file_dir in leagues_list:
        last_file = sorted(glob.glob(f'{file_dir}/*'))[-1]
        files.append(last_file)

    for res_file in files:
        update_database(res_file)
