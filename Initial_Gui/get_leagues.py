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

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit('Quitting...')

    root.protocol("WM_DELETE_WINDOW", on_closing)
    root.geometry("450x300+120+120")
    tk.Label(
        root, text="""Select the leagues you want to extract data from""",
        justify=tk.LEFT, font=("Arial", 14), padx=5, pady=10
        ).grid(row=0, column=0, columnspan=2)
    r = 0
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

    r = 0
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
              ).grid(row=8, column=0, pady=10, columnspan=2)
    root.mainloop()
    mask = [val.get() for val in box_var]
    return list(itertools.compress(leagues + leagues_2, mask)), mask
