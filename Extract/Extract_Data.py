import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np
import os
import glob               
import calendar
import datetime
import difflib
from urllib.request import urlopen, Request

def accept_cookies(year, league, round = None):
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
    options.headless = True
    driver = webdriver.Chrome(driver_dir, chrome_options=options)
    if round:
         driver.get(ROOT_DIR + league + str(year) + "/group1/round" + str(round))
    else:
        driver.get(ROOT_DIR + league + str(year))

    cookies_button = driver.find_elements_by_xpath('//button[@class="sc-ifAKCX hYNOwJ"]')
    
    try:
        for button in cookies_button:
            if button.text == "AGREE":
                relevant_button = button
                relevant_button.click()
    except:
        pass
    finally:
        return driver

def extract_rounds(driver):
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
        If the webpage has information about the number of rounds, it returns that number
        Otherwise, it returns 0
    '''
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    round = soup.find("b", {"id":'short_dateLive', "class":'bold'})
    if round:
        if len(round.text.split()) == 2:
            return int(round.text.split()[1])
        else:
            return 0
    else:
        return 0
        
def extract_standing(driver):
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
        If one of the list couldn't be extracted, the function return a list of null values
    '''
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    soup_table = soup.find("table", {"id": 'tabla2'})
    if soup_table:
        standings_table = soup_table.find('tbody').find_all('tr')
    else:
        return None
    num_teams = len(standings_table)

    position = [standings_table[i].find_all('td')[0].find('span').text for i in range(num_teams)]
    team = [standings_table[i].find_all('td')[1].find('a').text for i in range(num_teams)]
    pts = [standings_table[i].find_all('td')[3].text for i in range(num_teams)]
    round = [standings_table[i].find_all('td')[4].text for i in range(num_teams)]
    win = [standings_table[i].find_all('td')[5].text for i in range(num_teams)]
    draw = [standings_table[i].find_all('td')[6].text for i in range(num_teams)]
    lost = [standings_table[i].find_all('td')[7].text for i in range(num_teams)]
    g_favour = [standings_table[i].find_all('td')[8].text for i in range(num_teams)]
    g_against = [standings_table[i].find_all('td')[9].text for i in range(num_teams)]
    n_teams = [num_teams] * len(position)

    standings = [position, team, pts, round, win, draw, lost, g_favour, g_against, n_teams]

    # Make sure that we haven't skipped any data
    
    if len(set([len(i) for i in standings])) == 1:
        return standings
    else:
        return [None] * len(standings)

def extract_results(driver):
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
        If one of the list couldn't be extracted, the function return a list of null values
    '''
    page = driver.page_source   
    soup = BeautifulSoup(page, 'html.parser')
    regex = re.compile('nonplayingnow')
    soup_table = soup.find("table", {"id": 'tablemarcador'})
    if soup_table:
        results_table = soup_table.find('tbody').find_all("tr", {"class" : regex})
    else:
        return None
    
    num_matches = len(results_table)

    home_team = [results_table[i].find('td', {'class':'team-home'}).find('span').find('a').text for i in range(num_matches)]
    away_team = [results_table[i].find('td', {'class':'team-away'}).find('span').find('a').text for i in range(num_matches)]
    
    link = []
    result = []
    for i in range(num_matches):
        try:
            link.append(results_table[i].find_all('td')[2].find('a')['href'])
        except:
            link.append(np.nan)

        try:
            result.append(results_table[i].find('div', {'class':'clase'}).text)
        except:
            result.append(np.nan)

    date = [results_table[i].find('td', {'class':'time'}).find(text=True) for i in range(num_matches)]

    results = [home_team, away_team, result, date, link]

    if len(set([len(i) for i in results])) == 1:
        return results
    else:
        return [None] * len(results)

def extract_team_info(df_standings):
    ROOT = 'https://www.besoccer.com/'
    years = list(set(df_standings['Year']))
    leagues = list(set(df_standings['League']))
    dict_team = {}
    for year in years:
        for league in leagues:
            print(f'Getting information about league {league}, in year {year}')
            URL = ROOT + league + str(year)
            temp_url = urlopen(URL)
            temp_bs = BeautifulSoup(temp_url.read(), 'html.parser', from_encoding="iso-8859-1")
            soup_table = temp_bs.find("table", {"id": 'tabla2'})
            if soup_table:
                standings_table = soup_table.find('tbody').find_all('tr')
                num_teams = len(standings_table)
                team = [standings_table[i].find_all('td')[1].find('a').text for i in range(num_teams)]
                team_links = [ROOT + standings_table[i].find_all('td')[1].find('a')['href'] for i in range(num_teams)]

                for i in range(len(team)):
                    if team[i] not in dict_team:
                        team_city = None
                        team_country = None 
                        stadium = None 
                        address = None 
                        capacity = None 
                        pitch = None
                        team_url = urlopen(team_links[i])
                        team_bs = BeautifulSoup(team_url.read(), 'html.parser', from_encoding="iso-8859-1")
                        team_table_1 = team_bs.find("table", {"class": 'table-info mr10 ml10 mt10'})
                        if team_table_1: 
                            team_city = team_table_1.find('td', text=re.compile("City"))
                            if team_city:
                                team_city = team_city.findNext('td').text
                                team_city = ' '.join(team_city.split())
                            team_country = team_table_1.find('td', text=re.compile("Country"))
                            if team_country:
                                team_country = team_country.findNext('td').text
                                team_country = ' '.join(team_country.split())

                        team_table_2 = team_bs.find("table", {"class": 'table-info mr10 ml10'})
                        if team_table_2: 
                            stadium = team_table_2.find('td', text=re.compile("Name"))
                            if stadium:
                                stadium = stadium.findNext('td').text
                                stadium = ' '.join(stadium.split())
                            pitch = team_table_2.find('td', text=re.compile("Pitch"))
                            if pitch:
                                pitch = pitch.findNext('td').text
                                pitch = ' '.join(pitch.split())              
                            capacity = team_table_2.find('td', text=re.compile("Seats"))
                            if capacity:
                                capacity = capacity.findNext('td').text
                                capacity = ' '.join(capacity.split())              
                            address = team_table_2.find('td', text=re.compile("Address"))
                            if address:
                                address = address.findNext('td').text
                                address = ' '.join(address.split())
                            dimensions = team_table_2.find('td', text=re.compile("Dimensions"))
                            if dimensions:
                                dimensions = dimensions.findNext('td').text
                                dimensions = ' '.join(dimensions.split())

                        dict_team[team[i]] = [team_city, team_country, stadium, address, capacity, pitch]
    return dict_team