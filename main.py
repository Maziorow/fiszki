import tkinter as tk
from tkinter import font as tkfont
from ctypes import windll
import pandas as pd
import random

df = pd.read_excel (r'baza_slowek_polsko_angielskie.xlsx')

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        windll.shcore.SetProcessDpiAwareness(1)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # put all of the pages in the same location;
            # the one on the top of the stacking order
            # will be the one that is visible.
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # title and icon of the application
        controller.title("Fiszki polsko-angielskie")
        controller.iconbitmap("pictures/xp_uk.ico")

        window_width = 1024
        window_height = 768
        screen_width = controller.winfo_screenwidth()
        screen_height = controller.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        controller.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        label = tk.Label(self, text="This is the start page", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Go to Page One",
                            command=lambda: controller.show_frame("PageOne"))
        button1.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Go to the start page",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()
        T = tk.Text(self, height=2, width=30)
        T.insert(tk.END, df.iat[random.randint(0, 99), 0])
        T.pack()



'''

root = tk.Tk()




tk.mainloop()
'''




#message = tk.Label(root, text="Hello world!")
#message.pack()

if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()



