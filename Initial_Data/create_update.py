import tkinter as tk
from tkinter import messagebox
import sys
from . import confirm, get_years, get_leagues

def create_or_update():
    root = tk.Tk()
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit('Quitting...')
            
    root.protocol("WM_DELETE_WINDOW", on_closing)
    v = tk.BooleanVar()
    w = tk.BooleanVar() 
    tk.Label(root, 
            text="""Do you want to Create a new Database,
            or Update an existing one?""",
            justify = tk.LEFT, padx = 20).grid(row=0, column=0)
    tk.Radiobutton(root, text="Create", indicatoron = 0, width = 30, padx = 20, variable=v, value = 1, command=root.destroy).grid(row=2, column=0)
    tk.Radiobutton(root, text="Update", indicatoron = 0, width = 30, padx = 20, variable=w, value = 1, command=root.destroy).grid(row=3, column=0)
    root.mainloop()
    return v.get()

def create():
    progress = 1
    next_fun = 0
    year_1 = 0
    year_2 = 0
    leagues = []
    mask = []
    while progress < 5:
        if next_fun == -1:
            progress -= 1
            next_fun = 0
        else:
            if progress == 1:
                leagues, mask = get_leagues.get_leagues()
                progress += 1
            elif progress == 2:
                year_1 = get_years.get_initial_year()
                if year_1 == -1:
                    next_fun = -1
                else:
                    progress += 1
            elif progress == 3:
                year_2 = get_years.get_final_year(year_1)
                if year_2 == -1:
                    next_fun = -1
                else:
                    progress += 1
            elif progress == 4:
                conf = confirm.confirm(year_1, year_2, mask)
                if conf:
                    progress += 1
                else:
                    next_fun = -1
    return year_1, year_2, leagues