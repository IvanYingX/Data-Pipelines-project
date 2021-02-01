from Load.load_df import load_raw
import pandas as pd
from Extract.Extract_Data import extract_match_info
import os
import pickle
import numpy as np
from urllib.error import HTTPError

RAW_STA_DIR = './Data/Raw_Data/Standings'
RAW_RES_DIR = './Data/Raw_Data/Results'

df_results = load_raw(RAW_RES_DIR)
filename = './Data/Extended_Raw/dict_match.pkl'
# if os.path.exists(filename):
#     with open(filename, "rb") as f:
#         dict_match = pickle.load(f)
# print(dict_match)
while True:
    try:
        dict_match = extract_match_info(df_results)
    except (HTTPError) as err:
        if err.code == 504:
            print('Gateway error')
            pass
        else:
            print(err)
            break