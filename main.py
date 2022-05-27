import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import messagebox as mb
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

        label = tk.Label(self, text="Fiszki polsko-angielskie", font=controller.title_font)
        label.pack(side="top", fill="x", pady=10)

        button1 = tk.Button(self, text="Do fiszek",
                            command=lambda: controller.show_frame("PageOne"))
        button1.pack()

        button2 = tk.Button(self, text="Dodaj słowo",
                            command=lambda: controller.show_frame("AddWordPage"))
        button2.pack()

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Powrót do głównego menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        T1 = tk.Text(self, height=1, width=30)
        T1.tag_configure("center", justify='center')
        T1.insert(tk.END, text)
        T1.tag_add("center", "1.0", "end")
        T1.config(state='disable')
        T1.place(x=50,y=378)

        T2 = tk.Text(self, height=1, width=30)
        T2.insert(tk.END,'')
        T2.place(x=800, y=378)

        button2 = tk.Button(self, text="Sprawdź odpowiedź", width=30, command=lambda: action(T1, T2))
        button2.place(x=500, y=450)


        def action(t1, t2):
            ans = logic.checkAnswer(T2.get('1.0','end-1c'))
            text = logic.randNewWord()
            if ans:
                mb.showwarning("Odpowiedź", "To poprawna odpowiedź!")
            else:
                mb.showerror("Odpowiedź", "Niestety, jest to niepoprawna odpowiedź!")
            T1.config(state='normal')
            T1.delete(1.0, 'end')
            T1.insert(tk.END, text)
            T1.config(state='disable')
            T2.delete(1.0, 'end')
            T2.insert(tk.END,'')

class AddWordPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        button = tk.Button(self, text="Powrót do głównego menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.pack()

        polish_word = tk.Text(self, height=1, width=30)
        polish_word.insert(tk.END, '')
        polish_word.place(x=100, y=378)

        english_word = tk.Text(self, height=1, width=30)
        english_word.insert(tk.END, '')
        english_word.place(x=400, y=378)

        difficulty_choice = ttk.Combobox(self,height=1,values=difficulty_list)
        difficulty_choice['state'] = 'readonly'
        difficulty_choice.insert(tk.END,'')
        difficulty_choice.place(x=700,y=378)

        add_word = tk.Button(self, text="Dodaj słowo", width=30, command=lambda: add_word(polish_word,english_word,difficulty_choice))
        add_word.place(x=400, y=460)

        def add_word(pl,en,diff): #TODO: popraw kolejność dodawania słów po polsku i po angielsku
            if pl.get('1.0','end-1c') and en.get('1.0','end-1c') and diff.get():
                try:
                    new_word = pd.DataFrame([{'english':en.get('1.0','end-1c'), 'polish':pl.get('1.0','end-1c'), 'difficulty':diff.get()}])
                    wb = load_workbook(filename = "baza_slowek_polsko_angielskie.xlsx")
                    ws = wb["Arkusz1"]
                    for r in dataframe_to_rows(new_word, index=False, header=False):
                        ws.append(r)
                    wb.save("baza_slowek_polsko_angielskie.xlsx")
                    mb.showwarning("Informacja", "Poprawnie dodano nowe słowo!")
                    pl.delete(1.0, 'end')
                    pl.insert(tk.END,"")
                    en.delete(1.0, 'end')
                    en.insert(tk.END,"")
                    diff.set('')
                except:
                    mb.showerror("Informacja", "Błąd")
            else:
                mb.showerror("Informacja", "Błąd w wprowadzaniu danych!")


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()



