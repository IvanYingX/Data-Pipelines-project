import pickle
import os
import pandas as pd
from Extract_Data import *
import glob
import numpy as np
from tqdm import tqdm

pd.options.mode.chained_assignment = None


def clean_result(x):
    if (':' in x) or ('(' in x):
        return None
    return x


def get_result(x):
    '''
    Returns the label, the goals for the home team, the
    the goals for the away team
    Parameters
    ----------
    x: str
        Result of the match in the form of X-X
    Returns
    -------
    int:
        Label of the match with 0 being win for the home
        team, 1 being draw, and 2 being lose for the home
        team
    int:
        Number of goals for of the home team
    int:
        Number of goals for of the away team
    '''
    if x is None:
        return None, None, None
    result = x.split('-')
    if len(x) == 3:
        if result[0] > result[1]:
            return 0, int(result[0]), int(result[1])
        elif result[0] == result[1]:
            return 1, int(result[0]), int(result[1])
        else:
            return 2, int(result[0]), int(result[1])
    else:
        return None, None, None


umlauts = {'Ã€': 'À', 'Ã‚': 'Â', 'Ã„': 'Ä',
           'Ã…': 'Å', 'Ã†': 'Æ', 'Ã‡': 'Ç', 'Ãˆ': 'È', 'Ã‰': 'É',
           'ÃŠ': 'Ê', 'Ã‹': 'Ë', 'ÃŒ': 'Ì', 'ÃŽ': 'Î',
           'Ã‘': 'Ñ', 'Ã’': 'Ò', 'Ã“': 'Ó',
           'Ã”': 'Ô', 'Ã•': 'Õ', 'Ã–': 'Ö', 'Ã—': '×', 'Ã˜': 'Ø',
           'Ã™': 'Ù', 'Ãš': 'Ú', 'Ã›': 'Û', 'Ãœ': 'Ü',
           'Ãž': 'Þ', 'ÃŸ': 'ß', 'Ã ': 'à', 'Ã¡': 'á', 'Ã¢': 'â',
           'Ã£': 'ã', 'Ã¤': 'ä', 'Ã¥': 'å', 'Ã¦': 'æ', 'Ã§': 'ç',
           'Ã¨': 'è', 'Ã©': 'é', 'Ãª': 'ê', 'Ã«': 'ë', 'Ã¬': 'ì',
           'Ã®': 'î', 'Ã¯': 'ï', 'Ã°': 'ð', 'Ã±': 'ñ',
           'Ã²': 'ò', 'Ã³': 'ó', 'Ã´': 'ô', 'Ãµ': 'õ', 'Ã¶': 'ö',
           'Ã·': '÷', 'Ã¸': 'ø', 'Ã¹': 'ù', 'Ãº': 'ú', 'Ã»': 'û',
           'Ã¼': 'ü', 'Ã½': 'ý', 'Ã¾': 'þ', 'Ã¿': 'ÿ'}


def clean_names(x):
    if any(map(x.__contains__, umlauts.keys())):
        for word, initial in umlauts.items():
            x = x.replace(word, initial)
    return x


