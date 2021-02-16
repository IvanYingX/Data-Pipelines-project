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

df_weather = pd.read_csv('./Data/Dictionaries/Weather_Info.csv')
ROOT = "https://www.wunderground.com/history/daily/"
for idx, row in df_weather.iterrows():
    URL = ROOT + row['Code'] + '/date/' + row['Date']
    # temp_url = urlopen(URL)
    # temp_bs = BeautifulSoup(temp_url.read(), 'html.parser')
    print(URL)
