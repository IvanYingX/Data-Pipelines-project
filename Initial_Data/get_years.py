import tkinter as tk
from tkinter import messagebox
import sys

def get_initial_year():
        root = tk.Tk()

        def on_closing():
                if messagebox.askokcancel("Quit", "Do you want to quit?"):
                        root.destroy()
                        sys.exit('Quitting...')
                
        root.protocol("WM_DELETE_WINDOW", on_closing)
        v = tk.IntVar()
        back = tk.BooleanVar()
        back.set(False)
        root.title("Initial Year")
        label = tk.Label(root, 
                text="""Select the initial year you want to extract data from""",
                justify = tk.LEFT, font=("Arial", 14), padx = 5, pady = 10).grid(row=0, column=0, columnspan=2)
        slider = tk.Scale(root, from_= 1990, to = 2020, variable=v, orient=tk.HORIZONTAL, 
                        length=300, tickinterval=5, width=10).grid(row=1, column=0, columnspan=2)
        tk.Radiobutton(root, text="Confirm", indicatoron = 0, width = 10, relief=tk.FLAT, value=True, command=root.destroy).grid(row=2, column=1, pady=10)
        tk.Radiobutton(root, text="Go Back", indicatoron = 0, width = 10, relief=tk.FLAT, variable=back, value=True, command=root.destroy).grid(row=2, column=0, pady=10)
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
                
        root.protocol("WM_DELETE_WINDOW", on_closing)

        v = tk.IntVar()
        back = tk.BooleanVar()
        root.title("Final Year")
        label = tk.Label(root, 
                text="""Select the final year you want to extract data from""",
                justify = tk.LEFT, font=("Arial", 14), padx = 5, pady = 10).grid(row=0, column=0, columnspan=2)
        slider = tk.Scale(root, from_= year_1, to = 2020, variable=v, orient=tk.HORIZONTAL, 
                        length=300, tickinterval=5, width=10).grid(row=1, column=0, columnspan=2)
        tk.Radiobutton(root, text="Confirm", indicatoron = 0, width = 10, relief=tk.FLAT, value=True, command=root.destroy).grid(row=2, column=1, pady=10)
        tk.Radiobutton(root, text="Go Back", indicatoron = 0, width = 10, relief=tk.FLAT, variable=back, value=True, command=root.destroy).grid(row=2, column=0, pady=10)
        root.mainloop()
        if back.get():
                return -1
        return v.get()