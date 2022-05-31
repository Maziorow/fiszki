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
import time

#db = 'baza_slowek_polsko_angielskie.xlsx'
db = 'jd.xlsx'

difficulty_list = ["łatwy","średni","trudne"]

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

@dataclass
class Word:
    english: str
    polish: str
    difficulty: str

class Logic():
    def __init__(self):
        self.formatted_base = []
        self.current_word = None
        self.number_of_words = None
        self.number_of_guessed = 0
        self.number_of_mistakes = 0
        self.words_base = pd.read_excel(db)
        self.start_time = None
        self.end_time = None
        self.time_elapsed = None
        self.learn_mode = None
    def newBase(self, diff=None):
        if diff == None:
            for index, row in self.words_base.iterrows():
                self.formatted_base.append(Word(row['english'], row['polish'], row['difficulty']))
        else:
            for index, row in self.words_base.iterrows():
                if row['difficulty'] == diff:
                    self.formatted_base.append(Word(row['english'], row['polish'], row['difficulty']))
        self.number_of_words = len(self.formatted_base)
    def clearAnswers(self):
        self.formatted_base = []
        self.current_word = 0
        self.number_of_guessed = 0
        self.number_of_mistakes = 0
    def randNewWord(self):
        if len(self.formatted_base) == 0:
            return False
        self.current_word = random.randint(0,len(self.formatted_base)-1)
        return True
    def checkAnswer(self, input):
        if(self.formatted_base[self.current_word].polish != input):
            self.current_word = 0
            if(self.learn_mode):
                self.formatted_base.pop(self.current_word)
                #self.number_of_guessed += 1
            return False
        else:
            self.formatted_base.pop(self.current_word)
            self.current_word = 0
            self.number_of_guessed += 1
            return True
    def getCurrentWord(self):
        if self.current_word != None:
            return self.formatted_base[self.current_word].english
        else:
            return "ERROR"
    def getCounter(self):
        return "Ilość słów: "+str(self.number_of_guessed)+"/"+str(self.number_of_words)
    def startTimer(self):
        self.start_time = time.time()
    def stopTimer(self):
        self.end_time = time.time()
    def showTime(self):
        sec = self.end_time - self.start_time
        mins = sec // 60
        sec = round(sec % 60, 2)
        return ("{0}:{1}".format(int(mins),sec))


class SampleApp(ctk.CTk):

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        windll.shcore.SetProcessDpiAwareness(1)

        self.title_font = tkfont.Font(family='Helvetica', size=72, weight="bold", slant="italic")

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
        window_height = 400
        screen_width = controller.winfo_screenwidth()
        screen_height = controller.winfo_screenheight()
        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)
        controller.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        label = ctk.CTkLabel(self, text="Fiszki polsko-angielskie",text_font=("Bank Gothic Medium BT", 40))
        label.place(relx=0.1,rely=0.1,relheight=0.1,relwidth=0.8)

        button1 = ctk.CTkButton(self, text="Tryb nauki",
                            command=lambda: chooseDifficulty())
        button1.place(relx=0.01,rely=0.5,relheight=0.1,relwidth=0.3)

        button2 = ctk.CTkButton(self, text="Dodaj słowo",
                            command=lambda: controller.show_frame("AddWordPage"))
        button2.place(relx=0.69,rely=0.5,relheight=0.1,relwidth=0.3)

        button3 = ctk.CTkButton(self, text="Sprawdź swoją wiedzę",
                                command=lambda: createToplevel())
        button3.place(relx=0.35,rely=0.5,relheight=0.1,relwidth=0.3)

        exit_button = ctk.CTkButton(self, text="Zamknij aplikację",command=lambda: exit())
        exit_button.place(relx=0.35,rely=0.75,relheight=0.1,relwidth=0.3)

        def createToplevel():
            self.window = ctk.CTkToplevel(self)
            self.window.grab_set()
            self.window.geometry("400x50")
            self.window.title("Wybierz poziom trudności")

            button_easy = ctk.CTkButton(self.window,text="Łatwy",command=lambda: closeToplevel("łatwy",False))
            button_easy.place(relx=0.01,rely=0.25,relheight=0.6,relwidth=0.3)
            button_medium = ctk.CTkButton(self.window,text="Średni",command=lambda: closeToplevel("średni",False))
            button_medium.place(relx=0.35,rely=0.25,relheight=0.6,relwidth=0.3)
            button_hard = ctk.CTkButton(self.window,text="Trudny",command=lambda: closeToplevel("trudne",False))
            button_hard.place(relx=0.69,rely=0.25,relheight=0.6,relwidth=0.3)

            def closeToplevel(diff,learn_mode):
                chooseDifficulty(diff,learn_mode)
                self.window.destroy()


        def chooseDifficulty(diff=None,learn_mode=True):
            logic.newBase(diff)
            logic.randNewWord()
            logic.learn_mode = learn_mode
            app.frames["PageOne"].T1.config(state='normal')
            app.frames["PageOne"].T1.delete("0", "end")
            app.frames["PageOne"].T1.insert(ctk.END, logic.getCurrentWord())
            app.frames["PageOne"].T1.config(state='disable')
            app.frames["PageOne"].counter.config(text=logic.getCounter())
            logic.startTimer()
            app.show_frame("PageOne")

