from Extract.Extract_Data import *
from Initial_Gui import *
from Create_Database import create_database
from Update_Database import update_database
from tkinter import *
import glob
import os

action = create_update.create_or_update()
if action == 1:
    year_1, year_2, leagues = create_update.create()
    create_database(year_1, year_2, leagues)

elif action == 2:
    y_or_l = create_update.year_or_league()
    root = Tk()
    gui = create_update.Update_Gui(root, y_or_l)
    root.mainloop()
    if y_or_l == 1:
        file_res = './' + os.path.relpath(gui.path_res, start=os.curdir)
        update_database(file_res)
    elif y_or_l == 2:
        res_dir = './' + os.path.relpath(gui.path_dir_res, start=os.curdir)
        file_res = sorted(glob.glob(f'{res_dir}/*'))[-1]
        update_database(file_res)
    else:
        res_dir = './' + os.path.relpath(gui.path_dir_res, start=os.curdir)
        files = []
        leagues_list = glob.glob(res_dir)
        print(leagues_list)
        for file_dir in leagues_list:
            last_file = sorted(glob.glob(f'{file_dir}/*'))[-1]
            files.append(last_file)

        for res_file in files:
            update_database(res_file)
