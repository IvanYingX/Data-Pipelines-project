from Extract.Extract_Data import *
import pandas as pd


def create_database(year_1, year_2, leagues):
    list_standings = ['Position', 'Team', 'Points', 'Round', 'Win',
                      'Draw', 'Lose', 'Goals_For', 'Goals_Against',
                      'Number_Teams', 'Year', 'League']
    list_results = ['Home_Team', 'Away_Team', 'Result', 'Date',
                    'Link', 'Year', 'Round', 'League']
    dict_standings = {x: [] for x in list_standings}
    dict_results = {x: [] for x in list_results}
    df_standings = pd.DataFrame(dict_standings)
    df_results = pd.DataFrame(dict_results)

    for league in leagues:
        df_standings.to_csv(f"Standings_Raw_{year_1}_{year_2}_{league}.csv",
                            index=False)
        df_results.to_csv(f"Results_Raw_{year_1}_{year_2}_{league}.csv",
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
                print(f'''\tAccesing data from round {round} of year
                      {year} of {league}''')
                driver = accept_cookies(year, league, round)
                standings = extract_standing(driver)
                results = extract_results(driver)

                if standings is None or results is None:
                    print(f'-------------------------------------------------')
                    print(f'''!!!\tRound {round} does not
                          exist on year {year}\t!!!''')
                    print(f'-------------------------------------------------')
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
                pd.DataFrame(dict_results).to_csv(
                        f"Results_Raw_{year_1}_{year_2}_{league}.csv",
                        mode='a', header=False, index=False)
                for key in dict_results:
                    dict_results[key].clear()

                pd.DataFrame(dict_standings).to_csv(
                        f"Standings_Raw_{year_1}_{year_2}_{league}.csv",
                        mode='a', header=False, index=False)
                for key in dict_standings:
                    dict_standings[key].clear()
