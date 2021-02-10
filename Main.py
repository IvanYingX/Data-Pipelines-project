from Extract.Extract_Data import *
from Initial_Gui import *
from Create_Database import create_database
from Update_Database import update_database
from tkinter import messagebox
from bs4 import BeautifulSoup
from tkinter import filedialog
from tkinter import *
import pandas as pd
import glob

action = create_update.create_or_update()
if action:
    year_1, year_2, leagues = create_update.create()
    create_database(year_1, year_2, leagues)
else:
    is_file = get_file_update.file_or_dir()
    if is_file:
        root = Tk()
        gui = get_file_update.Update_Gui(root, is_file)
        root.mainloop()
        STA_DIR = './' + os.path.relpath(gui.path_sta, start=os.curdir)
        RES_DIR = './' + os.path.relpath(gui.path_res, start=os.curdir)
        update_database(RES_DIR, STA_DIR)
    else:
        root = Tk()
        gui = get_file_update.Update_Gui(root, is_file)
        root.mainloop()
        sta_dir = './' + os.path.relpath(gui.path_dir_sta, start=os.curdir)
        res_dir = './' + os.path.relpath(gui.path_dir_res, start=os.curdir)
        file_res_list = sorted(glob.glob(f'{res_dir}/*'))
        file_sta_list = sorted(glob.glob(f'{sta_dir}/*'))
        for RES_DIR, STA_DIR in list(zip(file_res_list, file_sta_list)):
            update_database(RES_DIR, STA_DIR)