logic = Logic()

class PageOne(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        button = ctk.CTkButton(self, text="Powrót do głównego menu",
                           command=lambda: close_window())
        button.place(relx=0.4,rely=0.89,relheight=0.1,relwidth=0.2)

        self.T1 = ctk.CTkEntry(self, height=1, width=200,fg_color="#D3D3D3",text_color="#000000",corner_radius=8)
        self.T1.insert(ctk.END, str(logic.getCurrentWord()))
        self.T1.config(state='disable')
        self.T1.place(relx=0.15,rely=0.6,relheight=0.05,relwidth=0.3)

        T2 = ctk.CTkEntry(self, height=1, width=200,fg_color="#D3D3D3",text_color="#000000",corner_radius=8)
        T2.place(relx=0.55,rely=0.6,relheight=0.05,relwidth=0.3)

        translate = ctk.CTkLabel(self,text="Tłumaczenie")
        translate.place(relx=0.55,rely=0.45,relheight=0.1,relwidth=0.3)

        button2 = ctk.CTkButton(self, text="Sprawdź odpowiedź", width=25, command=lambda: checkAnswer(self.T1,self.counter))
        button2.place(relx=0.4,rely=0.78,relheight=0.1,relwidth=0.2)


        self.counter = ctk.CTkLabel(self,text=logic.getCounter(),text_font=("Arial", 20))
        self.counter.place(relx=0.35,rely=0.15,relheight=0.1,relwidth=0.3)


        def updateEntries(T1,counter):
            T1.config(state='normal')
            T1.delete("0", "end")
            T1.insert(ctk.END, logic.getCurrentWord())
            T1.config(state='disable')
            T2.delete("0", "end")
            T2.insert(ctk.END, '')
            counter.config(text=logic.getCounter())

        def clearEntries(T1,counter):
            T1.config(state='normal')
            T1.delete("0", "end")
            T1.insert(ctk.END, "")
            T1.config(state='disable')
            T2.delete("0", "end")
            T2.insert(ctk.END, '')
            counter.config(text=logic.getCounter())

        def checkAnswer(T1,counter):
            word_index = logic.current_word
            ans = logic.checkAnswer(T2.get())
            if len(logic.formatted_base) == 0:
                logic.stopTimer()
                def createToplevel():
                    self.window = ctk.CTkToplevel(self)
                    self.window.grab_set()
                    self.window.geometry("400x200")
                    self.window.title("")

                    napis = ctk.CTkLabel(self.window,text="Liczba poprawnych odpowiedzi " + str(logic.number_of_guessed) + '/' + str(logic.number_of_words))
                    napis.place(relx=0.15,rely=0.2,relheight=0.1,relwidth=0.7)

                    czas = ctk.CTkLabel(self.window,text="Czas rozwiązania: " + logic.showTime())
                    czas.place(relx=0.15,rely=0.32,relheight=0.1,relwidth=0.7)

                    button_medium = ctk.CTkButton(self.window, text="Wróc do menu",
                                                  command=lambda: closeToplevel())
                    button_medium.place(relx=0.15,rely=0.82,relheight=0.1,relwidth=0.7)
                    close_window()
                    def closeToplevel():
                        self.window.destroy()
                createToplevel()
                clearEntries(T1, counter)
            else:
                if ans:
                    def createToplevel():
                        self.window = ctk.CTkToplevel(self)
                        self.window.grab_set()
                        self.window.geometry("400x200")
                        self.window.title("")

                        napis = ctk.CTkLabel(self.window, text="Poprawna odpowiedź!")
                        napis.place(relx=0.15,rely=0.2,relheight=0.1,relwidth=0.7)

                        button_medium = ctk.CTkButton(self.window, text="Kontynuuj",
                                                      command=lambda: closeToplevel())
                        button_medium.place(relx=0.15,rely=0.82,relheight=0.1,relwidth=0.7)

                        def closeToplevel():
                            self.window.destroy()

                    createToplevel()
                else:
                    def createToplevel():
                        self.window = ctk.CTkToplevel(self)
                        self.window.grab_set()
                        self.window.geometry("400x200")
                        self.window.title("")
                        self.message = ''

                        if logic.learn_mode:
                            self.message = "Poprawne tłumaczenie to " + logic.formatted_base[word_index].polish
                        else:
                            self.message = "Niepoprawne tłumaczenie"

                        napis = ctk.CTkLabel(self.window, text=self.message)
                        napis.place(relx=0.15,rely=0.2,relheight=0.1,relwidth=0.7)

                        button_medium = ctk.CTkButton(self.window, text="Kontynuuj",
                                                      command=lambda: closeToplevel())
                        button_medium.place(relx=0.15,rely=0.82,relheight=0.1,relwidth=0.7)

                        def closeToplevel():
                            self.window.destroy()

                    createToplevel()
                logic.randNewWord()
                updateEntries(T1, counter)


        def close_window():
            logic.stopTimer()
            controller.show_frame("StartPage")
            self.update()
            logic.clearAnswers()

class AddWordPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        button = ctk.CTkButton(self, text="Powrót do głównego menu",
                           command=lambda: controller.show_frame("StartPage"))
        button.place(relx=0.4,rely=0.89,relheight=0.1,relwidth=0.2)

        label_polish = ctk.CTkLabel(self,text="Słowo po polsku", height=1, width=30)
        label_polish.place(relx=0.10,rely=0.4,relheight=0.05,relwidth=0.25)
        polish_word = ctk.CTkEntry(self, height=1, width=200,fg_color="#D3D3D3",text_color="#000000")
        polish_word.place(relx=0.10,rely=0.6,relheight=0.1,relwidth=0.25)

        label_english = ctk.CTkLabel(self, text="Słowo po angielsku",height=1, width=25)
        label_english.place(relx=0.375,rely=0.4,relheight=0.05,relwidth=0.25)
        english_word = ctk.CTkEntry(self, height=1, width=200,fg_color="#D3D3D3",text_color="#000000")
        english_word.place(relx=0.375,rely=0.6,relheight=0.1,relwidth=0.25)

        label_difficulty = ctk.CTkLabel(self, text="Poziom trudności", height=1, width=25)
        label_difficulty.place(relx=0.650,rely=0.4,relheight=0.05,relwidth=0.25)
        difficulty_choice = ttk.Combobox(self,height=1,width=25,values=difficulty_list)
        difficulty_choice['state'] = 'readonly'
        difficulty_choice.insert(ctk.END,'')
        difficulty_choice.place(relx=0.65,rely=0.625,relheight=0.05,relwidth=0.25)

        add_word = ctk.CTkButton(self, text="Dodaj słowo", corner_radius=6, width=25, command=lambda: add_word(polish_word,english_word,difficulty_choice))
        add_word.place(relx=0.4,rely=0.78,relheight=0.1,relwidth=0.2)

        def add_word(pl,en,diff):
            if pl.get() and en.get() and diff.get():
                try:
                    new_word = pd.DataFrame([{'polish':pl.get(), 'english':en.get(), 'difficulty':diff.get()}])
                    wb = load_workbook(filename = "baza_slowek_polsko_angielskie.xlsx")
                    ws = wb["Arkusz1"]
                    for r in dataframe_to_rows(new_word, index=False, header=False):
                        ws.append(r)
                    wb.save("baza_slowek_polsko_angielskie.xlsx")
                    pl.delete("0", 'end')
                    pl.insert(ctk.END,"")
                    en.delete("0", 'end')
                    en.insert(ctk.END,"")
                    diff.set('')
                    def createToplevel():
                        self.window = ctk.CTkToplevel(self)
                        self.window.grab_set()
                        self.window.geometry("400x200")
                        self.window.title("")

                        napis = ctk.CTkLabel(self.window, text="Dodano słowo")
                        napis.place(relx=0.15,rely=0.2,relheight=0.1,relwidth=0.7)

                        button_medium = ctk.CTkButton(self.window, text="Kontynuuj",
                                                      command=lambda: closeToplevel())
                        button_medium.place(relx=0.15,rely=0.82,relheight=0.1,relwidth=0.7)

                        def closeToplevel():
                            self.window.destroy()

                    createToplevel()
                except:
                    def createToplevel():
                        self.window = ctk.CTkToplevel(self)
                        self.window.grab_set()
                        self.window.geometry("400x200")
                        self.window.title("")

                        napis = ctk.CTkLabel(self.window, text="Błąd!")
                        napis.place(relx=0.15, rely=0.2, relheight=0.1, relwidth=0.7)

                        button_medium = ctk.CTkButton(self.window, text="Kontynuuj",
                                                      command=lambda: closeToplevel())
                        button_medium.place(relx=0.15, rely=0.82, relheight=0.1, relwidth=0.7)

                        def closeToplevel():
                            self.window.destroy()

                    createToplevel()
            else:
                def createToplevel():
                    self.window = ctk.CTkToplevel(self)
                    self.window.grab_set()
                    self.window.geometry("400x200")
                    self.window.title("")

                    napis = ctk.CTkLabel(self.window, text="Niepoprawnie wprowadzone dane!")
                    napis.place(relx=0.15, rely=0.2, relheight=0.1, relwidth=0.7)

                    button_medium = ctk.CTkButton(self.window, text="Kontynuuj",
                                                  command=lambda: closeToplevel())
                    button_medium.place(relx=0.15, rely=0.82, relheight=0.1, relwidth=0.7)

                    def closeToplevel():
                        self.window.destroy()

                createToplevel()


if __name__ == "__main__":
    app = SampleApp()
    app.mainloop()



