
from Data_Load.load_df import load_raw
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


def accept_cookies():
    '''
    Starts the driver which returns the html code of the webpage
    so that the city and country can be added to the search bar.

    Returns
    -------
    driver: webdriver
        The webdriver object that can extract the HTML code to look for the
        data in the wanted year, league and round
    '''

    ROOT_DIR = "https://www.wunderground.com/history"
    driver_dir = './Extract/chrome_driver/chromedriver.exe'
    options = Options()
    options.headless = True
    driver = webdriver.Chrome(driver_dir, chrome_options=options)
    driver.get(ROOT_DIR)
    delay = 3
    try:
        myElem = WebDriverWait(driver, delay).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//button[@id="truste-consent-button"]'))
                )
        print("Page is ready!")
    except TimeoutException:
        print("Loading took too much time!")
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


if __name__ == '__main__':
    filename = './Data/Dictionaries/dict_city_code.pkl'
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            dict_city_code = pickle.load(f)
    else:
        team_df = pd.read_csv('./Data/Dictionaries/Team_Info.csv')
        city_code_df = team_df.drop_duplicates(subset='City')
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
    print(dict_city_code)
