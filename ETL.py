<<<<<<< HEAD
from Extract.Extract_Data import * 
from Initial_Data import *
from Create_Database import create_database
from tkinter import messagebox
from bs4 import BeautifulSoup

action = create_extend.create_or_extend()
if action:
    year_1, year_2, leagues = create_extend.create()
    create_database(year_1, year_2, leagues)
else:
    leagues = get_leagues.get_leagues()
    year_1 = get_years.get_initial_year()
    year_2 = get_years.get_final_year(year_1)

=======
from Extract.Extract_Data import * 
from Initial_Data import *
from Create_Database import create_database
from tkinter import messagebox
from bs4 import BeautifulSoup

action = create_extend.create_or_extend()
if action:
    year_1, year_2, leagues = create_extend.create()
    create_database(year_1, year_2, leagues)
else:
    leagues = get_leagues.get_leagues()
    year_1 = get_years.get_initial_year()
    year_2 = get_years.get_final_year(year_1)

>>>>>>> origin/main
