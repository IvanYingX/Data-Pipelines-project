import tkinter
from tkinter import ttk, StringVar
from tkinter.filedialog import askopenfilename, askdirectory
import sys
from tkinter import messagebox


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

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.resizable(0, 0)  # This prevents from resizing the window
        self.root.geometry("700x300")

        if is_file:
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
        else:
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


def file_or_dir():
    root = tkinter.Tk()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit('Quitting...')

    root.protocol("WM_DELETE_WINDOW", on_closing)
    v = tkinter.BooleanVar()
    w = tkinter.BooleanVar()
    tkinter.Label(
        root, text="""Do you want to choose a file, or a directory?""",
        justify=tkinter.LEFT, padx=20
        ).grid(row=0, column=0)
    tkinter.Radiobutton(
        root, text="File", indicatoron=0, width=30,
        padx=20, variable=v, value=1, command=root.destroy
        ).grid(row=2, column=0)
    tkinter.Radiobutton(
        root, text="Directory", indicatoron=0,
        width=30, padx=20, variable=w, value=1, command=root.destroy
        ).grid(row=3, column=0)
    root.mainloop()
    return v.get()
