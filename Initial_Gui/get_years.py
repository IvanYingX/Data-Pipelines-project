import tkinter as tk
from tkinter import messagebox
import sys


def get_initial_year():
    root = tk.Tk()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit('Quitting...')

    w = 400  # width for the Tk root
    h = 150  # height for the Tk root
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.protocol("WM_DELETE_WINDOW", on_closing)
    v = tk.IntVar()
    back = tk.BooleanVar()
    back.set(False)
    root.title("Initial Year")
    tk.Label(
        root,
        text="""Select the initial year you want to extract data from""",
        justify=tk.CENTER, font=("Arial", 12),
        padx=5, pady=10
        ).pack(fill=tk.BOTH, expand=True)
    tk.Scale(
        root, from_=1990, to=2021,
        variable=v, orient=tk.HORIZONTAL,
        length=300, tickinterval=5, width=10
        ).pack(fill=tk.BOTH, expand=True)
    tk.Radiobutton(
        root, text="Confirm", indicatoron=0,
        width=10, relief=tk.FLAT, value=True,
        command=root.destroy
        ).pack(fill=tk.BOTH, expand=True)
    tk.Radiobutton(
        root, text="Go Back", indicatoron=0,
        width=10, relief=tk.FLAT, variable=back,
        value=True, command=root.destroy
        ).pack(fill=tk.BOTH, expand=True)
    root.mainloop()
    if back.get():
        return -1
    return v.get()


def get_final_year(year_1):
    root = tk.Tk()

    def on_closing():
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            root.destroy()
            sys.exit('Quitting...')

    w = 400  # width for the Tk root
    h = 150  # height for the Tk root
    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.protocol("WM_DELETE_WINDOW", on_closing)

    v = tk.IntVar()
    back = tk.BooleanVar()
    root.title("Final Year")
    tk.Label(root,
             text="""Select the final year you want to extract data from""",
             justify=tk.LEFT, font=("Arial", 12),
             padx=5, pady=10).pack(fill=tk.BOTH, expand=True)
    tk.Scale(
        root, from_=year_1, to=2021,
        variable=v, orient=tk.HORIZONTAL,
        length=300, tickinterval=5, width=10
        ).pack(fill=tk.BOTH, expand=True)
    tk.Radiobutton(
        root, text="Confirm", indicatoron=0,
        width=10, relief=tk.FLAT, value=True,
        command=root.destroy
        ).pack(fill=tk.BOTH, expand=True)
    tk.Radiobutton(
        root, text="Go Back", indicatoron=0,
        width=10, relief=tk.FLAT, variable=back,
        value=True, command=root.destroy
        ).pack(fill=tk.BOTH, expand=True)
    root.mainloop()
    if back.get():
        return -1
    return v.get()
