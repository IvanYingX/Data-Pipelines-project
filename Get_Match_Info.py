from Load.load_df import load_raw
import pandas as pd
from Extract.Extract_Data import extract_team_info

RAW_STA_DIR = './Data/Standings'
RAW_RES_DIR = './Data/Results'

df_results = load_raw(RAW_RES_DIR)
df_standings =load_raw(RAW_STA_DIR)