def get_from_standings(df):
    df.loc[:, 'Home_Team'] = df['Home_Team'].map(clean_names)
    df.loc[:, 'Away_Team'] = df['Away_Team'].map(clean_names)
    teams = list(set(df['Home_Team'].unique())
                 | set(df['Away_Team'].unique()))
    df['Number_Teams'] = len(teams)
    n_rounds = df['Round'].max()
    df['Total_Rounds'] = n_rounds
    # Get the result, the goals for and the goals against
    df['Result'] = df['Result'].map(clean_result)
    df['Label'], df['Goals_For_Home'], df['Goals_For_Away'] = \
        zip(*df['Result'].map(get_result))
    df = df[df['Label'].notna()]

    print(f'Getting info about \tSeason: {df.loc[0]["Season"]}'
          + f'\n\t\t\tLeague: {df.loc[0]["League"]}')
    # Create a dataframe to accumulates the results during the season
    # throughout the rounds
    list_standings = ['Team', 'Position', 'Points', 'Win',
                      'Draw', 'Lose', 'Win_Home', 'Win_Away',
                      'Draw_Home', 'Draw_Away', 'Lose_Home',
                      'Lose_Away', 'Goals_For', 'Goals_For_When_Home',
                      'Goals_For_When_Away', 'Goals_Against',
                      'Goals_Against_When_Home',
                      'Goals_Against_When_Away',
                      'Streak', 'Streak_When_Home', 'Streak_When_Away']
    dict_standings = {x: [] for x in list_standings}
    df_standings = pd.DataFrame(dict_standings)
    df_standings['Team'] = teams
    df_standings.iloc[:, 1:-3] = 0
    df_standings.iloc[:, -3:] = ''

    # Add new columns that can potentially increase the performance of
    # a model
    new_cols = ['Position_Home', 'Points_Home', 'Total_Wins_Home',
                'Total_Draw_Home', 'Total_Lose_Home',
                'Total_Goals_For_Home_Team',
                'Total_Goals_Against_Home_Team', 'Total_Streak_Home',
                'Wins_When_Home', 'Draw_When_Home', 'Lose_When_Home',
                'Goals_For_When_Home', 'Goals_Against_When_Home',
                'Position_Away', 'Points_Away', 'Total_Wins_Away',
                'Total_Draw_Away', 'Total_Lose_Away',
                'Total_Goals_For_Away_Team',
                'Total_Goals_Against_Away_Team', 'Total_Streak_Away',
                'Wins_When_Away', 'Draw_When_Away', 'Lose_When_Away',
                'Goals_For_When_Away', 'Goals_Against_When_Away',
                'Streak_When_Home', 'Streak_When_Away',
                ]

    df[new_cols] = 0
    # If a team wins it adds 3 points, 1 point if it draws and
    # 0 points if it loses
    dict_points_home = {0: 3, 1: 1, 2: 0}
    dict_points_away = {0: 0, 1: 1, 2: 3}

    # If Home team wins, we add 1 to the Wins Column, and 0 to the
    # Draws and Loses columns. On the other hand, the Away Team
    # behaves the other way around, it adds 1 to Lose, and 0
    # to the other columns
    dict_win_home = {0: 1, 1: 0, 2: 0}
    dict_draw_home = {0: 0, 1: 1, 2: 0}
    dict_lose_home = {0: 0, 1: 0, 2: 1}

    # We can extract the streak as a series of character, where 'W'
    # means wins, 'D' is Draw, and 'L' is lose.
    dict_streak_home = {0: 'W', 1: 'D', 2: 'L'}
    dict_streak_away = {0: 'L', 1: 'D', 2: 'W'}

    for r in tqdm(range(n_rounds)):
        cur_round = df[df['Round'] == (r + 1)]
        for _, row in df_standings.iterrows():
            team = row['Team']
            # If the selected team is in the Home Team column
            # we should add the variables concerning their
            # overall performance and only the performance
            # when it plays at home

            # Let's write the performance of the Home team
            if (cur_round['Home_Team'] == team).sum() >= 1:
                indices = list(cur_round.loc[cur_round['Home_Team']
                                             == team].index.values)

                # First the position of the team
                for idx in indices:
                    cur_round.loc[idx, 'Position_Home'] = \
                        row['Position']
                    cur_round.loc[idx, 'Points_Home'] = \
                        row['Points']
                    cur_round.loc[idx, 'Total_Wins_Home'] = \
                        int(row['Win'])
                    cur_round.loc[idx, 'Total_Draw_Home'] = \
                        int(row['Draw'])
                    cur_round.loc[idx, 'Total_Lose_Home'] = \
                        int(row['Lose'])
                    cur_round.loc[idx, 'Total_Goals_For_Home_Team'] = \
                        int(row['Goals_For'])
                    cur_round.loc[idx,
                                  'Total_Goals_Against_Home_Team'] = \
                        int(row['Goals_Against'])
                    cur_round.loc[idx, 'Total_Streak_Home'] = \
                        row['Streak']

                    # Let's write the performance of the home team
                    # when it is home
                    cur_round.loc[idx, 'Wins_When_Home'] = \
                        int(row['Win_Home'])
                    cur_round.loc[idx, 'Draw_When_Home'] = \
                        int(row['Draw_Home'])
                    cur_round.loc[idx, 'Lose_When_Home'] = \
                        int(row['Lose_Home'])
                    # Goals scored by the home team when it is home
                    cur_round.loc[idx, 'Goals_For_When_Home'] = \
                        int(row['Goals_For_When_Home'])
                    # Goals scored To the home team when
                    # it plays at home
                    cur_round.loc[idx, 'Goals_Against_When_Home'] = \
                        int(row['Goals_Against_When_Home'])
                    # Streak of the home team only for the matches
                    # played at home
                    cur_round.loc[idx, 'Streak_When_Home'] = \
                        row['Streak_When_Home']

            # Let's write the performance of the Away team when
            # it plays Away
            elif (cur_round['Away_Team'] == team).sum() >= 1:
                indices = list(cur_round.loc[cur_round['Away_Team']
                                             == team].index.values)

                # First the position of the team
                for idx in indices:
                    cur_round.loc[idx, 'Position_Away'] = \
                        row['Position']
                    cur_round.loc[idx, 'Points_Away'] = \
                        row['Points']
                    cur_round.loc[idx, 'Total_Wins_Away'] = \
                        int(row['Win'])
                    cur_round.loc[idx, 'Total_Draw_Away'] = \
                        int(row['Draw'])
                    cur_round.loc[idx, 'Total_Lose_Away'] = \
                        int(row['Lose'])
                    cur_round.loc[idx, 'Total_Goals_For_Away_Team'] = \
                        int(row['Goals_For'])
                    cur_round.loc[idx,
                                  'Total_Goals_Against_Away_Team'] = \
                        int(row['Goals_Against'])
                    cur_round.loc[idx, 'Total_Streak_Away'] = \
                        row['Streak']

                    # Let's write the performance of the away team when
                    # it plays away
                    cur_round.loc[idx, 'Wins_When_Away'] = \
                        int(row['Win_Away'])
                    cur_round.loc[idx, 'Draw_When_Away'] = \
                        int(row['Draw_Away'])
                    cur_round.loc[idx, 'Lose_When_Away'] = \
                        int(row['Lose_Away'])
                    # Goals scored by the Away team when it is Away
                    cur_round.loc[idx, 'Goals_For_When_Away'] = \
                        int(row['Goals_For_When_Away'])
                    # Goals scored To the Away team when it plays Away
                    cur_round.loc[idx, 'Goals_Against_When_Away'] = \
                        int(row['Goals_Against_When_Away'])
                    # Streak of the Away team only for the matches
                    # played at Away
                    cur_round.loc[idx, 'Streak_When_Away'] = \
                        row['Streak_When_Away']
            else:
                pass
        df.loc[cur_round.index] = cur_round
        for _, rows in cur_round.iterrows():
            # If a team wins it adds 3 points, 1 point if it draws and
            # 0 points if it loses

            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Points'] += \
                                 dict_points_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Points'] += \
                dict_points_away[rows['Label']]
            # If Home team wins, we add 1 to the Wins Column, and 0
            # to the Draws and Loses columns. On the other hand,
            # the Away Team behaves the other way around, it adds 1
            # to Lose, and 0 to the other columns
            # Let's do first the home team
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Win'] += \
                dict_win_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Win_Home'] += \
                dict_win_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Draw'] += \
                dict_draw_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Draw_Home'] += \
                dict_draw_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Lose'] += \
                dict_lose_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Lose_Home'] += \
                dict_lose_home[rows['Label']]
            # And now the away team
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Win'] += \
                dict_lose_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Win_Away'] += \
                dict_lose_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Draw'] += \
                dict_draw_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Draw_Away'] += \
                dict_draw_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Lose'] += \
                dict_win_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Lose_Away'] += \
                dict_win_home[rows['Label']]

            # We can extract the streak as a series of character,
            # where 'W' means wins, 'D' is Draw, and 'L' is lose.
            # The characters are added to the right, so the
            # leftmost character corresponds to the first round,
            # or the first round where the team was at
            # home if we are in the Streak_Home column
            # Let's see the Home_Team
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Streak'] += \
                dict_streak_home[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Streak_When_Home'] += \
                dict_streak_home[rows['Label']]
            # Let's see the away team
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Streak'] += \
                dict_streak_away[rows['Label']]
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Streak_When_Away'] += \
                dict_streak_away[rows['Label']]
            # The goals for of the home team is equal to
            # the goals against of the away team, and the
            # other way around
            # Let's see the home team
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Goals_For'] += \
                rows['Goals_For_Home']
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Goals_For_When_Home'] += \
                rows['Goals_For_Home']
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Goals_Against'] += rows['Goals_For_Away']
            df_standings.loc[df_standings['Team']
                             == rows['Home_Team'],
                             'Goals_Against_When_Home'] += \
                rows['Goals_For_Away']
            # Let's see the away team
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Goals_For'] += rows['Goals_For_Away']
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Goals_For_When_Away'] += \
                rows['Goals_For_Away']
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Goals_Against'] += \
                rows['Goals_For_Home']
            df_standings.loc[df_standings['Team']
                             == rows['Away_Team'],
                             'Goals_Against_When_Away'] += \
                rows['Goals_For_Home']
        df_standings = df_standings.sort_values(
                by='Points',
                ascending=False).reset_index(drop=True)
        df_standings['Position'] = np.array(df_standings.index) + 1
    print()
    return df


