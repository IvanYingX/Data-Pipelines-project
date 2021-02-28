from Extract.Extract_Data import *
from Initial_Gui import *
from Create_Database import create_database
from Create_Database import create_results_database
from Create_Database import create_standings_database
from Update_Database import update_database
from tkinter import *
import glob
import os

action = create_update.create_or_update()
if action == 1:
    res_or_sta = create_update.results_or_standings()
    year_1, year_2, leagues = create_update.create()
    if res_or_sta == 1:
        create_results_database(year_1, year_2, leagues)
    elif res_or_sta == 2:
        create_standings_database(year_1, year_2, leagues)
    elif res_or_sta == 3:
        create_database(year_1, year_2, leagues)

elif action == 2:
    y_or_l = create_update.year_or_league()
    root = Tk()
    gui = create_update.Update_Gui(root, y_or_l)
    root.mainloop()
    if y_or_l == 1:
        STA_DIR = './' + os.path.relpath(gui.path_sta, start=os.curdir)
        RES_DIR = './' + os.path.relpath(gui.path_res, start=os.curdir)
        update_database(RES_DIR, STA_DIR)
    elif (y_or_l == 2) or (y_or_l == 3):
        sta_dir = './' + os.path.relpath(gui.path_dir_sta, start=os.curdir)
        res_dir = './' + os.path.relpath(gui.path_dir_res, start=os.curdir)
        file_res_list = sorted(glob.glob(f'{res_dir}/*'))
        file_sta_list = sorted(glob.glob(f'{sta_dir}/*'))
        for RES_DIR, STA_DIR in list(zip(file_res_list, file_sta_list)):
            update_database(RES_DIR, STA_DIR)
