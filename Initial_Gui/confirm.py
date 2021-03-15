import tkinter as tk
from tkinter import messagebox
import sys
import itertools
leagues_names_1 = ['Premier League', 'Primera Division', 'Serie A', 'Ligue 1',
                   'Bundesliga', 'Eredivisie', 'Primeira Liga']
leagues_names_2 = ['Championship', 'Segunda Division', 'Serie B', 'Ligue 2',
                   '2. Bundesliga', 'Eerste Divisie', 'Segunda Liga']


def confirm(year_1, year_2, mask):
    league_names = list(itertools.compress(
                    leagues_names_1 + leagues_names_2, mask))
    leagues_text = '\n'.join(league_names)
    root = tk.Tk()
    root.title('Review')

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit('Quitting...')

    w = 300  # width for the Tk root
    h = 300  # height for the Tk root
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.protocol("WM_DELETE_WINDOW", on_closing)

    v = tk.IntVar()
    back = tk.BooleanVar()
    root.title("Summary")
    tk.Label(root, text=f'''You are extracting data from {year_1}
             to {year_2} from league(s)''',
             justify=tk.CENTER, font=("Arial", 12),
             padx=5, pady=10).grid(row=0, column=0, columnspan=2)
    tk.Label(root, text=f"{leagues_text}", justify=tk.CENTER,
             font=("Arial", 12), padx=5,
             pady=10).grid(row=1, column=0, columnspan=2)
    tk.Label(root, text="Do you want to continue?", justify=tk.CENTER,
             font=("Arial", 12), padx=5,
             pady=10).grid(row=2, column=0, columnspan=2)

    tk.Radiobutton(root, text="Yes", indicatoron=0, width=10, relief=tk.FLAT,
                   value=True, command=root.destroy).grid(
                       row=3, column=1, pady=10)
    tk.Radiobutton(root, text="Go Back", indicatoron=0,
                   width=10, relief=tk.FLAT, variable=back,
                   value=True, command=root.destroy).grid(
                       row=3, column=0, pady=10)
    root.mainloop()
    if back.get():
        return False
    else:
        return True
