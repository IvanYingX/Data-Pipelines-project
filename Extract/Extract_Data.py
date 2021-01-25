import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np
import os

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
    driver = webdriver.Chrome(driver_dir)
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
            return round.text.split()[1]
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

    result = []
    for i in range(num_matches):
        try:
            result.append(results_table[i].find('div', {'class':'clase'}).text)
        except:
            result.append(np.nan)

    date = [results_table[i].find('td', {'class':'time'}).find(text=True) for i in range(num_matches)]

    results = [home_team, away_team, result, date]

    if len(set([len(i) for i in results])) == 1:
        return results
    else:
        return [None] * len(results)