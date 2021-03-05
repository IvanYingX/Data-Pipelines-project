from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np
import os
from urllib.request import urlopen, Request
import pickle
import progressbar


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
                    '//button[@class="sc-ifAKCX hYNOwJ"]')

    try:
        for button in cookies_button:
            if button.text == "AGREE":
                relevant_button = button
                relevant_button.click()
    except AttributeError:
        pass
    finally:
        return driver


def extract_current_year(driver):
    '''
    Starts the driver which returns the html code of the webpage
    of a given year, league, and round to extract the data afterwards.

    Parameters
    ----------
    league: str
        League of the match

    Returns
    -------
    driver: webdriver
        The webdriver object that can extract the HTML code to look for the
        data in the current year, league and round
    '''
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    year = soup.find("small", {"class": 'nh-count'}).text.split('/')[1]
    return int(year)


def extract_rounds(soup):
    '''
    Returns the number of rounds corresponding to a year and league

    Parameters
    ----------
    driver: webdriver
        The webdriver object that can extract the HTML code to look for the
        data in the wanted year, league and round

    Returns
    -------
    int
        If the webpage has information about the number of rounds,
        it returns that number. Otherwise, it returns 0
    '''
    round = soup.find("b", {"id": 'short_dateLive', "class": 'bold'})
    if round:
        if len(round.text.split()) == 2:
            return int(round.text.split()[1])
        else:
            return 0
    else:
        return 0


def extract_standing(soup):
    '''
    Returns the standing data for a given year, league, and round

    Parameters
    ----------
    driver: webdriver
        The webdriver object that can extract the HTML code to look for the
        data in the wanted year, league and round

    Returns
    -------
    standings: list
        Returns a nested list with:
            Position: position
            Team: team
            Points: pts
            Round: round
            Number of matches won: win
            Number of matches drawn: draw
            Number of matches lost: lost
            Goals for: g_for
            Goals against: g_against
            Number of teams: n_teams
        If one of the list couldn't be extracted, the function return
        a list of null values
    '''
    soup_table = soup.find("table", {"id": 'tabla2'})
    if soup_table:
        standings_table = soup_table.find('tbody').find_all('tr')
    else:
        return None
    num_teams = len(standings_table)

    position = [
        int(standings_table[i].find_all('td')[0].find('span').text)
        for i in range(num_teams)
        ]
    team = [standings_table[i].find_all('td')[1].find('a').text
            for i in range(num_teams)]
    pts = [int(standings_table[i].find_all('td')[3].text)
           for i in range(num_teams)]
    win = [int(standings_table[i].find_all('td')[5].text)
           for i in range(num_teams)]
    draw = [int(standings_table[i].find_all('td')[6].text)
            for i in range(num_teams)]
    lost = [int(standings_table[i].find_all('td')[7].text)
            for i in range(num_teams)]
    g_favour = [int(standings_table[i].find_all('td')[8].text)
                for i in range(num_teams)]
    g_against = [int(standings_table[i].find_all('td')[9].text)
                 for i in range(num_teams)]
    n_teams = [num_teams] * len(position)

    standings = [position, team, pts, win, draw, lost, g_favour,
                 g_against, n_teams]

    # Make sure that we haven't skipped any data

    if len(set([len(i) for i in standings])) == 1:
        return standings
    else:
        return [None] * len(standings)


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
    regex = re.compile('nonplayingnow')
    soup_table = soup.find("table", {"id": 'tablemarcador'})
    if soup_table:
        results_table = soup_table.find('tbody').find_all(
            "tr", {"class": regex})
    else:
        return None

    num_matches = len(results_table)
    home_team = [results_table[i].find('td', {'class': 'team-home'}).find(
        'span').find('a').text for i in range(num_matches)]
    away_team = [results_table[i].find('td', {'class': 'team-away'}).find(
        'span').find('a').text for i in range(num_matches)]
    link = []
    result = []
    for i in range(num_matches):
        try:
            link.append(results_table[i].find_all('td')[2].find('a')['href'])
        except AttributeError:
            link.append(np.nan)

        try:
            result.append(results_table[i].find(
                'div', {'class': 'clase'}).text)
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

    ROOT = 'https://www.besoccer.com/'
    filename = './Data/Dictionaries/dict_match.pkl'

    if os.path.exists(filename):
        with open(filename, "rb") as f:
            dict_match = pickle.load(f)
    else:
        dict_match = {}

    new_match = set(df_results.Link.unique()) - set(dict_match.keys())
    bar = progressbar.ProgressBar(
            maxval=len(new_match),
            widgets=[progressbar.Bar('=', '[', ']'),
                     ' ', progressbar.Percentage()])
    bar.start()
    r = 0
    for match in new_match:
        date = None
        referee = None
        home_yellow = None
        home_red = None
        away_yellow = None
        away_red = None
        URL = ROOT + match
        match_url = urlopen(URL)
        match_bs = BeautifulSoup(match_url.read(), 'html.parser')
        match_table = match_bs.find('div', {'id': 'marcador'})
        home_table = match_bs.find('div', {'class': 'team team1'})
        away_table = match_bs.find('div', {'class': 'team team2'})

        if match_table:
            if match_table.find('div', {'class': 'marcador-header'}):
                date = match_table.find(
                    'div', {'class': 'marcador-header'}).find(
                    'span', {'class': 'jor-date'}).text
            if match_table.find('div', {'class': 'matchinfo'}):
                referee = match_table.find(
                    'div', {'class': 'matchinfo'}).find(
                    'li', {'class': 'ar'}).text
            if match_table.find('div', {'id': 'tarjetas'}):
                if match_table.find('div', {'id': 'tarjetas'}).find(
                                    'div', {'class': 'te1'}):
                    home_yellow = match_table.find(
                        'div', {'id': 'tarjetas'}).find(
                        'div', {'class': 'te1'}).find(
                        'span', {'class': 'am'}).text
                    home_red = match_table.find(
                        'div', {'id': 'tarjetas'}).find(
                        'div', {'class': 'te1'}).find(
                        'span', {'class': 'ro'}).text
                elif home_table:
                    home_yellow = len(home_table.find_all(
                        'span', {'class': 'flaticon-live-5'}))
                    home_red = len(home_table.find_all(
                        'span', {'class': 'flaticon-live-3'}))
            elif home_table:
                home_yellow = len(home_table.find_all(
                    'span', {'class': 'flaticon-live-5'}))
                home_red = len(home_table.find_all(
                    'span', {'class': 'flaticon-live-3'}))
            if match_table.find('div', {'id': 'tarjetas'}):
                if match_table.find('div', {'id': 'tarjetas'}).find(
                                    'div', {'class': 'te2'}):
                    away_yellow = match_table.find(
                        'div', {'id': 'tarjetas'}).find(
                        'div', {'class': 'te2'}).find(
                        'span', {'class': 'am'}).text
                    away_red = match_table.find(
                        'div', {'id': 'tarjetas'}).find(
                        'div', {'class': 'te2'}).find(
                        'span', {'class': 'ro'}).text
                elif away_table:
                    away_yellow = len(away_table.find_all(
                        'span', {'class': 'flaticon-live-5'}))
                    away_red = len(away_table.find_all(
                        'span', {'class': 'flaticon-live-3'}))
        dict_match[match] = [date, referee, home_yellow, home_red,
                             away_yellow, away_red]
        with open(filename, 'wb') as pickle_out:
            pickle.dump(dict_match, pickle_out)
        bar.update(r + 1)
        r += 1
    bar.finish()
