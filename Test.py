# %% import libraries
import pickle
import os
import pandas as pd
from Data.load_df import load_raw
from Extract.Extract_Data import *
import glob
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from Create_Database import create_standings_database

def clean_cities(x):
    '''
    DOCSTRING
    '''
    if len(x.split(',')) > 1:
        print(x.split(',')[-2].strip())
        return x.split(',')[-2].strip()
    print(x.strip())
    return x

create_standings_database(1990, 1991, 'premier_league')
# %% loading dataframes to update
