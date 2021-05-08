import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np
import os
from urllib.request import urlopen, Request
import requests
import pickle
from tqdm.notebook import tqdm
import time as tm
from urllib.error import HTTPError


def accept_cookies(year, league, round=None):
    '''
    Starts the driver which returns the html code of the webpage
    of a given year, league, and round to extract the data afterwards.

    Parameters
    ----------
    year: int
        Year of the match
    league: str
        League of the match
    round: int
        Number of the round from which the code starts the search.
        If None, the driver will start from the last round of that year,

    Returns
    -------
    driver: webdriver
        The webdriver object that can extract the HTML code to look for the
        data in the wanted year, league and round
    '''

    ROOT_DIR = "https://www.besoccer.com/"
    driver_dir = './Extract/chrome_driver/chromedriver.exe'
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    driver = webdriver.Chrome(driver_dir, chrome_options=options)
    if round:
        driver.get(ROOT_DIR + league + str(year) +
                   "/group1/round" + str(round))
    else:
        driver.get(ROOT_DIR + league + str(year))

    cookies_button = driver.find_elements_by_xpath(
                    '//button[@class=" css-1lloz7i"]')

    try:
        for button in cookies_button:
            if button.text == "AGREE":
                relevant_button = button
                relevant_button.click()
    except AttributeError:
        pass
    finally:
        return driver


def extract_current_year(soup):
    '''
    Returns the last year of the available data of a league

    ----------
    soup: BeautifulSoup
        The bs4 object that can extract the HTML code to look for the
        data in the wanted year, league and round

    Returns
    -------
    driver: webdriver
        The webdriver object that can extract the HTML code to look for the
        data in the current year, league and round
    '''
    year = soup.find("div", {"class": 'head-select'}).find(
        'option').text.split('/')[1]
    return int('20' + year)


def extract_rounds(soup):
    '''
    Returns the number of rounds corresponding to a year and league

    Parameters
    ----------
    soup: BeautifulSoup
        The bs4 object that can extract the HTML code to look for the
        data in the wanted year, league and round

    Returns
    -------
    int
        If the webpage has information about the number of rounds,
        it returns that number. Otherwise, it returns 0
    '''
    round = soup.find(
        "div", {"class": 'team-text ta-r cutom-margin'}
        ).find_all('p')[-1]
    if round:
        if len(round.text.split()) == 2:
            return int(round.text.split()[1])
        else:
            return 0
    else:
        return 0


def extract_results(soup):
    '''
    Returns the results from the matches for a given year, league, and round

    Parameters
    ----------
    driver: webdriver
        The webdriver object that can extract the HTML code to look for the
        data in the wanted year, league and round

    Returns
    -------
    results: list
        Returns a nested list with:
            Home Team: home_team
            Away Team: away_team
            Result: result
            Date: date
            Link: link
        If one of the list couldn't be extracted, the function
        return a list of null values
    '''
    soup_table = soup.find("div", {"class": 'panel-body p0 match-list-new'})
    if soup_table:
        results_table = soup_table.find_all(
            "a", {"class": 'match-link'})
    else:
        return None

    num_matches = len(results_table)
    home_team = [
        results_table[i].find(
            'div', {'class': 'team-info ta-r'}).find(
                'div', {'class': 'name'}).text
        for i in range(num_matches)]
    regex = re.compile('^team-name ta-l')
    away_team = [
        results_table[i].find(
            'div', {'class': regex}).find(
                'div', {'class': 'name'}).text
        for i in range(num_matches)]
    link = []
    result = []
    for i in range(num_matches):
        try:
            link.append(results_table[i]['href'])
        except AttributeError:
            link.append(np.nan)

        try:
            result.append(results_table[i].find(
                'div', {'class': 'marker'}).text.strip('\n'))
        except AttributeError:
            result.append(np.nan)

    results = [home_team, away_team, result, link]

    if len(set([len(i) for i in results])) == 1:
        return results
    else:
        return [None] * len(results)


