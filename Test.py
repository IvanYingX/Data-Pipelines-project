# %% import libraries
import pickle
import os
import pandas as pd
from Data.load_df import load_raw
from Extract.Extract_Data import *
import glob
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup


def clean_cities(x):
    '''
    DOCSTRING
    '''
    if len(x.split(',')) > 1:
        print(x.split(',')[-2].strip())
        return x.split(',')[-2].strip()
    print(x.strip())
    return x


# %% loading dataframes to update
