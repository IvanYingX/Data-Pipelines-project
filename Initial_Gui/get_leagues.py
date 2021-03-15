import tkinter as tk
import itertools
from tkinter import messagebox
import sys


def get_leagues():
    leagues = [
            'premier_league', 'primera_division',
            'serie_a', 'ligue_1', 'bundesliga',
            'eredivisie', 'primeira_liga'
            ]
    leagues_names = [
                'Premier League', 'Primera Division',
                'Serie A', 'Ligue 1', 'Bundesliga',
                'Eredivisie', 'Primeira Liga'
                ]
    leagues_2 = [
            'championship', 'segunda_division',
            'serie_b', 'ligue_2', '2_liga',
            'eerste_divisie', 'segunda_liga'
            ]
    leagues_names_2 = [
                'Championship', 'Segunda Division',
                'Serie B', 'Ligue 2', '2. Bundesliga',
                'Eerste Divisie', 'Segunda Liga'
                ]
    box_var = []
    boxes = []
    box_num = 0
    root = tk.Tk()
    root.title('League Selection')
    
    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit('Quitting...')

    w = 425  # width for the Tk root
    h = 300  # height for the Tk root
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.protocol("WM_DELETE_WINDOW", on_closing)
    tk.Label(
        root, text="""Select the leagues you want to extract data from""",
        justify=tk.LEFT, font=("Arial", 14), padx=5, pady=10
        ).grid(row=0, column=0, columnspan=2)
    r = 1
    for league in leagues_names:
        box_var.append(tk.IntVar())
        boxes.append(
            tk.Checkbutton(
                root, text=league,
                variable=box_var[box_num]
                )
            )
        box_var[box_num].set(1)
        boxes[box_num].grid(row=r + 1, column=0)
        box_num += 1
        r += 1

    r = 1
    for league in leagues_names_2:
        box_var.append(tk.IntVar())
        boxes.append(
            tk.Checkbutton(
                root, text=league,
                variable=box_var[box_num]
                )
            )
        box_var[box_num].set(1)
        boxes[box_num].grid(row=r + 1, column=1)
        box_num += 1
        r += 1

    tk.Button(root, text="Confirm", width=10, relief=tk.RAISED,
              command=root.destroy, justify=tk.CENTER
              ).grid(row=9, column=0, pady=10, columnspan=2)
    root.mainloop()
    mask = [val.get() for val in box_var]
    return list(itertools.compress(leagues + leagues_2, mask)), mask
