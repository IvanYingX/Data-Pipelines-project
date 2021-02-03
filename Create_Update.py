#%% 
from Extract.Extract_Data import * 
from Initial_Data import *
from Create_Database import create_database
from tkinter import messagebox
from bs4 import BeautifulSoup
from tkinter import filedialog
from tkinter import *
import pandas as pd

action = create_update.create_or_update()
if action:
    year_1, year_2, leagues = create_update.create()
    create_database(year_1, year_2, leagues)
else:
    # create_update.update()
    root = Tk()
    root.filename = filedialog.askopenfilename(initialdir = "./",title = "Select file",filetypes = (("csv files","*.csv"),("all files","*.*")))
    root.mainloop()
    DIR = './' + os.path.relpath(root.filename, start = os.curdir)
    print(pd.read_csv(DIR).head())
    print(pd.read_csv(DIR).tail())
    # leagues = get_leagues.get_leagues()
    # year_1 = get_years.get_initial_year()
    # year_2 = get_years.get_final_year(year_1)

# %%
