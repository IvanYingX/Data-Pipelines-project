from Data_Load.load_df import load_raw
from operator import methodcaller
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import ElementClickInterceptedException
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import numpy as np
import os
from urllib.request import urlopen, Request
import pickle


def accept_cookies(ROOT="https://www.wunderground.com/history"):
    """Starts the driver which returns the html code of the webpage so that the
    city and country can be added to the search bar.

    Returns
    -------
    driver: webdriver
        The webdriver object that can extract the HTML code to look for the
        data in the wanted year, league and round
    """

    ROOT_DIR = ROOT
    driver_dir = './Extract/chrome_driver/chromedriver.exe'
    options = Options()
    options.headless = True
    options.add_argument('log-level=2')
    driver = webdriver.Chrome(driver_dir, chrome_options=options)
    driver.get(ROOT_DIR)
    delay = 3
    n = 0
    while n < 20:
        n += 1
        print(f'Accessing {ROOT_DIR}. Iteration number {n}')
        try:
            myElem = WebDriverWait(driver, delay).until(
                    EC.presence_of_element_located(
                        (By.XPATH, '//button[@id="truste-consent-button"]'))
                    )
            print("Page is ready!")
            break
        except TimeoutException:
            print("Loading took too much time!")
            print('Trying again')
            delay += 2
    cookies_button = driver.find_elements_by_xpath(
                                '//button[@id="truste-consent-button"]'
                                )

    try:
        for button in cookies_button:
            if button.text == "Agree and proceed":
                relevant_button = button
                relevant_button.click()
    except AttributeError:
        pass
    finally:
        return driver


def get_city_code(city):
    driver = accept_cookies()
    print(f'Looking code for {city}')
    time.sleep(3)
    delay = 3
    search_bar = WebDriverWait(driver, delay).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//input[@id="historySearch"]')))
    while True:
        try:
            search_bar.click()
            search_bar.send_keys(city)
            time.sleep(4)
            search_bar.send_keys(Keys.ENTER)
        except StaleElementReferenceException:
            time.sleep(3)
            search_bar = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//input[@id="historySearch"]')))
        else:
            break

    view_button = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//input[@id="dateSubmit"]')))

    while True:
        try:
            view_button.click()
        except ElementClickInterceptedException:
            search_bar.click()
            search_bar.send_keys(Keys.ENTER)
            view_button = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//input[@id="dateSubmit"]')))
        else:
            break
    time.sleep(3)
    code_url = driver.current_url
    city_code = re.search('/daily/(.*?)/', code_url)
    if city_code:
        driver.quit()
        return city_code[1]
    else:
        driver.quit()
        return None


