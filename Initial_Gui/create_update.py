import tkinter as tk
from tkinter import messagebox
import sys
from . import confirm, get_years, get_leagues
import sys
from tkinter import *
from tkinter import filedialog
import tkinter
from tkinter import ttk, StringVar
from tkinter.filedialog import askopenfilename, askdirectory
import sys
from tkinter import messagebox
button_ttc = None


class Update_Gui:

    def __init__(self, root, is_file):
        self.input_text_res = StringVar()
        self.input_text_res_dir = StringVar()
        self.input_text_sta = StringVar()
        self.input_text_sta_dir = StringVar()
        self.path_res = ''
        self.path_dir_res = ''
        self.path_sta = ''
        self.path_dir_sta = ''

        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.resizable(0, 0)  # This prevents from resizing the window
        self.root.geometry("700x300")

        if is_file == 1:
            self.root.title("Choose your files")
            ttk.Button(
                self.root, text="Results File",
                command=lambda: self.set_path_res_field()
                ).grid(row=1, ipadx=5, ipady=15)
            ttk.Entry(
                self.root, textvariable=self.input_text_res,
                width=70
                ).grid(row=1, column=1, ipadx=1, ipady=1)
            ttk.Button(
                self.root, text="Standings File",
                command=lambda: self.set_path_sta_field()
                ).grid(row=2, ipadx=5, ipady=15)
            ttk.Entry(
                self.root, textvariable=self.input_text_sta, width=70
                ).grid(row=2, column=1, ipadx=1, ipady=1)
        elif is_file == 2:
            self.root.title("Choose your directories")
            ttk.Button(
                self.root, text="Directory of league (results)",
                command=lambda: self.set_path_res_dir_field()
                ).grid(row=1, ipadx=5, ipady=15)
            ttk.Entry(
                self.root, textvariable=self.input_text_res_dir,
                width=70
                ).grid(row=1, column=1, ipadx=1, ipady=1)
            ttk.Button(
                self.root, text="Directory of league (standings)",
                command=lambda: self.set_path_sta_dir_field()
                ).grid(row=2, ipadx=5, ipady=15)
            ttk.Entry(
                self.root, textvariable=self.input_text_sta_dir, width=70
                ).grid(row=2, column=1, ipadx=1, ipady=1)
        elif is_file == 3:
            self.root.title("Choose your directories")
            ttk.Button(
                self.root, text="Directory of results CSVs",
                command=lambda: self.set_path_res_dir_field()
                ).grid(row=1, ipadx=5, ipady=15)
            ttk.Entry(
                self.root, textvariable=self.input_text_res_dir,
                width=70
                ).grid(row=1, column=1, ipadx=1, ipady=1)
            ttk.Button(
                self.root, text="Directory of standings CSVs",
                command=lambda: self.set_path_sta_dir_field()
                ).grid(row=2, ipadx=5, ipady=15)
            ttk.Entry(
                self.root, textvariable=self.input_text_sta_dir, width=70
                ).grid(row=2, column=1, ipadx=1, ipady=1)

        ttk.Button(
            self.root, text="Accept", command=root.destroy
                  ).grid(row=3, ipadx=5, ipady=15)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()
            sys.exit('Quitting...')

    def set_path_res_field(self):
        """ Function sets the results CSV file text to the box."""
        self.path_res = askopenfilename(
            initialdir="./", title="Select results csv file"
            )
        self.input_text_res.set(self.path_res)

    def set_path_sta_field(self):
        """ Function sets the standings CSV file text to the box."""
        self.path_sta = askopenfilename(
            initialdir="./", title="Select standings csv file"
            )
        self.input_text_sta.set(self.path_sta)

    def set_path_res_dir_field(self):
        """ Function sets the directory text to the box."""
        self.path_dir_res = askdirectory(
            initialdir="./", title="Select directory of results CSV files"
            )
        self.input_text_res_dir.set(self.path_dir_res)

    def set_path_sta_dir_field(self):
        """ Function sets the standings directory text to the box."""
        self.path_dir_sta = askdirectory(
            initialdir="./", title="Select directory of standings CSV files"
            )
        self.input_text_sta_dir.set(self.path_dir_sta)


def create_or_update():
    root = tk.Tk()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit('Quitting...')

    def OnButtonClick(button_id):
        global button_ttc
        button_ttc = button_id
        root.destroy()
    w = 240  # width for the Tk root
    h = 180  # height for the Tk root
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title("Create or update")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    tk.Label(root, text="Do you want to create a new database,\n"
             + "or update an existing one?",
             justify=tk.CENTER,
             padx=20,
             pady=20).pack(fill=BOTH, expand=True)
    button1 = tk.Button(root, text="Create",
                        command=lambda *args: OnButtonClick(1))
    button1.pack(fill=BOTH, expand=True)
    button2 = tk.Button(root, text="Update",
                        command=lambda *args: OnButtonClick(2))
    button2.pack(fill=BOTH, expand=True)
    root.mainloop()
    return button_ttc


def results_or_standings():
    root = tk.Tk()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit('Quitting...')

    def OnButtonClick(button_id):
        global button_ttc
        button_ttc = button_id
        root.destroy()

    w = 240  # width for the Tk root
    h = 180  # height for the Tk root
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.title("Create or update")
    root.protocol("WM_DELETE_WINDOW", on_closing)
    tk.Label(root, text="Do you want to create the database of\n"
             + "results, standings or both?",
             justify=tk.CENTER,
             padx=20,
             pady=20).pack(fill=BOTH, expand=True)
    button1 = tk.Button(root, text="Results",
                        command=lambda *args: OnButtonClick(1))
    button1.pack(fill=BOTH, expand=True)
    button2 = tk.Button(root, text="Standings",
                        command=lambda *args: OnButtonClick(2))
    button2.pack(fill=BOTH, expand=True)
    button3 = tk.Button(root, text="Results and Standings",
                        command=lambda *args: OnButtonClick(3))
    button3.pack(fill=BOTH, expand=True)
    root.mainloop()
    return button_ttc


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


def year_or_league():
    root = tkinter.Tk()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit('Quitting...')

    def OnButtonClick(button_id):
        global button_ttc
        button_ttc = button_id
        root.destroy()

    w = 240  # width for the Tk root
    h = 180  # height for the Tk root
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.protocol("WM_DELETE_WINDOW", on_closing)
    tk.Label(root, text="Do you want to update a year\n"
             + "a whole league, the or the whole dataset?",
             justify=tk.CENTER,
             padx=20,
             pady=20).pack(fill=BOTH, expand=True)
    tk.Label(root, text="This is just a Test",
             justify=tk.CENTER,
             padx=20, pady=20,
             font=(None, 8, 'italic')).pack(fill=BOTH, expand=True)
    button1 = tk.Button(root, text="Single Year",
                        command=lambda *args: OnButtonClick(1))
    button1.pack(fill=BOTH, expand=True)
    button2 = tk.Button(root, text="Whole League",
                        command=lambda *args: OnButtonClick(2))
    button2.pack(fill=BOTH, expand=True)
    button3 = tk.Button(root, text="Whole Dataset",
                        command=lambda *args: OnButtonClick(3))
    button3.pack(fill=BOTH, expand=True)
    root.mainloop()
    return button_ttc