def extract_team_info(df_standings):
    '''
    Returns a dictionary containing information about the all the teams
    in df_standings

    Parameters
    ----------
    df_standings: DataFrame
        A pandas dataframe containing the standings of each team.
        The function looks for the leagues and years in the
        dataframe and webscrapes the corresponding webpage to see
        what teams played during that year and league.
        If the team appears twice, the function ignores it,
        and looks for the next non-repeated team

    Returns
    -------
    dict_team: dict
        A dictionary containing information about each team in df_standings.
        This information contains the city, country, address, stadium,
        capacity of the stadium, and pitch of the stadium corresponding
        to each team.
    '''

    ROOT = 'https://www.besoccer.com/'
    years = list(set(df_standings['Year']))
    leagues = list(set(df_standings['League']))
    filename = './Data/Dictionaries/dict_team.pkl'

    if os.path.exists(filename):
        with open(filename, "rb") as f:
            dict_team = pickle.load(f)
    else:
        dict_team = {}

    for year in years:
        for league in leagues:
            print(f'Getting information about league {league}, in year {year}')
            URL = ROOT + league + str(year) + '/group1/round1'
            temp_url = urlopen(URL)
            temp_bs = BeautifulSoup(temp_url.read(), 'html.parser')
            soup_table = temp_bs.find("table", {"id": 'tabla2'})
            if soup_table:
                standings_table = soup_table.find('tbody').find_all('tr')
                num_teams = len(standings_table)
                team = [standings_table[i].find_all('td')[1].find('a').text
                        for i in range(num_teams)]
                team_links = [ROOT + standings_table[i].find_all('td')[1].find(
                        'a')['href'] for i in range(num_teams)]

                for i in range(len(team)):
                    if team[i] not in dict_team:
                        team_city = None
                        team_country = None
                        stadium = None
                        address = None
                        capacity = None
                        pitch = None
                        team_url = urlopen(team_links[i])
                        team_bs = BeautifulSoup(team_url.read(), 'html.parser')
                        team_table_1 = team_bs.find(
                            "table", {"class": 'table-info mr10 ml10 mt10'})

                        if team_table_1:

                            team_city = team_table_1.find(
                                    'td', text=re.compile("City"))
                            if team_city:
                                team_city = team_city.findNext('td').text
                                team_city = ' '.join(team_city.split())

                            team_country = team_table_1.find(
                                        'td', text=re.compile("Country"))
                            if team_country:
                                team_country = team_country.findNext('td').text
                                team_country = ' '.join(team_country.split())

                        team_table_2 = team_bs.find(
                            "table", {"class": 'table-info mr10 ml10'})
                        if team_table_2:

                            stadium = team_table_2.find(
                                    'td', text=re.compile("Name"))
                            if stadium:
                                stadium = stadium.findNext('td').text
                                stadium = ' '.join(stadium.split())

                            pitch = team_table_2.find(
                                    'td', text=re.compile("Pitch"))
                            if pitch:
                                pitch = pitch.findNext('td').text
                                pitch = ' '.join(pitch.split())
                            capacity = team_table_2.find(
                                        'td', text=re.compile("Seats"))
                            if capacity:
                                capacity = capacity.findNext('td').text
                                capacity = ' '.join(capacity.split())

                            address = team_table_2.find(
                                        'td', text=re.compile("Address"))
                            if address:
                                address = address.findNext('td').text
                                address = ' '.join(address.split())

                            dimensions = team_table_2.find(
                                        'td', text=re.compile("Dimensions"))
                            if dimensions:
                                dimensions = dimensions.findNext('td').text
                                dimensions = ' '.join(dimensions.split())

                        dict_team[team[i]] = [team_city, team_country, stadium,
                                              address, capacity, pitch]
                        with open(filename, 'wb') as pickle_out:
                            pickle.dump(dict_team, pickle_out)
    return dict_team