def get_hour(x):
    if len(x.split(',')) > 2:
        time = x.split(',')[2]
        hour = int(time.split(':')[0])
        minutes = time.split(':')[1]
        pm = True
        if (hour // 12) < 1:
            pm = False
        if pm:
            pm = 'PM'
        else:
            pm = 'AM'
        hour = str(hour % 12)
        return f'{hour}:{minutes} {pm}'
    else:
        return '5:00 PM'


def create_weather(new_df, df_team, match_df):
    new_df = new_df.merge(
                df_team, left_on='Home_Team', right_on='Team').merge(
                match_df, left_on='Link', right_on='Link')
    new_df['Date'] = pd.to_datetime(new_df['Date_New'].map(
                        lambda x: x.split(',')[1]))
    new_df['Date'] = new_df['Date'].map(lambda x: str(x).split()[0])
    new_df['Hour'] = new_df['Date_New'].map(get_hour)
    new_weather = new_df[
                ['Link', 'Date',
                 'Hour', 'City',
                 'Country', 'Code']
                ]
    return new_weather


if __name__ == '__main__':
    # Load the dataframes
    RES_DIR = './Data/Results_Cleaned/*'
    df_results = load_raw(RES_DIR)
    df_results = df_results[df_results['Season'] >= 2005]
    df_match = pd.read_csv('./Data/Dictionaries/Match_Info.csv')
    df_team = pd.read_csv('./Data/Dictionaries/Team_Info.csv')

    # Get the code for each city
    filename = './Data/Dictionaries/dict_city_code.pkl'
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            dict_city_code = pickle.load(f)
        city_code_df = df_team.drop_duplicates(subset='City')
        cities = list(city_code_df.City)
        countries = list(city_code_df.Country)
        country_dict = {x: y for x, y in zip(cities, countries)}

        city_diff = list(set(cities) - set(dict_city_code.keys()))
        for city in city_diff:
            dict_city_code[city] = [country_dict[city], None]
    else:
        city_code_df = df_team.drop_duplicates(subset='City')
        cities = list(city_code_df.City)
        countries = list(city_code_df.Country)
        dict_city_code = {x: [y, None] for x, y in zip(cities, countries)}
    for city, values in dict_city_code.items():
        if values[1]:
            continue
        else:
            values[1] = get_city_code(city + ' ' + values[0])
            with open(filename, 'wb') as pickle_out:
                pickle.dump(dict_city_code, pickle_out)

    # Add a column to the team dataset with each code
    df_team['Code'] = df_team['City'].map(lambda x: dict_city_code[x][1])

    # Create a weather csv to store the weather on each match
    weather_file = 'Data/Dictionaries/Weather_Info.csv'
    if os.path.exists(weather_file):
        df_weather = pd.read_csv(weather_file)
        # Take the results whose link are not in df weather
        weather_links = set(df_weather['Link'])
        results_links = set(df_results['Link'])
        diff_links = results_links - weather_links
        if len(diff_links) > 0:
            new_samples = df_results[df_results['Link'].isin(diff_links)]
            # Create the weather csv only with those entries that are not
            # in weather csv yet.
            new_weather = create_weather(new_samples, df_team, df_match)
            # When updating, the weather conditions will be replaced by NaNs
            df_weather = pd.concat([df_weather, new_weather],
                                   ignore_index=False).drop_duplicates(
                                       subset='Link')
            df_weather.to_csv(weather_file, index=False)
    else:
        df_weather = create_weather(df_results, df_team, df_match)
        df_weather.to_csv(weather_file, index=False)

    # Create a dictionary whose keys are the links, and values
    # are a list with the weather conditions
    filename = 'Data/Dictionaries/dict_weather.pkl'
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            dict_weather = pickle.load(f)
    else:
        dict_weather = {}
        with open(filename, 'wb') as f:
            pickle.dump(dict_weather, f)

    # Start the Scraping iterating through each match
    ROOT = "https://www.wunderground.com/history/daily/"
    for _, row in df_weather.iterrows():
        if row['Link'] not in dict_weather.keys():
            URL = ROOT + row['Code'] + '/date/' + row['Date']
            driver = accept_cookies(URL)
            # Wait for the driver to find the table
            try:
                daily_observations = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//table[@class='
                                 + '"mat-table cdk-table '
                                 + 'mat-sort ng-star-inserted"'
                                 + ']')))
            except TimeoutException:
                print("I could not find the daily observation table,\n"
                      + "I will look for an alternative")
            else:
                print(f'I found the daily observation table')

                html = driver.page_source
                temp_bs = BeautifulSoup(html, 'html.parser')
                daily_observations = temp_bs.find(
                        "table",
                        {"class": 'mat-table cdk-table '
                         + 'mat-sort ng-star-inserted'})
                # Even if the driver finds the table, the webpage might
                # refresh itself, so we can make another check
                while daily_observations is None:
                    _ = WebDriverWait(driver, 15).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//table[@class='
                                 + '"mat-table cdk-table '
                                 + 'mat-sort ng-star-inserted"'
                                 + ']')))
                    html = driver.page_source
                    temp_bs = BeautifulSoup(html, 'html.parser')
                    daily_observations = temp_bs.find(
                            "table",
                            {"class": 'mat-table cdk-table '
                             + 'mat-sort ng-star-inserted'})
                hour = row['Hour'].split(':')[0]
                hour_pm = row['Hour'].split(':')[1][-2:]
                regex = re.compile(rf"^{hour}:[0-9]{{2}} {hour_pm}")

                hour_column = daily_observations.find(text=regex)
                if hour_column:
                    hour_row = hour_column.find_parent('tr')
                    if hour_row:
                        temperature = hour_row.find(
                            'td',
                            {'class': 'mat-cell cdk-cell cdk-column'
                             + '-temperature mat-column-temperature'
                             + ' ng-star-inserted'}
                        ).text
                        dew_point = hour_row.find(
                            'td',
                            {'class': 'mat-cell cdk-cell cdk-column-dewPoint'
                             + ' mat-column-dewPoint ng-star-inserted'}
                        ).text
                        wind = hour_row.find(
                            'td',
                            {'class': 'mat-cell cdk-cell cdk-column-windSpeed'
                             + ' mat-column-windSpeed ng-star-inserted'}
                        ).text
                        pressure = hour_row.find(
                            'td',
                            {'class': 'mat-cell cdk-cell cdk-column-pressure'
                             + ' mat-column-pressure ng-star-inserted'}
                        ).text
                        dict_weather[row['Link']] = [
                            temperature, dew_point, wind, pressure]
                        with open(filename, 'wb') as f:
                            pickle.dump(dict_weather, f)
                        print('Data added to the database')
                        driver.quit()
                        continue
                print('I could not find data for that time\n'
                      + 'I will look for an alternative')

            try:
                daily_observations = WebDriverWait(driver, 3).until(
                            EC.presence_of_element_located(
                                (By.XPATH,
                                 '//table[@class="ng-star-inserted"]')))
            except TimeoutException:
                print('I could not find data for this match\n'
                      + 'Skipping to the next match')
                driver.quit()
                temperature = None
                dew_point = None
                wind = None
                pressure = None
                dict_weather[row['Link']] = [
                        temperature, dew_point, wind, pressure]
                with open(filename, 'wb') as f:
                    pickle.dump(dict_weather, f)
            else:
                print(f'I found the summary table')
                html = driver.page_source
                temp_bs = BeautifulSoup(html, 'html.parser')
                driver.quit()
                summary_table = temp_bs.find(
                        "div", {"class": 'summary-table'})
                # Look for the temperature
                temp_row = summary_table.find('th', text="Day Average Temp")
                if temp_row:
                    temperature = temp_row.findNext('td').text
                else:
                    temperature = None
                # Look for the dew point
                dew_point_row = summary_table.find('th', text="Average")
                if dew_point_row:
                    dew_point = dew_point_row.findNext('td').text
                else:
                    dew_point = None
                # Look for the wind speed
                wind_row = summary_table.find('th', text="Max Wind Speed")
                if wind_row:
                    wind = wind_row.findNext('td').text
                else:
                    wind = None
                # Look for the pressure
                pressure_row = summary_table.find('th',
                                                  text="Sea Level Pressure")
                if pressure_row:
                    pressure = pressure_row.findNext('td').text
                else:
                    pressure = None
                dict_weather[row['Link']] = [
                        temperature, dew_point, wind, pressure]
                with open(filename, 'wb') as f:
                    pickle.dump(dict_weather, f)
                print('Data added to the database')
        else:
            continue
