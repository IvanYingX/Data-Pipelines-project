from Load.load_df import load_raw
import pandas as pd
from Extract.Extract_Data import extract_match_info
import os
import pickle
import numpy as np
from urllib.error import HTTPError

RES_DIR = './Data/Updated/Results'
df_results = load_raw(RES_DIR)
flag = False
while flag == False:
    try:
        flag = extract_match_info(df_results)
    except (HTTPError) as err:
        if err.code == 504:
            print('Gateway error')
            pass
        else:
            print(err)
            break

filename = './Data/Extended_Raw/dict_match.pkl'

if os.path.exists(filename):
    with open(filename, "rb") as f:
        dict_match = pickle.load(f)
else:
    dict_match = {}

new_columns = ['Date_New', 'Referee', 'Home_Yellow', 'Home_Red', 'Away_Yellow', 'Away_Red']
df_match = pd.DataFrame.from_dict(dict_match, orient='index', columns=new_columns)
df_match.index = df_match.index.set_names(['Link'])
df_match.to_csv('./Data/Extended_Raw/Match_Info.csv')