filename = 'Data/Dictionaries/dict_match.pkl'
with open(filename, 'rb') as f:
    match_dict = pickle.load(f)


def match_data(x):
    match_list = match_dict[x]
    return match_list[0], match_list[1], match_list[2], match_list[3]


def clean_database(to_clean=None, from_update=True, overwrite=False):
    '''
    Parameters
    ----------
    to_clean : list
        List of the leagues to clean. If set to None
        it clean all the available leagues
    from_update : bool
        Check whether we execute this function right
        after an update. If so, we need to specify
        which leagues have been updated to clean
        only those leagues that have been updated
    Returns
    -------
    '''
    if from_update:
        if to_clean is None:
            print('If from_update is true,'
                  + ' a list must be provided')
            return None
        else:
            for file in to_clean:
                season = file.split('Results_')[1].split('_')[0]
                league = '_'.join(file.split('Results_')[1].split('_')[1:]).split('.')[0]
                df = pd.read_csv(file)
                if len(df) == 0:
                    print(f'No available data for season {season} of {league}')
                    continue
                df = get_from_standings(df)
                df['Date'], df['Time'], df['Home_Score'], df['Away_Score'] = \
                    zip(*df['Link'].map(match_data))
                dst_file = file.split('Results_')[-1]
                dst_dir = f"./Data/Results_Cleaned/{league}/Cleaned_{dst_file}"
                df.to_csv(dst_dir, index=False)
    else:
        leagues = [x.split('/')[-1] for x in glob.glob('./Data/Results/*')]
        for league in leagues:
            os.makedirs(f"./Data/Results_Cleaned/{league}", exist_ok=True)
            seasons = glob.glob(f'./Data/Results/{league}/*')
            for season in seasons:
                # Load the data
                df = pd.read_csv(season)
                if len(df) == 0:
                    print(f'No available data for season {season} of {league}')
                    continue
                filename = f'Cleaned_{df.loc[0]["Season"]}' \
                           + f'_{df.loc[0]["League"]}.csv'
                dir_old_season = f"./Data/Results_Cleaned/{league}/{filename}"
                if os.path.exists(dir_old_season):
                    # Check if the existing cleaned dataset has the same length
                    # as the uncleaned dataset. Otherwise, that means some data
                    # is missing in the cleaned dataset
                    df_old = pd.read_csv(dir_old_season)
                    if (len(df) == len(df_old)) and (overwrite is False):
                        continue
                    else:
                        df = get_from_standings(df)
                        df['Date'], df['Time'], df['Home_Score'], \
                            df['Away_Score'] = \
                            zip(*df['Link'].map(match_data))
                        df.to_csv(dir_old_season, index=False)
                else:
                    df = get_from_standings(df)
                    df['Date'], df['Time'], df['Home_Score'], \
                        df['Away_Score'] = \
                        zip(*df['Link'].map(match_data))
                    df.to_csv(dir_old_season, index=False)


if __name__ == '__main__':
    leagues = [x.split('/')[-1] for x in glob.glob('./Data/Results/*')]
    to_clean = []
    for league in leagues:
        to_clean.extend(glob.glob(f'./Data/Results/{league}/*'))
    clean_database(
        to_clean = to_clean,
        from_update=True,
        overwrite=True
        )
