import tkinter as tk
from ctypes import windll
import pandas as pd
import random

class MainWindow():
    def __init__(self, df):
        windll.shcore.SetProcessDpiAwareness(1)
        root = tk.Tk()
        root.title("Fiszki polsko-angielskie")
        window_width = 1024
        window_height = 768
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        root.iconbitmap("pictures/xp_uk.ico")
        T = tk.Text(root, height=2, width=30)
        T.pack()
        T.insert(tk.END, df.iat[random.randint(0,100),0])
        tk.mainloop()

df = pd.read_excel (r'baza_slowek_polsko_angielskie.xlsx')
MainWindow(df) #creates main window of the


#message = tk.Label(root, text="Hello world!")
#message.pack()



