from Extract.Extract_Data import *
import os
import pandas as pd


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
        os.makedirs(f"./Data/Standings/{league}", exist_ok=True)
        os.makedirs(f"./Data/Results/{league}", exist_ok=True)

    list_standings = ['Position', 'Team', 'Points', 'Win',
                      'Draw', 'Lose', 'Goals_For', 'Goals_Against',
                      'Number_Teams', 'Season', 'Round', 'League']
    list_results = ['Home_Team', 'Away_Team', 'Result', 'Date',
                    'Link', 'Season', 'Round', 'League']
    dict_standings = {x: [] for x in list_standings}
    dict_results = {x: [] for x in list_results}
    df_standings = pd.DataFrame(dict_standings)
    df_results = pd.DataFrame(dict_results)

    for league in leagues:
        df_standings.to_csv(f"./Data/Standings/{league}/"
                            + f"Standings_{year_1}_{league}.csv",
                            index=False)
        df_results.to_csv(f"./Data/Results/{league}/"
                          + f"Results_{year_1}_{league}.csv",
                          index=False)
        for year in range(year_1, year_2 + 1):
            print(f'Accesing data from year {year} of {league}')
            driver = accept_cookies(year=year, league=league)
            num_rounds = extract_rounds(driver)
            if num_rounds == 0:
                print(f'No available data for year {year} on {league}')
                print('Skipping to the next year')
                driver.quit()
                continue
            driver.quit()

            for round in range(1, num_rounds + 1):
                print(f'\tAccesing data from round {round} of year'
                      + f' {year} of {league}')
                driver = accept_cookies(year, league, round)
                standings = extract_standing(driver)
                results = extract_results(driver)

                if standings is None or results is None:
                    print(f'-------------------------------------------------')
                    print(f'!!!\tRound {round} does not'
                          + f'exist on year {year}\t!!!''')
                    print(f'-------------------------------------------------')
                    driver.quit()
                    continue

                driver.quit()
                for i, key in enumerate(list_standings[:-3]):
                    dict_standings[key].extend(standings[i])

                dict_standings['Season'].extend([year] * len(standings[0]))
                dict_standings['Round'].extend([round] * len(standings[0]))
                dict_standings['League'].extend([league] * len(standings[0]))

                for i, key in enumerate(list_results[:-3]):
                    dict_results[key].extend(results[i])

                dict_results['Season'].extend([year] * len(results[0]))
                dict_results['Round'].extend([round] * len(results[0]))
                dict_results['League'].extend([league] * len(results[0]))
                pd.DataFrame(dict_results).to_csv(
                        f"./Data/Results/{league}/"
                        + f"Results_{year_1}_{league}.csv",
                        mode='w', header=False, index=False)
                for key in dict_results:
                    dict_results[key].clear()

                pd.DataFrame(dict_standings).to_csv(
                        f"./Data/Standings/{league}/"
                        + f"Standings_{year_1}_{league}.csv",
                        mode='w', header=False, index=False)
                for key in dict_standings:
                    dict_standings[key].clear()


def create_standings_database(year_1, year_2, leagues):
    '''
    Scrape the webpage to populate databases that gathers information
    about the standing tables from year_1 to year_2 in a specific league
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
        os.makedirs(f"./Data/Standings/{league}", exist_ok=True)

    list_standings = ['Position', 'Team', 'Points', 'Win',
                      'Draw', 'Lose', 'Goals_For', 'Goals_Against',
                      'Number_Teams', 'Season', 'Round', 'League']
    dict_standings = {x: [] for x in list_standings}
    df_standings = pd.DataFrame(dict_standings)

    for league in leagues:
        df_standings.to_csv(f"./Data/Standings/{league}/"
                            + f"Standings_{year_1}_{league}.csv",
                            index=False)
        for year in range(year_1, year_2 + 1):
            print(f'Accesing data from year {year} of {league}')
            driver = accept_cookies(year=year, league=league)
            num_rounds = extract_rounds(driver)
            if num_rounds == 0:
                print(f'No available data for year {year} on {league}')
                print('Skipping to the next year')
                driver.quit()
                continue
            driver.quit()

            for round in range(1, num_rounds + 1):
                print(f'Accesing data from round {round} of year'
                      + f' {year} of {league}')
                driver = accept_cookies(year, league, round)
                standings = extract_standing(driver)

                if standings is None:
                    print(f'-------------------------------------------------')
                    print(f'!!!\tRound {round} does not'
                          + f'exist on year {year}\t!!!''')
                    print(f'-------------------------------------------------')
                    driver.quit()
                    continue

                driver.quit()
                for i, key in enumerate(list_standings[:-3]):
                    dict_standings[key].extend(standings[i])

                dict_standings['Season'].extend([year] * len(standings[0]))
                dict_standings['Round'].extend([round] * len(standings[0]))
                dict_standings['League'].extend([league] * len(standings[0]))

                pd.DataFrame(dict_standings).to_csv(
                        f"./Data/Standings/{league}/"
                        + "Standings_{year_1}_{league}.csv",
                        mode='w', header=False, index=False)
                for key in dict_standings:
                    dict_standings[key].clear()


def create_results_database(year_1, year_2, leagues):
    '''
    Scrape the webpage to populate databases that gathers information
    about the results tables from year_1 to year_2 in a specific league
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

    list_results = ['Home_Team', 'Away_Team', 'Result', 'Date',
                    'Link', 'Season', 'Round', 'League']
    dict_results = {x: [] for x in list_results}
    df_results = pd.DataFrame(dict_results)

    for league in leagues:
        df_results.to_csv(f"./Data/Results/{league}/"
                          + f"Results_{year_1}_{league}.csv",
                          index=False)
        for year in range(year_1, year_2 + 1):
            print(f'Accesing data from year {year} of {league}')
            driver = accept_cookies(year=year, league=league)
            num_rounds = extract_rounds(driver)
            if num_rounds == 0:
                print(f'No available data for year {year} on {league}')
                print('Skipping to the next year')
                driver.quit()
                continue
            driver.quit()

            for round in range(1, num_rounds + 1):
                print(f'\tAccesing data from round {round} of year'
                      + f' {year} of {league}')
                driver = accept_cookies(year, league, round)
                results = extract_results(driver)

                if results is None:
                    print(f'-------------------------------------------------')
                    print(f'!!!\tRound {round} does not'
                          + f'exist on year {year}\t!!!''')
                    print(f'-------------------------------------------------')
                    driver.quit()
                    continue

                driver.quit()

                for i, key in enumerate(list_results[:-3]):
                    dict_results[key].extend(results[i])

                dict_results['Season'].extend([year] * len(results[0]))
                dict_results['Round'].extend([round] * len(results[0]))
                dict_results['League'].extend([league] * len(results[0]))
                pd.DataFrame(dict_results).to_csv(
                        f"./Data/Results/{league}/"
                        + f"Results_{year_1}_{league}.csv",
                        mode='w', header=False, index=False)
                for key in dict_results:
                    dict_results[key].clear()
