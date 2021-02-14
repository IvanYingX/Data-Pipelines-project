
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
    options.headless = False
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


def get_city_code():
    driver = accept_cookies()
    print('I have clicked cookies')
    time.sleep(3)
    delay = 3
    search_bar = WebDriverWait(driver, delay).until(
                            EC.presence_of_element_located(
                                (By.XPATH, '//input[@id="historySearch"]')))
    while True:
        try:
            search_bar.click()
            search_bar.send_keys('Madrid España')
        except StaleElementReferenceException as Exception:
            time.sleep(3)
            search_bar = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//input[@id="historySearch"]')))
        else:
            print('success')
            break

    view_button = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//input[@id="dateSubmit"]')))

    while True:
        try:
            view_button.click()
        except ElementClickInterceptedException as Exception:
            search_bar.click()
            search_bar.send_keys(Keys.ENTER)
            view_button = WebDriverWait(driver, delay).until(
                        EC.presence_of_element_located(
                            (By.XPATH, '//input[@id="dateSubmit"]')))
        else:
            print('success')
            break
    time.sleep(3)
    print(driver.current_url)


if __name__=='__main__':
    get_city_code()
