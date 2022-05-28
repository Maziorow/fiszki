import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import messagebox as mb
import customtkinter as ctk ##Wigdet Text is not implemented here, use tk.Text instead
from ctypes import windll
import pandas as pd
import random
from dataclasses import dataclass
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl import load_workbook
from sys import exit

db = 'baza_slowek_polsko_angielskie.xlsx'

difficulty_list = ["łatwy","średni","trudne"]

@dataclass
class Word:
    english: str
    polish: str
    difficulty: str

class Logic():
    def __init__(self):
        self.formatted_base = []
        self.current_word = None
        self.words_base = pd.read_excel(db)
        for index, row in self.words_base.iterrows():
            self.formatted_base.append(Word(row['english'], row['polish'], row['difficulty']))
    def randNewWord(self):
        if len(self.formatted_base) == 0:
            return None
        self.current_word = random.randint(0,len(self.formatted_base)-1)
        return self.formatted_base[self.current_word].english
    def checkAnswer(self, input):
        if(self.formatted_base[self.current_word].polish != input):
            self.current_word = None
            return False
        else:
            self.formatted_base.pop(self.current_word)
            self.current_word = None
            return True

logic = Logic()
text = logic.randNewWord()


class SampleApp(ctk.CTk):

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        windll.shcore.SetProcessDpiAwareness(1)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = ctk.CTkFrame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, AddWordPage):
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


class StartPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
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

        label = ctk.CTkLabel(self, text="Fiszki polsko-angielskie")
        label.pack(side="top", fill="x", pady=10)

        button1 = ctk.CTkButton(self, text="Do fiszek",
                            command=lambda: controller.show_frame("PageOne"))
        button1.pack()

        button2 = ctk.CTkButton(self, text="Dodaj słowo",
                            command=lambda: controller.show_frame("AddWordPage"))
        button2.pack()

class PageOne(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        button = ctk.CTkButton(self, text="Powrót do głównego menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        T1 = ctk.CTkEntry(self, height=1, width=200)
        T1.insert(ctk.END, text)
        T1.config(state='disable')
        T1.place(x=50,y=378)

        T2 = ctk.CTkEntry(self, height=1, width=200)
        T2.place(x=800, y=378)

        button2 = ctk.CTkButton(self, text="Sprawdź odpowiedź", width=25, command=lambda: action(T1, T2))
        button2.place(x=500, y=450)


        def action(t1, t2):
            ans = logic.checkAnswer(T2.get())
            text = logic.randNewWord()
            if ans:
                mb.showwarning("Odpowiedź", "To poprawna odpowiedź!")
            else:
                mb.showerror("Odpowiedź", "Niestety, jest to niepoprawna odpowiedź!")
            T1.config(state='normal')
            T1.delete("0","end")
            T1.insert(ctk.END, text)
            T1.config(state='disable')
            T2.delete("0","end")
            T2.insert(ctk.END,'')

class AddWordPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        button = ctk.CTkButton(self, text="Powrót do głównego menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        label_polish = ctk.CTkLabel(self,text="Słowo po polsku", height=1, width=30)
        label_polish.place(x=100, y=328)
        polish_word = ctk.CTkEntry(self, height=1, width=200)
        polish_word.place(x=100, y=378)

        label_english = ctk.CTkLabel(self, text="Słowo po angielsku",height=1, width=25)
        label_english.place(x=400, y=328)
        english_word = ctk.CTkEntry(self, height=1, width=200)
        english_word.place(x=400, y=378)

        label_difficulty = ctk.CTkLabel(self, text="Poziom trudności", height=1, width=25)
        label_difficulty.place(x=700, y=328)
        difficulty_choice = ttk.Combobox(self,height=1,width=25,values=difficulty_list)
        difficulty_choice['state'] = 'readonly'
        difficulty_choice.insert(ctk.END,'')
        difficulty_choice.place(x=700,y=378)

        add_word = ctk.CTkButton(self, text="Dodaj słowo", corner_radius=6, width=25, command=lambda: add_word(polish_word,english_word,difficulty_choice))
        add_word.place(x=400, y=460)

        def add_word(pl,en,diff):
            if pl.get('1.0','end-1c') and en.get('1.0','end-1c') and diff.get():
                try:
                    new_word = pd.DataFrame([{'polish':pl.get('1.0','end-1c'), 'english':en.get('1.0','end-1c'), 'difficulty':diff.get()}])
                    wb = load_workbook(filename = "baza_slowek_polsko_angielskie.xlsx")
                    ws = wb["Arkusz1"]
                    for r in dataframe_to_rows(new_word, index=False, header=False):
                        ws.append(r)
                    wb.save("baza_slowek_polsko_angielskie.xlsx")
                    mb.showwarning("Informacja", "Poprawnie dodano nowe słowo!")
                    pl.delete("0", 'end')
                    pl.insert(ctk.END,"")
                    en.delete("0", 'end')
                    en.insert(ctk.END,"")
                    diff.set('')
                except:
                    mb.showerror("Informacja", "Błąd")
            else:
                mb.showerror("Informacja", "Błąd w wprowadzaniu danych!")


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()