def extract_match_info(df_results):
    '''
    Extracts information about the matches in df_results using the Link column.
    The information is stored in a dictionary that is updated as the function
    encounters matches that have not been included in the dictionary already.
    Returns a boolean that tells whether all links have been visited

    Parameters
    ----------
    df_results: DataFrame
        A pandas dataframe containing information about matches. The function
        iterates through all the rows, and scrapes in the URL included in the
        Link colum. This Link includes aditional information about the match

    Returns
    -------
    bool
        The boolean is True if the amount of keys in the dictionary is equal
        to the amount of unique links in df_results. This value tells the
        script or function calling extract_match_info when to stop.
    '''

    match_filename = 'dict_match.pkl'
    players_filename = 'dict_players.pkl'

    if os.path.exists(match_filename):
        with open(match_filename, "rb") as f:
            dict_match = pickle.load(f)
    else:
        dict_match = {}

    if os.path.exists(players_filename):
        with open(players_filename, "rb") as f:
            dict_players = pickle.load(f)
    else:
        dict_players = {}
    t_0 = tm.time()
    new_match = set(df_results.Link.unique()) - set(dict_match.keys())
    pbar = tqdm(new_match)
    for match in pbar:
        if tm.time() - t_0 > 30 * 60:
            break
        date = None
        time = None
        home_mean_score = None
        away_mean_score = None
        session = requests.Session()
        match_url = session.get(match, headers={'User-Agent': 'Mozilla/5.0'})
        tm.sleep(1)
        if match_url.status_code == 403:
            print(match_url.status_code)
            # raise NameError('403: Forbidden')
            break
        elif match_url.status_code != 200:
            raise HTTPError(match,
                            match_url.status_code,
                            'Internal Error',
                            {},
                            None)
        league_season = df_results[df_results['Link'] == match]
        if len(league_season) > 1:
            league_season = league_season.iloc[0]
            pbar.set_postfix({'League': league_season['League'],
                            'Season': league_season['Season'],
                            'Round': league_season['Round']})
        else:

            pbar.set_postfix({'League': league_season['League'].values[0],
                            'Season': league_season['Season'].values[0],
                            'Round': league_season['Round'].values[0]})
        match_bs = BeautifulSoup(match_url.text, 'html.parser')

        match_date = match_bs.find('div', {'class': 'date'})

        if match_date:
            if len(match_date.text.split()) > 3:
                date = ' '.join(match_date.text.split()[0:3])
                time = match_date.text.split()[3]
            else:
                date = match_date.text.strip()
                time = None
        home_lineup = match_bs.find('ul',
                                    {'class': 'lineup local'})
        if home_lineup:
            home_score = 0
            for i, player in enumerate(home_lineup.find_all('li'), 1):
                player_link = player.find('a')['href']
                if player_link in dict_players:
                    player_score = dict_players[player_link][1]
                else:
                    player_url = urlopen(player_link)
                    player_bs = BeautifulSoup(player_url.read(), 'html.parser')
                    player_score = player_bs.find('div',
                                                  {'class': 'elo-box'}).text
                    player_score = int(player_score.strip())
                    player_name = player_bs.find('div',
                                                 {'class': 'head-title'}).text
                    player_name = player_name.strip()
                    dict_players[player_link] = [player_name, player_score]
                home_score += player_score
            home_mean_score = home_score / i

        away_lineup = match_bs.find('ul',
                                    {'class': 'lineup visitor'})
        if away_lineup:
            away_score = 0
            for i, player in enumerate(away_lineup.find_all('li'), 1):
                player_link = player.find('a')['href']
                if player_link in dict_players:
                    player_score = dict_players[player_link][1]
                else:
                    player_url = urlopen(player_link)
                    player_bs = BeautifulSoup(player_url.read(), 'html.parser')
                    player_score = player_bs.find('div',
                                                  {'class': 'elo-box'}).text
                    player_score = int(player_score.strip())
                    player_name = player_bs.find('div',
                                                 {'class': 'head-title'}).text
                    player_name = player_name.strip()
                    dict_players[player_link] = [player_name, player_score]
                away_score += player_score
            away_mean_score = away_score / i

        dict_match[match] = [date, time, home_mean_score, away_mean_score]

        with open(match_filename, 'wb') as pickle_out:
            pickle.dump(dict_match, pickle_out)

        with open(players_filename, 'wb') as pickle_out:
            pickle.dump(dict_players, pickle_out)
