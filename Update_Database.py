import pickle
import os
import pandas as pd
from Data.load_df import load_raw
from Extract.Extract_Data import *
import glob
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def update_database(RES_DIR, STA_DIR):
    '''
    Takes the files in RES_DIR and STA_DIR and checks if there
    is any available update.
    If there is, it appends the available update to the 'Update'
    folder.

    If the chosen files don't have the latest year, it looks
    for the last available year in the file and its corresponding
    last round. That way, it can start the search in the next
    round, and if it was the last round of that year, the search
    will start on the first round of the following year.
    Parameters
    ----------
    RES_DIR: str
        Directory of the results file. The file has to be a csv
        corresponding to a single league
    STA_DIR: str
        Directory of the standings file. The chosen file has to
        correspond to the same league as the league in the results
        file, otherwise, the function terminates.

    '''
    
    df_results = pd.read_csv(RES_DIR)
    df_standings = pd.read_csv(STA_DIR)
    list_standings = ['Position', 'Team', 'Points', 'Round', 'Win', 'Draw',
                      'Lose', 'Goals_For', 'Goals_Against', 'Number_Teams',
                      'Year', 'League']
    list_results = ['Home_Team', 'Away_Team', 'Result', 'Date', 'Link',
                    'Year', 'Round', 'League']
    # Last year available in the dataset
    final_year = df_results.Year.max()
    # Last round available in the last year of the dataset
    last_round_df = df_results[df_results['Year'] == final_year].Round.max()
    # Check how many leagues we have in both files. There should be only one
    league = pd.concat([df_standings.League, df_results.League]).unique()
    print(league)
    if len(league) != 1:
        raise ValueError('''There is a problem with these CSVs. There is
                         more than 1 league''')
    league = league[0]

    dest_res_file = f'./Data/Updated/Results/Results_{league}.csv'
    dest_sta_file = f'./Data/Updated/Standings/Standings_{league}.csv'
    if not os.path.exists(dest_res_file):
        df_results.to_csv(dest_res_file, index=False)
    if not os.path.exists(dest_sta_file):
        df_standings.to_csv(dest_sta_file, index=False)

    driver = accept_cookies(year='', league=league)
    current_year = extract_current_year(driver)
    current_round = extract_rounds(driver)
    driver.quit()

    if final_year != current_year:
        for year in range(final_year, current_year):
            driver = accept_cookies(year=year, league=league)
            last_round_final_year = extract_rounds(driver)
            driver.quit()
            for r in range(last_round_df + 1, last_round_final_year + 1):
                print(f'''\tAccesing data from round {r} of year {year}
                      of {league}''')
                subset_results = df_results[(df_results['Year'] == year)
                                            & (df_results['Round'] == r)]
                subset_standings = df_standings[(df_standings['Year'] == year)
                                                & (df_standings['Round'] == r)]
                driver = accept_cookies(year=year, league=league, round=r)
                standings = extract_standing(driver)
                results = extract_results(driver)
                dict_standings = {x: [] for x in list_standings}
                dict_results = {x: [] for x in list_results}
                if standings is None or results is None:
                    print(f'------------------------------------------------')
                    print(f'!!!\tRound {r} does not exist on year {year}\t!!!')
                    print(f'------------------------------------------------')
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
                df_diff_standings = subset_standings.merge(
                                  new_df_standings, indicator=True,
                                  how='right').loc[
                                  lambda x: x['_merge'] != 'both']
                df_diff_standings = df_diff_standings.drop(['_merge'], axis=1)
                df_diff_standings.to_csv(dest_sta_file, mode='a', header=False,
                                         index=False)

            last_round_df = 0
    # Iterate through the current year
    if last_round_df != current_round:
        for r in range(last_round_df + 1, current_round + 1):
            print(f'''\tAccesing data from round {r} of year
                  {current_year} of {league}''')
            subset_results = df_results[(df_results['Year'] == current_year) &
                                        (df_results['Round'] == r)]
            subset_standings = df_standings[
                               (df_standings['Year'] == current_year) &
                               (df_standings['Round'] == r)]
            driver = accept_cookies(year=current_year, league=league, round=r)
            standings = extract_standing(driver)
            results = extract_results(driver)
            dict_standings = {x: [] for x in list_standings}
            dict_results = {x: [] for x in list_results}
            if standings is None or results is None:
                print(f'----------------------------------------------------')
                print(f'''!!!\tRound {r} does not exist on year
                      {current_year}\t!!!''')
                print(f'----------------------------------------------------')
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
            mask = new_df_results['Result'].map(lambda x: ':' not in x,
                                                na_action=None)
            new_df_results = new_df_results[mask]

            df_diff_results = subset_results.merge(
                            new_df_results, indicator=True,
                            how='right').loc[lambda x: x['_merge'] != 'both']
            df_diff_results = df_diff_results.drop(['_merge'], axis=1)
            df_diff_results.to_csv(dest_res_file, mode='a', header=False,
                                   index=False)
            df_diff_standings = subset_standings.merge(
                                new_df_standings, indicator=True,
                                how='right').loc[
                                lambda x: x['_merge'] != 'both']
            df_diff_standings = df_diff_standings.drop(['_merge'], axis=1)
            df_diff_standings.to_csv(dest_sta_file, mode='a', header=False,
                                     index=False)
    return None


if __name__ == '__main__':
    '''This will take the CSV files that were updated
    yesterday to check for new updates today.
    Don't change these values unless you haven't created an
    updated file, or you need to overwrite the updated files.'''
    res_dir = './Data/Updated/Results'
    sta_dir = './Data/Updated/Standings'
    file_res_list = sorted(glob.glob(f'{res_dir}/*'))
    file_sta_list = sorted(glob.glob(f'{sta_dir}/*'))
    for RES_DIR, STA_DIR in list(zip(file_res_list, file_sta_list)):
        update_database(RES_DIR, STA_DIR)
