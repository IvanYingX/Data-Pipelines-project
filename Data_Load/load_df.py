import pandas as pd
import numpy as np
import glob
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import os
import time
pd.options.mode.chained_assignment = None


def load_raw(dir):
    '''
    DOCSTRING
    '''
    df_list = []
    for data_file in sorted(glob.glob(f'{dir}/*')):
        df_partial = pd.read_csv(data_file)
        df_list.append(df_partial)
    df = pd.concat(df_list, axis=0, ignore_index=True)
    return df


def check_teams_raw(df_results, df_standings):
    '''
    DOCSTRING
    '''
    diff_res = set()
    diff_sta = set()
    if set(df_results.Home_Team) != set(df_standings.Team):
        diff_res = sorted(set(df_results.Home_Team) - set(df_standings.Team))
        diff_sta = sorted(set(df_standings.Team) - set(df_results.Home_Team))

        if diff_res:
            print(f'''{diff_res} appear(s) in the results dataframe
                  but not in the standings dataframe''')
        if diff_sta:
            print(f'''{diff_sta} appear(s) in the standings dataframe
                  but not in the results dataframe''')

    return diff_res, diff_sta
