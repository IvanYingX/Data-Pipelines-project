from Load.load_df import load_raw
import pandas as pd
from Extract.Extract_Data import extract_match_info
import os
import pickle
import numpy as np
from urllib.error import HTTPError

RAW_RES_DIR = './Data/Raw_Data/Results'
df_results = load_raw(RAW_RES_DIR)
df_match = pd.read_csv('./Data/Extended_Raw/Match_Info.csv')
df_results = df_results.merge(right=df_match, on='Link')
df_results = df_results.drop(columns=['Date'])
df_results = df_results.rename(columns={'Date_New':'Date'})
print(df_results.columns)
