#!/usr/bin/env python
# -*- coding: utf-8 -*-
# https://www.python-forum.de/viewtopic.php?t=42239

# wichtige debug var 1342 MouseMover select
#print(blockPositionFokus)

import tkinter as tk
from tkinter.constants import BOTH, END, LEFT, RIGHT, TOP, VERTICAL, X
import tkinter.ttk
import tkinter.messagebox
import tkinter.filedialog
import tkinter.simpledialog
import os
import json
#from time import sleep
from PIL import Image, ImageTk
import copy
import time
from funktionen import compelier

TITLE = "pyblockplc v1.0"
TITLE_ICO = "..."
TITLE_IMAGE = "play_button.png"
MAIN_WIN_WIDTH = 1024
MAIN_WIN_HEIGHT = 768

#1024x768
#1920x1080

state_x = [0]
state_y = [0]


#tonTyp = {'in1': '', 'paramter': '', 'startTime': 0, 'actualTime': 0, 'setTime': 0, 'isWork': '0'}

ton = {}
'''item = {}
for number in range(1, 10):
    item[('TON'+ str(number))] = {}
    item[('TON'+ str(number))] = dict(tonTyp)
    ton.update(item)'''

#tofTyp = {'in1': '', 'paramter': '', 'startTime': 0, 'actualTime': 0, 'setTime': 0, 'isWork': '0'}

tof = {}
'''item = {}
for numberTof in range(1, 10):
    item[('TOF'+ str(numberTof))] = {}
    item[('TOF'+ str(numberTof))] = dict(tofTyp)
    tof.update(item)'''

#countTyp = {'presetValue': 0, 'setValue': 0, 'actualValue': 0,
            #'countUpFlanke': '0', 'countDownFlanke': '0', 'init': '0'}
cud = {}
'''item = {}
for numberCud in range(1, 10):
    item[('CUD'+ str(numberCud))] = {}
    item[('CUD'+ str(numberCud))] = dict(countTyp)
    cud.update(item)'''

sr = {}
'''for nummer in range(1, 20):
    item = {('SR' + str(nummer)): '0'}
    sr.update(item)'''

ip = {}
'''for nummer in range(1, 20):
    item = {('IP' + str(nummer)): '0'}
    ip.update(item)'''

mw = {}
'''for nummer in range(1, 20):
    item = {('MW' + str(nummer)): 0}
    mw.update(item)'''

# init Programm hochlauf
block = {}
'''for nummer in range(1, 100):
    item = {('B' + str(nummer)): '0'}
    block.update(item)'''

comment = {}
for nummer in range(1, 200):
    item = {('C' + str(nummer)): ''}
    comment.update(item)

#block = {'B1': '0', 'B2': '0', 'B3': '0', 'B4': '0', 'B5': '0', 'B6': '0', 'B7': '0', 'B8': '0', 'B9': '0',
                                                     #'B10': '0', 'B11': '0', 'B12': '0', 'B13': '0', 'B14': '0'}
#input = {'I1': '1', 'I2': '1', 'I3': '0', 'I4': '1', 'I5': '1', 'I6': '0', 'I7': '1', 'I8': '0'}
#output = {'Q1': '0', 'Q2': '0', 'Q3': '0', 'Q4': '0', 'Q5': '0', 'Q6': '0', 'Q7': '0', 'Q8': '0'}
input = {}
output = {}

# Block Program
sd = [{'B1':'ZUW', 'OUT':'Q1', 'IN1': 'B2'}, {'B2':'OR', 'OUT':'B1-I1', 'IN1': 'B3', 'IN2': 'B6'},
                                            {'B6':'INPUT', 'OUT':'B2-I2', 'IN1': 'I6'},
                                            {'B3':'AND', 'OUT':'B2-I1', 'IN1': 'B4', 'IN2': 'B5', 'IN3': 'B7'},
                                            {'B4':'INPUT', 'OUT':'B3-I1', 'IN1': 'I4'},
                                            {'B5':'INPUT', 'OUT':'B3-I2', 'IN1': 'I5'},
                                            {'B7':'INPUT', 'OUT':'B3-I3', 'IN1': 'I3'}]
sd2 = copy.deepcopy(sd)

# Blöcke die gerniert werden
blocks = []
lines = []
comments = []
blockFokusInput = 0
blockPositionFokus = [0, 0, '', '']  # x, y, blockNR , in1 oder in2 vom Markieten Eingang
letzterBlockNr = ''
blocksQuelle = []
blockProgram = []

#daten von File
blocksVonFile = []
linesVonFile = []
commentsVonFile = []
pageVonFile = []

# Page daten
page1 = []
page2 = []
page3 = []
page4 = []
page5 = []
page6 = []
pageFokus = 0

# Read config File
configDaten = {}
uploadPathExe = ''
try:
    with open('config.txt' , 'r') as fp:
                configDaten = json.load(fp)
except:
    pass
if configDaten:
    if 'uploadPathExe' in configDaten:
        uploadPathExe = configDaten['uploadPathExe']


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    https://stackoverflow-com.translate.goog/questions/3221956/how-do-i-display-tooltips-in-tkinter?_x_tr_sl=en&_x_tr_tl=de&_x_tr_hl=de&_x_tr_pto=nui,sc
    """
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None

    def enter(self, event=None):
        self.schedule()

    def leave(self, event=None):
        self.unschedule()
        #self.tw = tk.Toplevel(self.widget) #vorschlag wenn sich tooltip aufhägt
        self.hidetip()

    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)

    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)

    def showtip(self, event=None):
        x = y = 0
        x, y, cx, cy = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 20
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
                       background="#ffffff", relief='solid', borderwidth=1,
                       wraplength = self.wraplength)
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw= None
        if tw:
            tw.destroy()

class MainWindowFrame(object):
    def __init__(self, parent):
        self.parent = parent
        self.tk = tk

        #Menue Button
        self.menu_frame = tkinter.ttk.LabelFrame(parent.main_win)
        self.menu_frame.pack(side=TOP, fill=X)
        #self.ribbon = Ribbon.TabRibbonFrame(self)
		#self.ribbon.pack(side=TOP, fill=X)

        # Main frame
        self.paned = tkinter.ttk.PanedWindow(parent.main_win, orient='horizontal')
        self.paned.pack(fill='both', expand='yes')

        # --- Left side ---
        frame = tkinter.ttk.Frame(self.paned)
        self.paned.add(frame)

        # Taps
        self.note = tkinter.ttk.Notebook(frame)
        self.tab1 = tkinter.ttk.Frame(self.note)
        self.tab2 = tkinter.ttk.Frame(self.note)
        self.tab3 = tkinter.ttk.Frame(self.note)
        self.note.add(self.tab1, text="Logic")
        self.note.add(self.tab2, text="Simulator") #'I/O'
        self.note.add(self.tab3, text="File")
        self.note.pack(fill='both', expand='yes', padx=4, pady=2)
        self.note.configure(width=220)
        

        
        #frame1 = tkinter.ttk.Frame(self.paned)
        #self.paned.add(frame1)
        #self.frame1 = tk.Frame(frame1, relief="ridge")
        #self.frame1.pack(side=TOP)
        #self.frame1.configure(width=40)

        frame2 = tkinter.ttk.Frame(self.paned)
        self.paned.add(frame2)
        self.frame2 = tk.Frame(frame2, relief="ridge")
        self.frame2.pack(fill='both', expand='yes')


        #Titelbild & Icon
        #parent.main_win.iconbitmap(TITLE_ICO) # Für Windows

        #Zeichenwand
        #self.hintergrund = tk.PhotoImage(file="bild2.png")
        self.zeichenwand = tk.Canvas(self.frame2, relief='groove', borderwidth=2, bg='white')
        self.zeichenwand.pack(side=LEFT, fill='both', expand='yes')

        def clicked1(event):
            global pageFokus, blockPositionFokus
            pageFokus = 0
            blockPositionFokus = [0, 0, '', '']
            self.zeichenwand.itemconfig(self.buttonBG, fill="white")
            self.zeichenwand.itemconfig(self.buttonBG2, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG3, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG4, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG5, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG6, fill="grey80")
            self.parent.zeichnen_aktuelle_page1()
        def clicked2(event):
            global pageFokus, blockPositionFokus
            pageFokus = 1
            blockPositionFokus = [0, 0, '', '']
            self.zeichenwand.itemconfig(self.buttonBG, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG2, fill="white")
            self.zeichenwand.itemconfig(self.buttonBG3, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG4, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG5, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG6, fill="grey80")
            self.parent.zeichnen_aktuelle_page2()
        def clicked3(event):
            global pageFokus, blockPositionFokus
            pageFokus = 2
            blockPositionFokus = [0, 0, '', '']
            self.zeichenwand.itemconfig(self.buttonBG, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG2, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG3, fill="white")
            self.zeichenwand.itemconfig(self.buttonBG4, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG5, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG6, fill="grey80")
            self.parent.zeichnen_aktuelle_page3()
        def clicked4(event):
            global pageFokus, blockPositionFokus
            pageFokus = 3
            blockPositionFokus = [0, 0, '', '']
            self.zeichenwand.itemconfig(self.buttonBG, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG2, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG3, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG4, fill="white")
            self.zeichenwand.itemconfig(self.buttonBG5, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG6, fill="grey80")
            self.parent.zeichnen_aktuelle_page4()
        def clicked5(event):
            global pageFokus, blockPositionFokus
            pageFokus = 4
            blockPositionFokus = [0, 0, '', '']
            self.zeichenwand.itemconfig(self.buttonBG, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG2, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG3, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG4, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG5, fill="white")
            self.zeichenwand.itemconfig(self.buttonBG6, fill="grey80")
            self.parent.zeichnen_aktuelle_page5()
        def clicked6(event):
            global pageFokus, blockPositionFokus
            pageFokus = 5
            blockPositionFokus = [0, 0, '', '']
            self.zeichenwand.itemconfig(self.buttonBG, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG2, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG3, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG4, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG5, fill="grey80")
            self.zeichenwand.itemconfig(self.buttonBG6, fill="white")
            self.parent.zeichnen_aktuelle_page6()

        #https://stackoverflow.com/questions/11980812/how-do-you-create-a-button-on-a-tkinter-canvas
        self.buttonBG = self.zeichenwand.create_rectangle(0, 0, 70, 30, fill="white", outline="grey60")
        self.buttonTXT = self.zeichenwand.create_text(35, 15, text="Page 1")
        self.zeichenwand.tag_bind(self.buttonBG, "<Button-1>", clicked1) ## when the square is clicked runs function "clicked".
        self.zeichenwand.tag_bind(self.buttonTXT, "<Button-1>", clicked1) ## same, but for the text.
        
        self.buttonBG2 = self.zeichenwand.create_rectangle(70, 0, 140, 30, fill="grey80", outline="grey60")
        self.buttonTXT2 = self.zeichenwand.create_text(105, 15, text="Page 2")
        self.zeichenwand.tag_bind(self.buttonBG2, "<Button-1>", clicked2) ## when the square is clicked runs function "clicked".
        self.zeichenwand.tag_bind(self.buttonTXT2, "<Button-1>", clicked2) ## same, but for the text.

        self.buttonBG3 = self.zeichenwand.create_rectangle(140, 0, 210, 30, fill="grey80", outline="grey60")
        self.buttonTXT3 = self.zeichenwand.create_text(175, 15, text="Page 3")
        self.zeichenwand.tag_bind(self.buttonBG3, "<Button-1>", clicked3) ## when the square is clicked runs function "clicked".
        self.zeichenwand.tag_bind(self.buttonTXT3, "<Button-1>", clicked3) ## same, but for the text.

        self.buttonBG4 = self.zeichenwand.create_rectangle(210, 0, 280, 30, fill="grey80", outline="grey60")
        self.buttonTXT4 = self.zeichenwand.create_text(245, 15, text="Page 4")
        self.zeichenwand.tag_bind(self.buttonBG4, "<Button-1>", clicked4) ## when the square is clicked runs function "clicked".
        self.zeichenwand.tag_bind(self.buttonTXT4, "<Button-1>", clicked4) ## same, but for the text.
        
        self.buttonBG5 = self.zeichenwand.create_rectangle(280, 0, 350, 30, fill="grey80", outline="grey60")
        self.buttonTXT5 = self.zeichenwand.create_text(315, 15, text="Page 5")
        self.zeichenwand.tag_bind(self.buttonBG5, "<Button-1>", clicked5) ## when the square is clicked runs function "clicked".
        self.zeichenwand.tag_bind(self.buttonTXT5, "<Button-1>", clicked5) ## same, but for the text.

        self.buttonBG6 = self.zeichenwand.create_rectangle(350, 0, 420, 30, fill="grey80", outline="grey60")
        self.buttonTXT6 = self.zeichenwand.create_text(385, 15, text="Page 6")
        self.zeichenwand.tag_bind(self.buttonBG6, "<Button-1>", clicked6) ## when the square is clicked runs function "clicked".
        self.zeichenwand.tag_bind(self.buttonTXT6, "<Button-1>", clicked6) ## same, but for the text.

        # anzeige Progressbar neben Schaltflächen (Simulator EIN ist ein Progress bar sichtbar)
        self.runProgressbar_20 = self.zeichenwand.create_rectangle(425, 0, 443, 30, fill="white", outline="white")
        self.runProgressbar_40 = self.zeichenwand.create_rectangle(445, 0, 463, 30, fill="white", outline="white")
        self.runProgressbar_60 = self.zeichenwand.create_rectangle(465, 0, 483, 30, fill="white", outline="white")
        self.runProgressbar_80 = self.zeichenwand.create_rectangle(485, 0, 503, 30, fill="white", outline="white")
        self.runProgressbar_100 = self.zeichenwand.create_rectangle(505, 0, 523, 30, fill="white", outline="white")
        self.runProgressbar_text = self.zeichenwand.create_text(600, 15, fill="white", font="Times 20 italic bold"
                                                                , text="Simulator on")

        # Button oberhalb auf der Zeichnung ------------------------------------------------------------------------
        '''image = Image.open("icons/play_button.png")
        self.imgPlayButton2 = ImageTk.PhotoImage(image)  
        self.menuButton4 = tk.Button(self.menu_frame, text="Test1", image=self.imgPlayButton2, 
                                command=self.parent.laden_programm, width=10)
        self.menuButton4.config(image=self.imgPlayButton2 , width="30", height="30")
        #self.menuButton4.grid(row=0, column=0, padx=105, sticky="nw")
        self.menuButton4.pack(side=LEFT)

        image = Image.open("icons/stop_button.png")
        self.imgStopButton2 = ImageTk.PhotoImage(image)
        self.menuButton5 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.periodicCallOff, width=10) 
        self.menuButton5.config(image=self.imgStopButton2 , width="30", height="30")       
        #self.menuButton5.grid(row=0, column=0, padx=140, sticky="nw")
        self.menuButton5.pack(side=LEFT)'''

        image = Image.open("icons/datei_oeffnen_button.png")
        self.imgFileOpenButton = ImageTk.PhotoImage(image)  
        self.menuButton5 = tk.Button(self.menu_frame, text="Test1", image=self.imgFileOpenButton, 
                                command=self.parent.file_open, width=10)
        self.menuButton5.config(image=self.imgFileOpenButton , width="30", height="30")
        #self.menuButton5.grid(row=0, column=0, padx=175, sticky="nw")
        self.menuButton5.pack(side=LEFT)
        self.menuButton5_ttp = CreateToolTip(self.menuButton5, \
            'Open file. Only json format allowed. ')

        image = Image.open("icons/datei_speichern_als_button.png")
        self.imgFileCloseButton = ImageTk.PhotoImage(image)
        self.menuButton6 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.file_save_as, width=10) 
        self.menuButton6.config(image=self.imgFileCloseButton , width="30", height="30")       
        #self.menuButton6.grid(row=0, column=0, padx=210, sticky="nw")
        self.menuButton6.pack(side=LEFT)
        self.menuButton6_ttp = CreateToolTip(self.menuButton6, \
            'File save as. Only json format allowed. ')

        image = Image.open("icons/datei_speichern_button.png")
        self.imgFileSaveButton = ImageTk.PhotoImage(image)
        self.menuButtonSave = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.file_save, width=10) 
        self.menuButtonSave.config(image=self.imgFileSaveButton , width="30", height="30")       
        #self.menuButton6.grid(row=0, column=0, padx=210, sticky="nw")
        self.menuButtonSave.pack(side=LEFT)
        self.menuButtonSave_ttp = CreateToolTip(self.menuButtonSave, \
            'Save file, file must be selected beforehand. ')

        image = Image.open("icons/v_line.png")
        self.imgV_line3 = ImageTk.PhotoImage(image)
        self.menuButton9 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.v_line, width=10) 
        self.menuButton9.config(image=self.imgV_line3 , width="3", height="30")       
        self.menuButton9.pack(side=LEFT)

        image = Image.open("icons/delite_object_button.png")
        self.imgDeliteObjectButton = ImageTk.PhotoImage(image)
        self.menuButton7 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.del_object, width=10) 
        self.menuButton7.config(image=self.imgDeliteObjectButton , width="30", height="30")       
        #self.menuButton7.grid(row=0, column=0, padx=280, sticky="nw")
        self.menuButton7.pack(side=LEFT)
        self.menuButton7_ttp = CreateToolTip(self.menuButton7, \
            'Block delete, delete select block and line. ')

        image = Image.open("icons/datei_page_delite_button.png")
        self.imgDeliteObjectButton2 = ImageTk.PhotoImage(image)
        self.menuButton8 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.del_page, width=10) 
        self.menuButton8.config(image=self.imgDeliteObjectButton2 , width="30", height="30")       
        #self.menuButton7.grid(row=0, column=0, padx=280, sticky="nw")
        self.menuButton8.pack(side=LEFT)
        self.menuButton8_ttp = CreateToolTip(self.menuButton8, \
            'Delete current page, delete all blocks and line on the current page. ')

        image = Image.open("icons/datei_file_delite_button.png")
        self.imgFileDeliteButton = ImageTk.PhotoImage(image)
        self.menuButton6 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.del_all, width=10) 
        self.menuButton6.config(image=self.imgFileDeliteButton , width="30", height="30")       
        #self.menuButton6.grid(row=0, column=0, padx=245, sticky="nw")
        self.menuButton6.pack(side=LEFT)
        self.menuButton6_ttp = CreateToolTip(self.menuButton6, \
            'Project delete, delete all pages blocks lines --> new project. ')

        image = Image.open("icons/v_line.png")
        self.imgV_line1 = ImageTk.PhotoImage(image)
        self.menuButton9 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.v_line, width=10) 
        self.menuButton9.config(image=self.imgV_line1 , width="3", height="30")       
        self.menuButton9.pack(side=LEFT)

        image = Image.open("icons/page_export_button.png")
        self.imgPageExport = ImageTk.PhotoImage(image)
        self.menuButtonPageExport = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.page_export, width=10) 
        self.menuButtonPageExport.config(image=self.imgPageExport , width="30", height="30")       
        self.menuButtonPageExport.pack(side=LEFT)
        self.menuButtonPageExport_ttp = CreateToolTip(self.menuButtonPageExport, \
            'Page export, export selectet page. ')

        image = Image.open("icons/page_import_button.png")
        self.imgPageInport = ImageTk.PhotoImage(image)
        self.menuButtonPageInport = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.page_import, width=10) 
        self.menuButtonPageInport.config(image=self.imgPageInport , width="30", height="30")       
        self.menuButtonPageInport.pack(side=LEFT)
        self.menuButtonPageInport_ttp = CreateToolTip(self.menuButtonPageInport, \
            'Page import, import selectet page. ')

        image = Image.open("icons/v_line.png")
        self.imgV_line2 = ImageTk.PhotoImage(image)
        self.menuButton10 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.v_line, width=10) 
        self.menuButton10.config(image=self.imgV_line2 , width="3", height="30")       
        self.menuButton10.pack(side=LEFT)

        image = Image.open("icons/compelier_button.png")
        self.imgCompButton = ImageTk.PhotoImage(image)
        self.menuButton3 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.compelieren2, width=10) 
        self.menuButton3.config(image=self.imgCompButton , width="30", height="30")    
        #self.menuButton3.grid(row=0, column=0, padx=70, sticky="nw")
        self.menuButton3.pack(side=LEFT)
        self.menuButton3_ttp = CreateToolTip(self.menuButton3, \
            'Compile project, compile project for simulate and transfer. ')

        image = Image.open("icons/play_button.png")
        self.imgPlayButton = ImageTk.PhotoImage(image)  
        self.menuButton1 = tk.Button(self.menu_frame, text="Test1", image=self.imgPlayButton, 
                                command=self.parent.pre_periodicCall, width=10)
        self.menuButton1.config(image=self.imgPlayButton , width="30", height="30")
        #self.menuButton1.grid(row=0, column=0, sticky="nw")
        self.menuButton1.pack(side=LEFT)
        self.menuButton1_ttp = CreateToolTip(self.menuButton1, \
            'Run simulator, compile project befor you simulate. ')

        image = Image.open("icons/stop_button.png")
        #image = image.resize((50, 20), Image.ANTIALIAS)
        self.imgStopButton = ImageTk.PhotoImage(image)
        self.menuButton2 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.periodicCallOff, width=10) 
        self.menuButton2.config(image=self.imgStopButton , width="30", height="30")       
        #self.menuButton2.grid(row=0, column=0, padx=35, sticky="nw")
        self.menuButton2.pack(side=LEFT)
        self.menuButton2_ttp = CreateToolTip(self.menuButton2, \
            'Stop simulator, project ready for editing. ')

        image = Image.open("icons/v_line.png")
        self.imgV_line4 = ImageTk.PhotoImage(image)
        self.menuButton10 = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.v_line, width=10) 
        self.menuButton10.config(image=self.imgV_line4 , width="3", height="30")       
        self.menuButton10.pack(side=LEFT)

        image = Image.open("icons/upload_button.png")
        self.imgUpload = ImageTk.PhotoImage(image)
        self.menuButtonUpload = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.upload_plc, width=10) 
        self.menuButtonUpload.config(image=self.imgUpload , width="30", height="30")       
        self.menuButtonUpload.pack(side=LEFT)
        self.menuButtonUpload_ttp = CreateToolTip(self.menuButtonUpload, \
            'Upload programm, upload programm.json to plc. ')
        
        image = Image.open("icons/information_button.png")
        self.imgInformation = ImageTk.PhotoImage(image)
        self.menuButtonInformation = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.onClickInformation, width=10) 
        self.menuButtonInformation.config(image=self.imgInformation , width="30", height="30")       
        self.menuButtonInformation.pack(side=RIGHT)
        self.menuButtonInformation_ttp = CreateToolTip(self.menuButtonInformation, \
            'Information. ')
        
        image = Image.open("icons/setting_button.png")
        self.imgSetting = ImageTk.PhotoImage(image)
        self.menuButtonSetting = tk.Button(self.menu_frame, text="Test2",
                                command=self.parent.onClickSetting, width=10) 
        self.menuButtonSetting.config(image=self.imgSetting , width="30", height="30")       
        self.menuButtonSetting.pack(side=RIGHT)
        self.menuButtonSetting_ttp = CreateToolTip(self.menuButtonSetting, \
            'Project setting. ')

        # Registerkarten -----------------------------------------------------------------------------------------
        # Page - Logic +++++
        self.tk.Label(self.tab1, text="Elementary ", font=('Arial', 12), fg="black").grid(row=0, column=0)
        #Button and 2
        image = Image.open("icons/and2_button.png")
        self.imgAnd2Button = ImageTk.PhotoImage(image)  
        self.and2Button = tk.Button(self.tab1, text="Test1", image=self.imgAnd2Button, 
                                command=self.parent.erzeuge_and_2, width=10)
        self.and2Button.config(image=self.imgAnd2Button , width="30", height="30")
        self.and2Button.grid(row=1, column=0)
        #Button and 3
        image = Image.open("icons/and3_button.png")
        self.imgAnd3Button = ImageTk.PhotoImage(image)  
        self.and3Button = tk.Button(self.tab1, text="Test1", image=self.imgAnd3Button, 
                                command=self.parent.erzeuge_and_3, width=10)
        self.and3Button.config(image=self.imgAnd3Button , width="30", height="30")
        self.and3Button.grid(row=2, column=0)
        #Button or 2
        image = Image.open("icons/or2_button.png")
        self.imgOr2Button = ImageTk.PhotoImage(image)  
        self.or2Button = tk.Button(self.tab1, text="Test1", image=self.imgOr2Button, 
                                command=self.parent.erzeuge_or_2, width=10)
        self.or2Button.config(image=self.imgOr2Button , width="30", height="30")
        self.or2Button.grid(row=1, column=1)
        #Button or 3
        image = Image.open("icons/or3_button.png")
        self.imgOr3Button = ImageTk.PhotoImage(image)  
        self.or3Button = tk.Button(self.tab1, text="Test1", image=self.imgOr3Button, 
                                command=self.parent.erzeuge_or_3, width=10)
        self.or3Button.config(image=self.imgOr3Button , width="30", height="30")
        self.or3Button.grid(row=2, column=1)
        #Button Input
        image = Image.open("icons/input_button.png")
        self.imgInputButton = ImageTk.PhotoImage(image)  
        self.InputButton = tk.Button(self.tab1, text="Test1", image=self.imgInputButton, 
                                command=self.parent.input, width=10)
        self.InputButton.config(image=self.imgInputButton , width="30", height="30")
        self.InputButton.grid(row=3, column=0)
        self.InputButton_ttp = CreateToolTip(self.InputButton, \
            'Input                                  .\
             input = I or B')
        #Button Output
        image = Image.open("icons/output_button.png")
        self.imgOutputButton = ImageTk.PhotoImage(image)  
        self.OutputButton = tk.Button(self.tab1, text="Test1", image=self.imgOutputButton, 
                                command=self.parent.zuweisung, width=10)
        self.OutputButton.config(image=self.imgOutputButton , width="30", height="30")
        self.OutputButton.grid(row=3, column=1)

        # Timer
        self.tk.Label(self.tab1, text="Timer", font=('Arial', 12), fg="black").grid(row=4, column=0)
        #Button TON
        image = Image.open("icons/ton_button.png")
        self.imgTonButton = ImageTk.PhotoImage(image)  
        self.tonButton = tk.Button(self.tab1, text="Test1", image=self.imgTonButton, 
                                command=self.parent.erzeuge_ton, width=10)
        self.tonButton.config(image=self.imgTonButton , width="30", height="30")
        self.tonButton.grid(row=5, column=0)
        self.tonButton_ttp = CreateToolTip(self.tonButton, \
            'Time On delay                    \
             in = 1 --> start on delay time   \
             out = 1 --> on delay time ends')
        #Button TOF
        image = Image.open("icons/toff_button.png")
        self.imgToffButton = ImageTk.PhotoImage(image)  
        self.toffButton = tk.Button(self.tab1, text="Test1", image=self.imgToffButton, 
                                command=self.parent.erzeuge_tof, width=10)
        self.toffButton.config(image=self.imgToffButton , width="30", height="30")
        self.toffButton.grid(row=6, column=0)
        self.toffButton_ttp = CreateToolTip(self.toffButton, \
            'Time off delay                    \
             in = 0 --> start off delay time   \
             out = 1 --> until off delay time ends')

        # Bool
        self.tk.Label(self.tab1, text="Bool", font=('Arial', 12), fg="black").grid(row=7, column=0)
        #Button Sr
        image = Image.open("icons/sr_button.png")
        self.imgSrButton = ImageTk.PhotoImage(image)  
        self.srButton = tk.Button(self.tab1, text="Test1", image=self.imgSrButton, 
                                command=self.parent.erzeuge_sr, width=10)
        self.srButton.config(image=self.imgSrButton , width="30", height="30")
        self.srButton.grid(row=8, column=0)
        self.srButton_ttp = CreateToolTip(self.srButton, \
            'Bistable relay                     \
             in S = 1 --> out = 1               \
             in R = 1 --> out = 0')
        #Button Inv
        image = Image.open("icons/inv_button.png")
        self.imgInvButton = ImageTk.PhotoImage(image)  
        self.invButton = tk.Button(self.tab1, text="Test1", image=self.imgInvButton, 
                                command=self.parent.erzeuge_inv, width=10)
        self.invButton.config(image=self.imgInvButton , width="30", height="30")
        self.invButton.grid(row=8, column=1)
        self.invButton_ttp = CreateToolTip(self.invButton, \
            'Invert                                    \
             in = 1 --> out = 0                        \
             in = 0 --> out = 1')
        #Button ip
        image = Image.open("icons/ip_button.png")
        self.imgIpButton = ImageTk.PhotoImage(image)  
        self.ipButton = tk.Button(self.tab1, text="Test1", image=self.imgIpButton, 
                                command=self.parent.erzeuge_ip, width=10)
        self.ipButton.config(image=self.imgIpButton , width="30", height="30")
        self.ipButton.grid(row=9, column=1)
        self.ipButton_ttp = CreateToolTip(self.ipButton, \
            'Impulse positive                     \
             in = 1 --> out = one plc cykle 1         \
             in = 0 --> out = 0')

        # counter
        self.tk.Label(self.tab1, text="Counter", font=('Arial', 12), fg="black").grid(row=10, column=0)
        #Button cud
        image = Image.open("icons/count_button.png")
        self.imgCountButton = ImageTk.PhotoImage(image)  
        self.countButton = tk.Button(self.tab1, text="Test1", image=self.imgCountButton, 
                                command=self.parent.erzeuge_cud, width=10)
        self.countButton.config(image=self.imgCountButton , width="30", height="30")
        self.countButton.grid(row=11, column=0)
        self.countButton_ttp = CreateToolTip(self.countButton, \
            'Count up down                     \
             in UP = count up                  \
             in DOWN = count down               \
             in SET = set counter to Preset Val\
             Preset Value = is setting if SET = 1 \
             Set Value = (if aktual count = set Value --> out = 1)')

        # Compare Int
        self.tk.Label(self.tab1, text="Compare Int    ", font=('Arial', 12), fg="black").grid(row=12, column=0)
        # <I
        image = Image.open("icons/lt_button.png")
        self.imgLtButton = ImageTk.PhotoImage(image)  
        self.ltButton = tk.Button(self.tab1, text="Test1", image=self.imgLtButton, 
                                command=self.parent.erzeuge_lt, width=10)
        self.ltButton.config(image=self.imgLtButton , width="30", height="30")
        self.ltButton.grid(row=13, column=0)
        # <=I
        image = Image.open("icons/lit_button.png")
        self.imgLitButton = ImageTk.PhotoImage(image)  
        self.litButton = tk.Button(self.tab1, text="Test1", image=self.imgLitButton, 
                                command=self.parent.erzeuge_lit, width=10)
        self.litButton.config(image=self.imgLitButton , width="30", height="30")
        self.litButton.grid(row=13, column=0, sticky="e")
        # >I
        image = Image.open("icons/gt_button.png")
        self.imgGtButton = ImageTk.PhotoImage(image)  
        self.gtButton = tk.Button(self.tab1, text="Test1", image=self.imgGtButton, 
                                command=self.parent.erzeuge_gt, width=10)
        self.gtButton.config(image=self.imgGtButton , width="30", height="30")
        self.gtButton.grid(row=14, column=0)
        # >=I
        image = Image.open("icons/git_button.png")
        self.imgGitButton = ImageTk.PhotoImage(image)  
        self.gitButton = tk.Button(self.tab1, text="Test1", image=self.imgGitButton, 
                                command=self.parent.erzeuge_git, width=10)
        self.gitButton.config(image=self.imgGitButton , width="30", height="30")
        self.gitButton.grid(row=14, column=0, sticky="e")
        # =I
        image = Image.open("icons/it_button.png")
        self.imgItButton = ImageTk.PhotoImage(image)  
        self.ItButton = tk.Button(self.tab1, text="Test1", image=self.imgItButton, 
                                command=self.parent.erzeuge_it, width=10)
        self.ItButton.config(image=self.imgItButton , width="30", height="30")
        self.ItButton.grid(row=13, column=1)
        # !=I
        image = Image.open("icons/nit_button.png")
        self.imgNitButton = ImageTk.PhotoImage(image)  
        self.NitButton = tk.Button(self.tab1, text="Test1", image=self.imgNitButton, 
                                command=self.parent.erzeuge_nit, width=10)
        self.NitButton.config(image=self.imgNitButton , width="30", height="30")
        self.NitButton.grid(row=14, column=1)

        # Aritmetic Int
        self.tk.Label(self.tab1, text="Aritmetic Int    ", font=('Arial', 12), fg="black").grid(row=15, column=0)
        # addieren
        image = Image.open("icons/add_button.png")
        self.imgAddButton = ImageTk.PhotoImage(image)  
        self.addButton = tk.Button(self.tab1, text="Test1", image=self.imgAddButton, 
                                command=self.parent.erzeuge_add, width=10)
        self.addButton.config(image=self.imgAddButton , width="30", height="30")
        self.addButton.grid(row=16, column=0)
        # subtrahieren
        image = Image.open("icons/sub_button.png")
        self.imgSubButton = ImageTk.PhotoImage(image)  
        self.subButton = tk.Button(self.tab1, text="Test1", image=self.imgSubButton, 
                                command=self.parent.erzeuge_sub, width=10)
        self.subButton.config(image=self.imgSubButton , width="30", height="30")
        self.subButton.grid(row=16, column=1)
        # multiblizieren
        image = Image.open("icons/mul_button.png")
        self.imgMulButton = ImageTk.PhotoImage(image)  
        self.mulButton = tk.Button(self.tab1, text="Test1", image=self.imgMulButton, 
                                command=self.parent.erzeuge_mul, width=10)
        self.mulButton.config(image=self.imgMulButton , width="30", height="30")
        self.mulButton.grid(row=17, column=0)
        # dividieren
        image = Image.open("icons/div_button.png")
        self.imgDivButton = ImageTk.PhotoImage(image)  
        self.divButton = tk.Button(self.tab1, text="Test1", image=self.imgDivButton, 
                                command=self.parent.erzeuge_div, width=10)
        self.divButton.config(image=self.imgDivButton , width="30", height="30")
        self.divButton.grid(row=17, column=1)

        # Other
        self.tk.Label(self.tab1, text="Other", font=('Arial', 12), fg="black").grid(row=18, column=0)
        # Move Int
        image = Image.open("icons/mov_button.png")
        self.imgMoveButton = ImageTk.PhotoImage(image)  
        self.moveButton = tk.Button(self.tab1, text="Test1", image=self.imgMoveButton, 
                                command=self.parent.erzeuge_move, width=10)
        self.moveButton.config(image=self.imgMoveButton , width="30", height="30")
        self.moveButton.grid(row=19, column=0)
        # Kommentar
        image = Image.open("icons/com_button.png")
        self.imgCommentButton = ImageTk.PhotoImage(image)  
        self.commentButton = tk.Button(self.tab1, text="Test1", image=self.imgCommentButton, 
                                command=self.parent.erzeuge_comm, width=10)
        self.commentButton.config(image=self.imgCommentButton , width="30", height="30")
        self.commentButton.grid(row=19, column=1)

        # Page - I/O +++++
        #Check Button
        self.tk.Label(self.tab2, text="INPUT/OUTPUT ", font=('Arial', 12), fg="black").grid(row=0, column=0)
        self.checkI_1 = tk.IntVar()
        self.checkI_2 = tk.IntVar()
        self.checkI_3 = tk.IntVar()
        self.checkI_4 = tk.IntVar()
        self.checkI_5 = tk.IntVar()
        self.checkI_6 = tk.IntVar()
        self.checkI_7 = tk.IntVar()
        self.checkI_8 = tk.IntVar()
        self.checkO_1 = tk.IntVar()
        self.checkO_2 = tk.IntVar()
        self.checkO_3 = tk.IntVar()
        self.checkO_4 = tk.IntVar()
        self.checkO_5 = tk.IntVar()
        self.checkO_6 = tk.IntVar()
        self.checkO_7 = tk.IntVar()
        self.checkO_8 = tk.IntVar()
        self.check_I_1 = tk.Checkbutton(self.tab2, text="I 1", variable= self.checkI_1,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_I_2 = tk.Checkbutton(self.tab2, text="I 2", variable= self.checkI_2,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_I_3 = tk.Checkbutton(self.tab2, text="I 3", variable= self.checkI_3,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_I_4 = tk.Checkbutton(self.tab2, text="I 4", variable= self.checkI_4,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_I_5 = tk.Checkbutton(self.tab2, text="I 5", variable= self.checkI_5,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_I_6 = tk.Checkbutton(self.tab2, text="I 6", variable= self.checkI_6,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_I_7 = tk.Checkbutton(self.tab2, text="I 7", variable= self.checkI_7,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_I_8 = tk.Checkbutton(self.tab2, text="I 8", variable= self.checkI_8,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_O_1 = tk.Checkbutton(self.tab2, text="Q 1", variable= self.checkO_1,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_O_2 = tk.Checkbutton(self.tab2, text="Q 2", variable= self.checkO_2,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_O_3 = tk.Checkbutton(self.tab2, text="Q 3", variable= self.checkO_3,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_O_4 = tk.Checkbutton(self.tab2, text="Q 4", variable= self.checkO_4,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_O_5 = tk.Checkbutton(self.tab2, text="Q 5", variable= self.checkO_5,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_O_6 = tk.Checkbutton(self.tab2, text="Q 6", variable= self.checkO_6,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_O_7 = tk.Checkbutton(self.tab2, text="Q 7", variable= self.checkO_7,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_O_8 = tk.Checkbutton(self.tab2, text="Q 8", variable= self.checkO_8,
                                        onvalue=1, offvalue=0, height=1, 
                                        width=1)
        self.check_I_1.grid(row=1, column=0)
        self.check_I_2.grid(row=2, column=0)
        self.check_I_3.grid(row=3, column=0)
        self.check_I_4.grid(row=4, column=0)
        self.check_I_5.grid(row=5, column=0)
        self.check_I_6.grid(row=6, column=0)
        self.check_I_7.grid(row=7, column=0)
        self.check_I_8.grid(row=8, column=0)
        self.check_O_1.grid(row=1, column=1)
        self.check_O_2.grid(row=2, column=1)
        self.check_O_3.grid(row=3, column=1)
        self.check_O_4.grid(row=4, column=1)
        self.check_O_5.grid(row=5, column=1)
        self.check_O_6.grid(row=6, column=1)
        self.check_O_7.grid(row=7, column=1)
        self.check_O_8.grid(row=8, column=1)

        '''self.tk.Label(self.tab2, text="Other ", font=('Arial', 12), fg="black").grid(row=9, column=0)
        self.check_auto_hand = tk.IntVar()
        self.check_modbus = tk.IntVar()
        self.c_auto_hand = tk.Checkbutton(self.tab2, text="Auto", variable=self.check_auto_hand, \
                         onvalue=1, offvalue=0, height=1, \
                         width=1)
        self.c_modbus = tk.Checkbutton(self.tab2, text="Modbus", variable=self.check_modbus, \
                         onvalue=1, offvalue=0, height=1, \
                         width=1)
        self.c_auto_hand.grid(row=10, column=0)
        self.c_modbus.grid(row=11, column=0)'''

        # Page - File +++++
        self.selectFileNamePath = self.tk.Label(self.tab3, text="No file select! ", font=('Arial', 12), fg="black")#.grid(row=16, column=0)
        self.selectFileNamePath.grid(row=0, column=0)
        self.selectFileName = self.tk.Label(self.tab3, text="No file select! ", font=('Arial', 12), fg="black")
        self.selectFileName.grid(row=1, column=0, sticky='W')

        '''self.loeschen_block = tk.Button(self.tab3, text="del",
                         command=self.parent.loeschen_block, width=15) #command=self.parent.login)
        self.erzeuge_and_2 = tk.Button(self.tab3, text="and",
                          command=self.parent.erzeuge_and_2, width=15) #command=self.parent.do)
        self.auf = tk.Button(self.tab3, text="auf",
                               command=self.parent.achseAuf, width=15)  # command=self.parent.login)
        self.ab = tk.Button(self.tab3, text="ab",
                                command=self.parent.laden_programm, width=15)  # command=self.parent.do)
        self.start = tk.Button(self.tab3, text="=",
                           command=self.parent.zuweisung, width=15) #command=self.parent.do)

        self.loeschen_block.grid(row=17, column=0)
        self.erzeuge_and_2.grid(row=17, column=1)
        self.auf.grid(row=18, column=0)
        self.ab.grid(row=18, column=1)
        self.start.grid(row=19, column=0)'''

class DialogTon:
    def __init__(self, parent, parameter1):
        top = self.top = tk.Toplevel(parent)
        self.paramter1 = str(parameter1)
        self.myLabel = tk.Label(top, text='Set Time in ms')
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()
        self.mySubmitButton = tk.Button(top, text='ok', command=self.send)
        self.mySubmitButton.pack()
        # aktuelle wert in entrybox vorbelegen
        self.set_text(self.paramter1)
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        top.update_idletasks()
        xp = (top.winfo_screenwidth() // 2) - (top.winfo_width() // 2)
        yp = (top.winfo_screenheight() // 2) - (top.winfo_height() // 2)
        geom = (top.winfo_width(), top.winfo_height(), xp, yp)
        top.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # wait for window to appear on screen before calling grab_set
        #self.top.wait_visibility()
        #self.top.grab_set()
        #self.top.wait_window(parent)

    def set_text(self, text):
        self.myEntryBox.delete(0,END)
        self.myEntryBox.insert(0,text)

    def send(self):
        self.paramter1 = self.myEntryBox.get()
        self.top.destroy()

class DialogTof:
    def __init__(self, parent, parameter1):
        top = self.top = tk.Toplevel(parent)
        self.paramter1 = str(parameter1)
        self.myLabel = tk.Label(top, text='Set Time in ms')
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()
        self.mySubmitButton = tk.Button(top, text='ok', command=self.send)
        self.mySubmitButton.pack()
        # aktuelle wert in entrybox vorbelegen
        self.set_text(self.paramter1)
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        top.update_idletasks()
        xp = (top.winfo_screenwidth() // 2) - (top.winfo_width() // 2)
        yp = (top.winfo_screenheight() // 2) - (top.winfo_height() // 2)
        geom = (top.winfo_width(), top.winfo_height(), xp, yp)
        top.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # wait for window to appear on screen before calling grab_set
        #self.top.wait_visibility()
        #self.top.grab_set()
        #self.top.wait_window(parent)

    def set_text(self, text):
        self.myEntryBox.delete(0,END)
        self.myEntryBox.insert(0,text)

    def send(self):
        self.paramter1 = self.myEntryBox.get()
        self.top.destroy()

class DialogCounter:
    def __init__(self, parent, parameter1, parameter2):
        top = self.top = tk.Toplevel(parent)
        self.paramter1 = str(parameter1)
        self.paramter2 = str(parameter2)
        self.myLabel = tk.Label(top, text='Preset Value Counter')
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()
        self.myLabel2 = tk.Label(top, text='Set Value Counter')
        self.myLabel2.pack()
        self.myEntryBox2 = tk.Entry(top)
        self.myEntryBox2.pack()
        self.mySubmitButton = tk.Button(top, text='ok', command=self.send)
        self.mySubmitButton.pack()
        # aktuelle wert in entrybox vorbelegen
        self.set_text(self.paramter1, self.paramter2)
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        top.update_idletasks()
        xp = (top.winfo_screenwidth() // 2) - (top.winfo_width() // 2)
        yp = (top.winfo_screenheight() // 2) - (top.winfo_height() // 2)
        geom = (top.winfo_width(), top.winfo_height(), xp, yp)
        top.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # wait for window to appear on screen before calling grab_set
        #self.top.wait_visibility()
        #self.top.grab_set()
        #self.top.wait_window(parent)

    def set_text(self, text, text2):
        self.myEntryBox.delete(0,END)
        self.myEntryBox.insert(0,text)
        self.myEntryBox2.delete(0,END)
        self.myEntryBox2.insert(0,text2)

    def send(self):
        self.paramter1 = self.myEntryBox.get()
        self.paramter2 = self.myEntryBox2.get()
        self.top.destroy()

class DialogLt:
    def __init__(self, parent, parameter1, parameter2):
        top = self.top = tk.Toplevel(parent)
        self.paramter1 = str(parameter1)
        self.paramter2 = str(parameter2)
        self.myLabel = tk.Label(top, text='Input 1, MW, CUD, TON, TOF')
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()
        self.myLabel2 = tk.Label(top, text='Input 2, MW, CUD, TON, TOF')
        self.myLabel2.pack()
        self.myEntryBox2 = tk.Entry(top)
        self.myEntryBox2.pack()
        self.mySubmitButton = tk.Button(top, text='ok', command=self.send)
        self.mySubmitButton.pack()
        # aktuelle wert in entrybox vorbelegen
        self.set_text(self.paramter1, self.paramter2)
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        top.update_idletasks()
        xp = (top.winfo_screenwidth() // 2) - (top.winfo_width() // 2)
        yp = (top.winfo_screenheight() // 2) - (top.winfo_height() // 2)
        geom = (top.winfo_width(), top.winfo_height(), xp, yp)
        top.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # wait for window to appear on screen before calling grab_set
        #self.top.wait_visibility()
        #self.top.grab_set()
        #self.top.wait_window(parent)

    def set_text(self, text, text2):
        self.myEntryBox.delete(0,END)
        self.myEntryBox.insert(0,text)
        self.myEntryBox2.delete(0,END)
        self.myEntryBox2.insert(0,text2)

    def send(self):
        self.paramter1 = self.myEntryBox.get()
        self.paramter2 = self.myEntryBox2.get()
        self.top.destroy()

class DialogAritmetic:
    def __init__(self, parent, parameter1, parameter2, parameter3):
        top = self.top = tk.Toplevel(parent)
        self.paramter1 = str(parameter1)
        self.paramter2 = str(parameter2)
        self.paramter3 = str(parameter3)
        self.myLabel = tk.Label(top, text='Input 1, MW, CUD, TON, TOF')
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()
        self.myLabel2 = tk.Label(top, text='Input 2, MW, CUD, TON, TOF')
        self.myLabel2.pack()
        self.myEntryBox2 = tk.Entry(top)
        self.myEntryBox2.pack()
        self.myLabel3 = tk.Label(top, text='Output, MW')
        self.myLabel3.pack()
        self.myEntryBox3 = tk.Entry(top)
        self.myEntryBox3.pack()
        self.mySubmitButton = tk.Button(top, text='ok', command=self.send)
        self.mySubmitButton.pack()
        # aktuelle wert in entrybox vorbelegen
        self.set_text(self.paramter1, self.paramter2, self.paramter3)
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        top.update_idletasks()
        xp = (top.winfo_screenwidth() // 2) - (top.winfo_width() // 2)
        yp = (top.winfo_screenheight() // 2) - (top.winfo_height() // 2)
        geom = (top.winfo_width(), top.winfo_height(), xp, yp)
        top.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # wait for window to appear on screen before calling grab_set
        #self.top.wait_visibility()
        #self.top.grab_set()
        #self.top.wait_window(parent)

    def set_text(self, text, text2, text3):
        self.myEntryBox.delete(0,END)
        self.myEntryBox.insert(0,text)
        self.myEntryBox2.delete(0,END)
        self.myEntryBox2.insert(0,text2)
        self.myEntryBox3.delete(0,END)
        self.myEntryBox3.insert(0,text3)

    def send(self):
        self.paramter1 = self.myEntryBox.get()
        self.paramter2 = self.myEntryBox2.get()
        self.paramter3 = self.myEntryBox3.get()
        self.top.destroy()

class DialogMove:
    def __init__(self, parent, parameter1, parameter2):
        top = self.top = tk.Toplevel(parent)
        self.paramter1 = str(parameter1)
        self.paramter2 = str(parameter2)
        self.myLabel = tk.Label(top, text='Input 1, MW, CUD, TON, TOF')
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()
        self.myLabel2 = tk.Label(top, text='Output 2, MW, CUD, TON, TOF')
        self.myLabel2.pack()
        self.myEntryBox2 = tk.Entry(top)
        self.myEntryBox2.pack()
        self.mySubmitButton = tk.Button(top, text='ok', command=self.send)
        self.mySubmitButton.pack()
        # aktuelle wert in entrybox vorbelegen
        self.set_text(self.paramter1, self.paramter2)
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        top.update_idletasks()
        xp = (top.winfo_screenwidth() // 2) - (top.winfo_width() // 2)
        yp = (top.winfo_screenheight() // 2) - (top.winfo_height() // 2)
        geom = (top.winfo_width(), top.winfo_height(), xp, yp)
        top.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # wait for window to appear on screen before calling grab_set
        #self.top.wait_visibility()
        #self.top.grab_set()
        #self.top.wait_window(parent)

    def set_text(self, text, text2):
        self.myEntryBox.delete(0,END)
        self.myEntryBox.insert(0,text)
        self.myEntryBox2.delete(0,END)
        self.myEntryBox2.insert(0,text2)

    def send(self):
        self.paramter1 = self.myEntryBox.get()
        self.paramter2 = self.myEntryBox2.get()
        self.top.destroy()

class DialogComment:
    def __init__(self, parent, parameter1):
        top = self.top = tk.Toplevel(parent)
        self.paramter1 = str(parameter1)
        self.myLabel = tk.Label(top, text='Comment')
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()
        self.mySubmitButton = tk.Button(top, text='ok', command=self.send)
        self.mySubmitButton.pack()
        # aktuelle wert in entrybox vorbelegen
        self.set_text(self.paramter1)
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        top.update_idletasks()
        xp = (top.winfo_screenwidth() // 2) - (top.winfo_width() // 2)
        yp = (top.winfo_screenheight() // 2) - (top.winfo_height() // 2)
        geom = (top.winfo_width(), top.winfo_height(), xp, yp)
        top.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # wait for window to appear on screen before calling grab_set
        #self.top.wait_visibility()
        #self.top.grab_set()
        #self.top.wait_window(parent)

    def set_text(self, text):
        self.myEntryBox.delete(0,END)
        self.myEntryBox.insert(0,text)

    def send(self):
        self.paramter1 = self.myEntryBox.get()
        self.top.destroy()

class DialogOutput:
    def __init__(self, parent, outNrFockus):
        top = self.top = tk.Toplevel(parent)
        self.paramter1 = outNrFockus
        self.outNrFockus = outNrFockus  
        self.myLabel = tk.Label(top, text='Output number Q1-Q8')
        self.myLabel.pack()
        self.myEntryBox = tk.Entry(top)
        self.myEntryBox.pack()
        self.mySubmitButton = tk.Button(top, text='ok', command=self.send)
        self.mySubmitButton.pack()
        # aktuelle wert in entrybox vorbelegen
        self.set_text_out_nr(self.outNrFockus)

        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        top.update_idletasks()
        xp = (top.winfo_screenwidth() // 2) - (top.winfo_width() // 2)
        yp = (top.winfo_screenheight() // 2) - (top.winfo_height() // 2)
        geom = (top.winfo_width(), top.winfo_height(), xp, yp)
        top.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # wait for window to appear on screen before calling grab_set
        #self.top.wait_visibility()
        #self.top.grab_set()
        #self.top.wait_window(parent)

    def set_text_out_nr(self, text):
        self.myEntryBox.delete(0,END)
        self.myEntryBox.insert(0,text)

    def send(self):
        self.paramter1 = self.myEntryBox.get()
        self.top.destroy()

class DialogBlockInput(tkinter.simpledialog.Dialog):
    def __init__(self, parent, title, blockNrFockus, inputNrFockus):
        self.blockNr = None
        self.inputNr = None
        self.blockNrFockus = blockNrFockus
        self.inputNrFockus = inputNrFockus       
        super().__init__(parent, title)      
                
    def body(self, frame):
        #print(type(frame)) # tkinter.Frame
        self.blockNr_label = tk.Label(frame, width=25, text="Block Number")
        self.blockNr_label.pack()
        self.blockNr_box = tk.Entry(frame, width=25)
        self.blockNr_box.pack()
        self.set_text_block_nr(self.blockNrFockus)

        self.inputNr_label = tk.Label(frame, width=25, text="Input Number")
        self.inputNr_label.pack()
        self.inputNr_box = tk.Entry(frame, width=25)
        self.inputNr_box.pack()
        self.set_text_input_nr(self.inputNrFockus)
        #self.inputNr_box['show'] = '*'

        return frame

    def set_text_block_nr(self, text):
        self.blockNr_box.delete(0,END)
        self.blockNr_box.insert(0,text)

    def set_text_input_nr(self, text):
        self.inputNr_box.delete(0,END)
        self.inputNr_box.insert(0,text)
        
    def ok_pressed(self):
        # print("ok")
        self.blockNr = self.blockNr_box.get()
        self.inputNr = self.inputNr_box.get()
        self.destroy()

    def cancel_pressed(self):
        # print("cancel")
        self.destroy()

    def buttonbox(self):
        self.ok_button = tk.Button(self, text='OK', width=5, command=self.ok_pressed)
        self.ok_button.pack(side="left")
        cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())

class DialogSetting:
    def __init__(self, parent):
        top = self.top = tk.Toplevel(parent)
        #self.paramter1 = ''
        self.myLabel = tk.Label(top, text='File path for external programm to uploading plc ')
        self.myLabel.grid(row=0, column=0)
        self.myEntryBox = tk.Entry(top, width=100)
        self.myEntryBox.grid(row=1, column=0)
        global uploadPathExe
        self.myEntryBox.insert(0, str(uploadPathExe))
        self.pathButton = tk.Button(top, text='Path exe', command=self.path, width=8, height=1)
        self.pathButton.grid(row=1, column=1)
        self.mySubmitButton = tk.Button(top, text='ok', command=self.send)
        self.mySubmitButton.grid(row=3, column=0)
        # for accuracy see: https://stackoverflow.com/a/10018670/1217270
        top.update_idletasks()
        xp = (top.winfo_screenwidth() // 2) - (top.winfo_width() // 2)
        yp = (top.winfo_screenheight() // 2) - (top.winfo_height() // 2)
        geom = (top.winfo_width(), top.winfo_height(), xp, yp)
        top.geometry('{0}x{1}+{2}+{3}'.format(*geom))

        # wait for window to appear on screen before calling grab_set
        #self.top.wait_visibility()
        #self.top.grab_set()
        #self.top.wait_window(parent)

    def send(self):
        self.paramter1 = self.myEntryBox.get()
        self.top.destroy()
    
    def path(self):
        ftypes = [('Programm exe', '*.exe'), ('All files', '*')]
        dlg = tkinter.filedialog.askopenfilename(filetypes = ftypes)
        
        global uploadPathExe
        configDaten = {'uploadPathExe': ''}
        uploadPathExe = dlg
        configDaten['uploadPathExe'] = str(uploadPathExe)
        try:
            with open('config.txt', 'w') as fp:
                json.dump(configDaten, fp)
        except:
            print('Conig File not Write')

class MouseMover():
    def __init__(self):
        self.item = 0
        self.previous = (0, 0)
        self.lines = []
        self.lastX = None
        self.lastY = None
        self.redLine = None
        self.linieZeichnen = False
        self.liniePos = [0, 0, 0, 0, '', '', '']
        self.geklicktFokus = 0
        self.geklicktFokusBlockLetzter = ''

    def select(self, event):
        widget = event.widget                       # Get handle to canvas 
        # Convert screen coordinates to canvas coordinates
        xc = widget.canvasx(event.x); yc = widget.canvasx(event.y)
        self.item = widget.find_closest(xc, yc)[0]        # ID for closest
        global blockFokusInput, blocks, blockPositionFokus, comments
        blockFokusInput = self.item
        self.previous = (xc, yc)
        #print((xc, yc, self.item))
        # Aktuelle postion vom Block eingang der Makeirt ist
        #self.main_window_frame.zeichenwand.coords(1, 0, 0, 100, 100)
        for block in blocks:
            if 'objectNrInput1' in block:
                if block['objectNrInput1'] == blockFokusInput:
                    if 'inX1' in block:
                        blockPositionFokus[0] = block['inX1']
                        blockPositionFokus[1] = block['inY1']
                        blockPositionFokus[2] = block['blockNr'] 
                        blockPositionFokus[3] = 'in1'
                        if self.liniePos[0]:
                            self.liniePos[2] = blockPositionFokus[0]
                            self.liniePos[3] = blockPositionFokus[1]
                            self.liniePos[5] = block['blockNr'] 
                            self.liniePos[6] = 'in1'
                            self.zeichne_line()
                            self.liniePos = [0, 0, 0, 0, '', '', ''] 

            if 'objectNrInput2' in block:
                if block['objectNrInput2'] == blockFokusInput:
                    if 'inX2' in block:
                        blockPositionFokus[0] = block['inX2']
                        blockPositionFokus[1] = block['inY2']
                        blockPositionFokus[2] = block['blockNr'] 
                        blockPositionFokus[3] = 'in2'
                        if self.liniePos[0]:
                            self.liniePos[2] = blockPositionFokus[0]
                            self.liniePos[3] = blockPositionFokus[1]
                            self.liniePos[5] = block['blockNr'] 
                            self.liniePos[6] = 'in2'
                            self.zeichne_line()
                            self.liniePos = [0, 0, 0, 0, '', '', '']  

            if 'objectNrInput3' in block:
                if block['objectNrInput3'] == blockFokusInput:
                    if 'inX3' in block:
                        blockPositionFokus[0] = block['inX3']
                        blockPositionFokus[1] = block['inY3']
                        blockPositionFokus[2] = block['blockNr'] 
                        blockPositionFokus[3] = 'in3'
                        if self.liniePos[0]:
                            self.liniePos[2] = blockPositionFokus[0]
                            self.liniePos[3] = blockPositionFokus[1]
                            self.liniePos[5] = block['blockNr'] 
                            self.liniePos[6] = 'in3'
                            self.zeichne_line()
                            self.liniePos = [0, 0, 0, 0, '', '', '']
                            
            if 'objectNrOutput' in block:
                if block['objectNrOutput'] == blockFokusInput:
                    if 'out1' in block:
                        blockPositionFokus[0] = block['outX1']
                        blockPositionFokus[1] = block['outY1']
                        blockPositionFokus[2] = block['blockNr'] 
                        blockPositionFokus[3] = 'out1'
                        self.liniePos[0] = blockPositionFokus[0]
                        self.liniePos[1] = blockPositionFokus[1]
                        self.liniePos[4] = block['blockNr'] 

            if 'objectNr' in block:
                if block['objectNr'] == blockFokusInput:
                        blockPositionFokus[0] = block['x']
                        blockPositionFokus[1] = block['y']
                        blockPositionFokus[2] = block['blockNr'] 
                        blockPositionFokus[3] = ''    

            if 'objectNrTextBlockTyp' in block:
                if block['objectNrTextBlockTyp'] == blockFokusInput:
                        blockPositionFokus[0] = block['x']
                        blockPositionFokus[1] = block['y']
                        blockPositionFokus[2] = block['blockNr'] 
                        blockPositionFokus[3] = '' 

        for comment in comments:
            if 'objectNr' in block:
                if comment['objectNr'] == blockFokusInput:
                        blockPositionFokus[0] = comment['x']
                        blockPositionFokus[1] = comment['y']
                        blockPositionFokus[2] = comment['commentNr'] 
                        blockPositionFokus[3] = ''     

        #print(blockPositionFokus)
        # wenn Out geklickt wird kreis zeichnen 
        if blockPositionFokus[3] == 'out1':
            if self.geklicktFokusBlockLetzter:      
                    for block in blocks:
                        if block['blockNr'] == self.geklicktFokusBlockLetzter:
                            self.main_window_frame.zeichenwand.itemconfig(block['objectNr'],
                                                                    fill='lightyellow')
            self.main_window_frame.zeichenwand.delete(self.geklicktFokus)
            self.geklicktFokus = self.main_window_frame.zeichenwand.create_oval(blockPositionFokus[0] - 10, blockPositionFokus[1] - 10
                                                                                , blockPositionFokus[0] + 10, blockPositionFokus[1] + 10, 
                                                                                outline="BLUE",
                                                                                fill="RED", width=2)
        # wenn in123 geklickt wird Kreis löschen(Fokus)
        if 'in' in blockPositionFokus[3]:
            if self.geklicktFokusBlockLetzter:      
                    for block in blocks:
                        if block['blockNr'] == self.geklicktFokusBlockLetzter:
                            self.main_window_frame.zeichenwand.itemconfig(block['objectNr'],
                                                                    fill='lightyellow')
            self.main_window_frame.zeichenwand.delete(self.geklicktFokus)

        # Fofus Block zeichnen
        if not blockPositionFokus[3]:
            if 'B' in blockPositionFokus[2]:
                if self.geklicktFokusBlockLetzter:      
                    for block in blocks:
                        if block['blockNr'] == self.geklicktFokusBlockLetzter:
                            self.main_window_frame.zeichenwand.itemconfig(block['objectNr'],
                                                                    fill='lightyellow')
                for block in blocks:
                    if block['blockNr'] == blockPositionFokus[2]:
                        self.main_window_frame.zeichenwand.delete(self.geklicktFokus)                    
                        self.main_window_frame.zeichenwand.itemconfig(block['objectNr'],                                                        
                                                                    fill='RED')
                        self.geklicktFokusBlockLetzter = blockPositionFokus[2]
        
        '''if self.main_window_frame.check_modbus.get() == 1:
            if self.lastX:
                l = self.main_window_frame.zeichenwand.create_line(self.lastX,self.lastY,event.x,event.y)
                self.lines.append(l)

            self.lastX = event.x
            self.lastY = event.y
            pass'''

    def motion(self, event):
        global blockPositionFokus
        if self.linieZeichnen:
            #if self.lastX != None:
            if self.redLine:
                self.main_window_frame.zeichenwand.delete(self.redLine);
            self.redLine = self.main_window_frame.zeichenwand.create_line(blockPositionFokus[0], blockPositionFokus[1],
                                            event.x, event.y, fill="red")
        x, y = event.x, event.y
        #print('{}, {}'.format(x, y))

    def drag(self, event):
        global blockPositionFokus, blocks, lines, comments

        '''if self.main_window_frame.check_modbus.get() == 1:
            #if self.lastX != None:
            if self.redLine:
                self.main_window_frame.zeichenwand.delete(self.redLine);
            self.redLine = self.main_window_frame.zeichenwand.create_line(self.lastX, self.lastY,
                                            event.x, event.y, fill="red")
            return None'''

        # Makierten Block verschieben
        widget = event.widget
        xc = widget.canvasx(event.x); yc = widget.canvasx(event.y)
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2] and not blockPositionFokus[3]:
                if 'objectNrInput1' in block:
                    self.main_window_frame.zeichenwand.move(block['objectNrInput1'], xc-self.previous[0], yc-self.previous[1])
                    pos = self.main_window_frame.zeichenwand.coords(block['objectNrInput1'])
                    block['inX1'] = int(pos[0])
                    block['inY1'] = int(pos[1])
                    if block['inY1']:
                        for line in lines:
                            if line['ziel'] == blockPositionFokus[2] and line['zielIn'] == 'in1':
                                self.x = line['x']
                                self.y = line['y']
                                self.x2 = block['inX1']
                                self.y2 = block['inY1']
                                self.linie_1_x2 = int(((self.x2 - self.x) / 2) + self.x)
                                self.linie_1_y2 = self.y
                                self.linie_2_x1 = self.linie_1_x2
                                self.linie_2_y1 = self.y
                                self.linie_2_x2 = self.linie_1_x2
                                self.linie_2_y2 = self.y2
                                self.linie_3_x1 = self.linie_1_x2
                                self.linie_3_y1 = self.y2
                                self.main_window_frame.zeichenwand.coords(line['objectNr'], line['x'], line['y'],
                                                                            self.linie_1_x2 , self.linie_1_y2)
                                self.main_window_frame.zeichenwand.coords(line['objectNr2'], self.linie_2_x1, self.linie_2_y1,
                                                                            self.linie_2_x2 , self.linie_2_y2)
                                self.main_window_frame.zeichenwand.coords(line['objectNr3'], self.linie_3_x1, self.linie_3_y1,
                                                                            self.x2 , self.y2)
                                line['x2'] = block['inX1']
                                line['y2'] = block['inY1']
                                line['l1_x2'] = self.linie_1_x2
                                line['l1_y2'] = self.linie_1_y2
                                line['l2_x1'] = self.linie_2_x1
                                line['l2_y1'] = self.linie_2_y1
                                line['l3_x1'] = self.linie_3_x1
                                line['l3_y1'] = self.linie_3_y1
                if 'objectNrInput2' in block:
                    self.main_window_frame.zeichenwand.move(block['objectNrInput2'], xc-self.previous[0], yc-self.previous[1])
                    pos = self.main_window_frame.zeichenwand.coords(block['objectNrInput2'])
                    block['inX2'] = int(pos[0])
                    block['inY2'] = int(pos[1])
                    if block['inY2']:
                        for line in lines:
                            if line['ziel'] == blockPositionFokus[2] and line['zielIn'] == 'in2':
                                self.x = line['x']
                                self.y = line['y']
                                self.x2 = block['inX2']
                                self.y2 = block['inY2']
                                self.linie_1_x2 = int(((self.x2 - self.x) / 2) + self.x)
                                self.linie_1_y2 = self.y
                                self.linie_2_x1 = self.linie_1_x2
                                self.linie_2_y1 = self.y
                                self.linie_2_x2 = self.linie_1_x2
                                self.linie_2_y2 = self.y2
                                self.linie_3_x1 = self.linie_1_x2
                                self.linie_3_y1 = self.y2
                                self.main_window_frame.zeichenwand.coords(line['objectNr'], line['x'], line['y'],
                                                                            self.linie_1_x2 , self.linie_1_y2)
                                self.main_window_frame.zeichenwand.coords(line['objectNr2'], self.linie_2_x1, self.linie_2_y1,
                                                                            self.linie_2_x2 , self.linie_2_y2)
                                self.main_window_frame.zeichenwand.coords(line['objectNr3'], self.linie_3_x1, self.linie_3_y1,
                                                                            self.x2 , self.y2)
                                line['x2'] = block['inX2']
                                line['y2'] = block['inY2']
                                line['l1_x2'] = self.linie_1_x2
                                line['l1_y2'] = self.linie_1_y2
                                line['l2_x1'] = self.linie_2_x1
                                line['l2_y1'] = self.linie_2_y1
                                line['l3_x1'] = self.linie_3_x1
                                line['l3_y1'] = self.linie_3_y1
                if 'objectNrInput3' in block:
                    self.main_window_frame.zeichenwand.move(block['objectNrInput3'], xc-self.previous[0], yc-self.previous[1])
                    pos = self.main_window_frame.zeichenwand.coords(block['objectNrInput3'])
                    block['inX3'] = int(pos[0])
                    block['inY3'] = int(pos[1])
                    if block['inY3']:
                        for line in lines:
                            if line['ziel'] == blockPositionFokus[2] and line['zielIn'] == 'in3':
                                self.x = line['x']
                                self.y = line['y']
                                self.x2 = block['inX3']
                                self.y2 = block['inY3']
                                self.linie_1_x2 = int(((self.x2 - self.x) / 2) + self.x)
                                self.linie_1_y2 = self.y
                                self.linie_2_x1 = self.linie_1_x2
                                self.linie_2_y1 = self.y
                                self.linie_2_x2 = self.linie_1_x2
                                self.linie_2_y2 = self.y2
                                self.linie_3_x1 = self.linie_1_x2
                                self.linie_3_y1 = self.y2
                                self.main_window_frame.zeichenwand.coords(line['objectNr'], line['x'], line['y'],
                                                                            self.linie_1_x2 , self.linie_1_y2)
                                self.main_window_frame.zeichenwand.coords(line['objectNr2'], self.linie_2_x1, self.linie_2_y1,
                                                                            self.linie_2_x2 , self.linie_2_y2)
                                self.main_window_frame.zeichenwand.coords(line['objectNr3'], self.linie_3_x1, self.linie_3_y1,
                                                                            self.x2 , self.y2)
                                line['x2'] = block['inX3']
                                line['y2'] = block['inY3']
                                line['l1_x2'] = self.linie_1_x2
                                line['l1_y2'] = self.linie_1_y2
                                line['l2_x1'] = self.linie_2_x1
                                line['l2_y1'] = self.linie_2_y1
                                line['l3_x1'] = self.linie_3_x1
                                line['l3_y1'] = self.linie_3_y1
                if 'objectNrOutput' in block:
                    self.main_window_frame.zeichenwand.move(block['objectNrOutput'], xc-self.previous[0], yc-self.previous[1])
                    pos = self.main_window_frame.zeichenwand.coords(block['objectNrOutput'])
                    block['outX1'] = int(pos[2])
                    block['outY1'] = int(pos[3])
                    if block['out1']:
                        for line in lines:
                            if line['start'] == blockPositionFokus[2]:
                                self.x = block['outX1']
                                self.y = block['outY1']
                                self.x2 = line['x2']
                                self.y2 = line['y2']
                                self.linie_1_x2 = int(((self.x2 - self.x) / 2) + self.x)
                                self.linie_1_y2 = self.y
                                self.linie_2_x1 = self.linie_1_x2
                                self.linie_2_y1 = self.y
                                self.linie_2_x2 = self.linie_1_x2
                                self.linie_2_y2 = self.y2
                                self.linie_3_x1 = self.linie_1_x2
                                self.linie_3_y1 = self.y2
                                self.main_window_frame.zeichenwand.coords(line['objectNr'], line['x'], line['y'],
                                                                            self.linie_1_x2 , self.linie_1_y2)
                                self.main_window_frame.zeichenwand.coords(line['objectNr2'], self.linie_2_x1, self.linie_2_y1,
                                                                            self.linie_2_x2 , self.linie_2_y2)
                                self.main_window_frame.zeichenwand.coords(line['objectNr3'], self.linie_3_x1, self.linie_3_y1,
                                                                            self.x2 , self.y2)
                                line['x'] = block['outX1']
                                line['y'] = block['outY1']
                                line['l1_x2'] = self.linie_1_x2
                                line['l1_y2'] = self.linie_1_y2
                                line['l2_x1'] = self.linie_2_x1
                                line['l2_y1'] = self.linie_2_y1
                                line['l3_x1'] = self.linie_3_x1
                                line['l3_y1'] = self.linie_3_y1
                if 'objectNr' in block:
                    self.main_window_frame.zeichenwand.move(block['objectNr'], xc-self.previous[0], yc-self.previous[1])
                    pos = self.main_window_frame.zeichenwand.coords(block['objectNr'])
                    block['x'] = int(pos[0])
                    block['y'] = int(pos[1])
                if 'objectNrTextBlockNr' in block:
                    self.main_window_frame.zeichenwand.move(block['objectNrTextBlockNr'], xc-self.previous[0], yc-self.previous[1])
                if 'objectNrTextBlockTyp' in block:
                    self.main_window_frame.zeichenwand.move(block['objectNrTextBlockTyp'], xc-self.previous[0], yc-self.previous[1])
                if 'objectTextTimerNr' in block:
                    self.main_window_frame.zeichenwand.move(block['objectTextTimerNr'], xc-self.previous[0], yc-self.previous[1])
                if 'objectParameterSet' in block:
                    self.main_window_frame.zeichenwand.move(block['objectParameterSet'], xc-self.previous[0], yc-self.previous[1])
                if 'objectParameterActual' in block:
                    self.main_window_frame.zeichenwand.move(block['objectParameterActual'], xc-self.previous[0], yc-self.previous[1]) 
                if 'objectTextSet' in block:
                    self.main_window_frame.zeichenwand.move(block['objectTextSet'], xc-self.previous[0], yc-self.previous[1])
                if 'objectTextReset' in block:
                    self.main_window_frame.zeichenwand.move(block['objectTextReset'], xc-self.previous[0], yc-self.previous[1])
                if 'objectTextIpNr' in block:
                    self.main_window_frame.zeichenwand.move(block['objectTextIpNr'], xc-self.previous[0], yc-self.previous[1])
                if 'objectTextCounterNr' in block:
                    self.main_window_frame.zeichenwand.move(block['objectTextCounterNr'], xc-self.previous[0], yc-self.previous[1])
                if 'objectParameterPreset' in block:
                    self.main_window_frame.zeichenwand.move(block['objectParameterPreset'], xc-self.previous[0], yc-self.previous[1])
                if 'objectTextUp' in block:
                    self.main_window_frame.zeichenwand.move(block['objectTextUp'], xc-self.previous[0], yc-self.previous[1])
                if 'objectTextDown' in block:
                    self.main_window_frame.zeichenwand.move(block['objectTextDown'], xc-self.previous[0], yc-self.previous[1])
                if 'objectParameter1' in block:
                    self.main_window_frame.zeichenwand.move(block['objectParameter1'], xc-self.previous[0], yc-self.previous[1])
                if 'objectParameter2' in block:
                    self.main_window_frame.zeichenwand.move(block['objectParameter2'], xc-self.previous[0], yc-self.previous[1])
                if 'objectParameter3' in block:
                    self.main_window_frame.zeichenwand.move(block['objectParameter3'], xc-self.previous[0], yc-self.previous[1])
                if 'objectParameter1actual' in block:
                    self.main_window_frame.zeichenwand.move(block['objectParameter1actual'], xc-self.previous[0], yc-self.previous[1])
                if 'objectParameter2actual' in block:
                    self.main_window_frame.zeichenwand.move(block['objectParameter2actual'], xc-self.previous[0], yc-self.previous[1])
                if 'objectParameter3actual' in block:
                    self.main_window_frame.zeichenwand.move(block['objectParameter3actual'], xc-self.previous[0], yc-self.previous[1])

        for comment in comments:
            if comment['commentNr'] == blockPositionFokus[2] and not blockPositionFokus[3]:
                if 'objectNr' in comment:
                    self.main_window_frame.zeichenwand.move(comment['objectNr'], xc-self.previous[0], yc-self.previous[1])
                    pos = self.main_window_frame.zeichenwand.coords(comment['objectNr'])
                    comment['x'] = int(pos[0])
                    comment['y'] = int(pos[1])
                if 'objectParameter1' in comment:
                    self.main_window_frame.zeichenwand.move(comment['objectParameter1'], xc-self.previous[0], yc-self.previous[1])
                if 'objectNrTextBlockNr' in comment:
                    self.main_window_frame.zeichenwand.move(comment['objectNrTextBlockNr'], xc-self.previous[0], yc-self.previous[1])

        self.previous = (xc, yc)
        #print(self.previous)

    def on_drop(self, event):
        widget = event.widget
        # find the widget under the cursor
        x,y = widget.winfo_pointerxy()
        #target = event.widget.winfo_containing(x,y)
        widget = widget.winfo_containing(x,y)
        #print("widget:", widget)
        try:
            pass
            #print("on drop", x, y)
        except:
            pass
    
    def double(self, event):
        #print("doubleKlick")      
        global blockPositionFokus, blocks, comments

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'INPUT':
                        self.show_dialog_block_input()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'TON':
                        self.onClickTon()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'TOF':
                        self.onClickTof()
        
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'CUD':
                        self.onClickCounter()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'LT':
                        self.onClickCompare()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'LIT':
                        self.onClickCompare()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'GT':
                        self.onClickCompare()
        
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'GIT':
                        self.onClickCompare()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'IT':
                        self.onClickCompare()
        
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'NIT':
                        self.onClickCompare()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'ADD':
                        self.onClickAritmetic()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'SUB':
                        self.onClickAritmetic()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'MUL':
                        self.onClickAritmetic()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'DIV':
                        self.onClickAritmetic()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'MOVE':
                        self.onClickMove()

        for comment in comments:
            if comment['commentNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if comment['typ'] == 'COMMENT':
                        self.onClickComment()

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                if 'typ' in block:
                    if block['typ'] == 'ZUW':
                        self.onClickOutput()

    def block_move_fokus(self, event):
        self.select(event)
        self.blockMove.append(blockPositionFokus[2])  
             
class Application(MouseMover):
    def __init__(self, main_win, title):
        MouseMover.__init__(self)
        self.main_win = main_win
        main_win.title(title)

        # Schliessung des Hauptfensters übder das 'x'-Symbol in der Titelleiste
        main_win.protocol("WM_DELETE_WINDOW", self.close_app)
        # Erstelle die Geometriedaten für ein zentriertes Hauptfenster
        geometry = self.center_win(main_win, MAIN_WIN_WIDTH, MAIN_WIN_HEIGHT)
        # Zentrier das Hauptfenster
        self.main_win.geometry("{}x{}+{}+{}".format(*geometry))
        # Erstelle den Inhalt des Hauptfensters
        self.main_window_frame = MainWindowFrame(self)
        # Variablen für Zeichnen
        self.achseX_x1 = 100
        self.achseX_x2 = 120
        self.achseY_y1 = 60
        self.achseY_y2 = 80
        self.lPx = 150
        self.lPy = 150

        # Varibale für aktuelle Datei ausgewählt
        self.selectFile = ''

        # Periodischer Aufruf
        self.sollwert_x_alt = 0

        #Anzahl der Blöcke un Linien
        self.aktuelleBlockNr = 0
        self.aktuelleLineNr = 0
        self.aktuelleInputNr = 0
        self.aktuelleOutputNr = 0
        self.aktuelleTonNr = 0
        self.aktuelleTofNr = 0
        self.aktuelleSrNr = 0
        self.aktuelleIpNr = 0
        self.aktuelleCudNr = 0
        self.aktuelleCommentNr = 0

        #Varibale Simulator ein
        self.simulatorEin = False
        self.runProgressbar = 0
        self.zyklusTimeOn = False

        # Variable für Programmänderung
        self.programChange = False

        # block fokus sammeln für verschieben
        self.blockMove = []

        # Bind mouse events to methods (could also be in the constructor)
        self.main_window_frame.zeichenwand.bind("<Button-1>", self.select)
        self.main_window_frame.zeichenwand.bind("<B1-Motion>", self.drag)
        #self.main_window_frame.zeichenwand.bind("<Motion>", self.motion)
        self.main_window_frame.zeichenwand.bind('<Double-Button-1>', self.double)
        self.main_window_frame.zeichenwand.bind("<ButtonRelease-1>", self.on_drop)
        self.main_window_frame.zeichenwand.bind("<Control-1 >", self.block_move_fokus)

    def center_win(self, window, width, height):
        xpos = int((window.winfo_screenwidth() - width) / 2)
        ypos = int((window.winfo_screenheight() - height) / 2)
        return width, height, xpos, ypos

    def close_app(self):
        global blocks
        # Here do something before apps shutdown
        yes = False
        if blocks:
            yes = tkinter.messagebox.askyesno('Close project', 'You are sure you delete all data, close program?')
            if not yes:
                return
            if yes:
                pass
        print("Good Bye!")
        self.main_win.withdraw()
        self.main_win.destroy()

    def onClickTon(self):
        global blockPositionFokus, blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # lade aktuelle Eintrag von Block
        parameter1 = 0
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                parameter1 = block['parameter1']

        tonDialog = DialogTon(self.main_win, parameter1)
        self.main_win.wait_window(tonDialog.top)

        # check input
        checkInput = self.check_input_timer_set(tonDialog.paramter1)
        if not checkInput:
            tkinter.messagebox.showerror('Timer', 'input incorrect, only 0 - 99999')
            return

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                block['parameter1'] = int(checkInput)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameterSet'], text= checkInput)
        #print('Username: ', tonDialog.paramter1)

        # Prgrammänderung
        self.programChange = True

    def onClickTof(self):
        global blockPositionFokus, blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # lade aktuelle Eintrag von Block
        parameter1 = 0
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                parameter1 = block['parameter1']

        tofDialog = DialogTof(self.main_win, parameter1)
        self.main_win.wait_window(tofDialog.top)

        # check input
        checkInput = self.check_input_timer_set(tofDialog.paramter1)
        if not checkInput:
            tkinter.messagebox.showerror('Timer', 'input incorrect, only 0 - 99999')
            return

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                block['parameter1'] = int(checkInput)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameterSet'], text= checkInput)
        #print('Username: ', tonDialog.paramter1)

        # Prgrammänderung
        self.programChange = True

    def onClickCounter(self):
        global blockPositionFokus, blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # lade aktuelle Eintrag von Block
        parameter1 = 0
        parameter2 = 0
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                parameter1 = block['parameter1']
                parameter2 = block['parameter2']

        counterDialog = DialogCounter(self.main_win, parameter1, parameter2)
        self.main_win.wait_window(counterDialog.top)

        # check input
        checkInput = self.check_input_int_value(counterDialog.paramter1)
        checkInput2 = self.check_input_int_value(counterDialog.paramter2)
        if not checkInput:
            tkinter.messagebox.showerror('Counter', 'input incorrect, only -99999 - 99999')
            return
        if not checkInput2:
            tkinter.messagebox.showerror('Counter', 'input incorrect, only -99999 - 99999')
            return

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                block['parameter1'] = int(checkInput)
                block['parameter2'] = int(checkInput2)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameterPreset'], text= checkInput)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameterSet'], text= checkInput2)
        
        # Prgrammänderung
        self.programChange = True

    def onClickCompare(self):
        global blockPositionFokus, blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # lade aktuelle Eintrag von Block
        parameter1 = '0'
        parameter2 = '0'
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                parameter1 = block['parameter1']
                parameter2 = block['parameter2']

        compareDialog = DialogLt(self.main_win, parameter1, parameter2)
        self.main_win.wait_window(compareDialog.top)

        # check input
        # prüfen ob es eine dezimalzahl ist mit minus vorzeichen
        valueInt1 = self.check_int(compareDialog.paramter1)
        if valueInt1:
            checkInput = self.check_input_int_value(compareDialog.paramter1)
        else:
            checkInput = self.check_input_mw_cud_ton_tof(compareDialog.paramter1)

        valueInt2 = self.check_int(compareDialog.paramter2)
        if valueInt2:
            checkInput2 = self.check_input_int_value(compareDialog.paramter2)
        else:
            checkInput2 = self.check_input_mw_cud_ton_tof(compareDialog.paramter2)

        if not checkInput:
            tkinter.messagebox.showerror('Counter', 'input1 incorrect, only -99999 - 99999, MW1 - 1000, \
                                         CUD1 - 1000, TOF1 - 1000, TOF1 - 1000')
            return
        if not checkInput2:
            tkinter.messagebox.showerror('Counter', 'input2 incorrect, only -99999 - 99999, MW1 - 1000, \
                                         CUD1 - 1000, TOF1 - 1000, TOF1 - 1000')
            return

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                block['parameter1'] = checkInput
                block['parameter2'] = checkInput2
                block['in1'] = checkInput
                block['in2'] = checkInput2
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter1'], text= checkInput)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter1actual'], text= checkInput)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter2'], text= checkInput2)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter2actual'], text= checkInput2)
        
        # Prgrammänderung
        self.programChange = True

    def onClickAritmetic(self):
        global blockPositionFokus, blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # lade aktuelle Eintrag von Block
        parameter1 = 0
        parameter2 = 0
        parameter3 = 0
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                parameter1 = block['parameter1']
                parameter2 = block['parameter2']
                parameter3 = block['parameter3']

        aritmeticreDialog = DialogAritmetic(self.main_win, parameter1, parameter2, parameter3)
        self.main_win.wait_window(aritmeticreDialog.top)

        # check input
        # prüfen ob es eine dezimalzahl ist mit minus vorzeichen
        valueInt1 = self.check_int(aritmeticreDialog.paramter1)
        if valueInt1:
            checkInput = self.check_input_int_value(aritmeticreDialog.paramter1)
        else:
            checkInput = self.check_input_mw_cud_ton_tof(aritmeticreDialog.paramter1)

        valueInt2 = self.check_int(aritmeticreDialog.paramter2)
        if valueInt2:
            checkInput2 = self.check_input_int_value(aritmeticreDialog.paramter2)
        else:
            checkInput2 = self.check_input_mw_cud_ton_tof(aritmeticreDialog.paramter2)

        valueInt3 = self.check_int(aritmeticreDialog.paramter3)
        if valueInt3:
            checkInput3 = self.check_input_int_value(aritmeticreDialog.paramter3)
        else:
            checkInput3 = self.check_input_mw(aritmeticreDialog.paramter3)

        if not checkInput:
            tkinter.messagebox.showerror('Math', 'input1 incorrect, only -99999 - 99999, MW1 - 1000, \
                                         CUD1 - 1000, TOF1 - 1000, TOF1 - 1000')
            return
        if not checkInput2:
            tkinter.messagebox.showerror('Math', 'input2 incorrect, only -99999 - 99999, MW1 - 1000, \
                                         CUD1 - 1000, TOF1 - 1000, TOF1 - 1000')
            return
        
        if not checkInput3:
            tkinter.messagebox.showerror('Math', 'output incorrect, only MW1 - 1000')
            return

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                block['parameter1'] = checkInput
                block['parameter2'] = checkInput2
                block['parameter3'] = checkInput3
                block['in2'] = checkInput
                block['in3'] = checkInput2
                block['out1'] = checkInput3
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter1'], text= checkInput)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter1actual'], text= checkInput)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter2'], text= checkInput2)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter2actual'], text= checkInput2)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter3'], text= checkInput3)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter3actual'], text= checkInput3)

        # Prgrammänderung
        self.programChange = True

    def onClickMove(self):
        global blockPositionFokus, blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # lade aktuelle Eintrag von Block
        parameter1 = '0'
        parameter2 = '0'
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                parameter1 = block['parameter1']
                parameter2 = block['parameter2']

        moveDialog = DialogMove(self.main_win, parameter1, parameter2)
        self.main_win.wait_window(moveDialog.top)

        # check input
        # prüfen ob es eine dezimalzahl ist mit minus vorzeichen
        valueInt1 = self.check_int(moveDialog.paramter1)
        if valueInt1:
            checkInput = self.check_input_int_value(moveDialog.paramter1)
        else:
            checkInput = self.check_input_mw_cud_ton_tof(moveDialog.paramter1)

        valueInt2 = self.check_int(moveDialog.paramter2)
        if valueInt2:
            checkInput2 = self.check_input_int_value(moveDialog.paramter2)
        else:
            checkInput2 = self.check_input_mw_cud_ton_tof(moveDialog.paramter2)

        if not checkInput:
            tkinter.messagebox.showerror('Move', 'input1 incorrect, only -99999 - 99999, MW1 - 1000, \
                                         CUD1 - 1000, TOF1 - 1000, TOF1 - 1000')
            return
        if not checkInput2:
            tkinter.messagebox.showerror('Move', 'input2 incorrect, only -99999 - 99999, MW1 - 1000, \
                                         CUD1 - 1000, TOF1 - 1000, TOF1 - 1000')
            return

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                block['parameter1'] = checkInput
                block['parameter2'] = checkInput2
                block['in2'] = checkInput
                block['out1'] = checkInput2
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter1'], text= checkInput)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter1actual'], text= checkInput)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter2'], text= checkInput2)
                self.main_window_frame.zeichenwand.itemconfig(block['objectParameter2actual'], text= checkInput2)

        # Prgrammänderung
        self.programChange = True

    def onClickComment(self):
        global blockPositionFokus, comments

        # lade aktuelle Eintrag von Block
        parameter1 = 'Text'
        for comment in comments:
            if comment['commentNr'] == blockPositionFokus[2]:
                parameter1 = comment['parameter1']

        commentDialog = DialogComment(self.main_win, parameter1)
        self.main_win.wait_window(commentDialog.top)

        for comment in comments:
            if comment['commentNr'] == blockPositionFokus[2]:
                comment['parameter1'] = commentDialog.paramter1
                self.main_window_frame.zeichenwand.itemconfig(comment['objectParameter1'], text= commentDialog.paramter1)

    def onClickOutput(self):
        global blockPositionFokus, blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # lade aktuelle Eintrag von Block
        outNr = ''
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                outNr = block['OUT']

        outputDialog = DialogOutput(self.main_win, outNr)
        self.main_win.wait_window(outputDialog.top)

        # check input
        checkInput = self.check_input_block_output(outputDialog.paramter1)
        if not checkInput:
            tkinter.messagebox.showerror('Output', 'input incorrect')
            return

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                block['OUT'] = checkInput # alt outputDialog.paramter1
                self.main_window_frame.zeichenwand.itemconfig(block['objectNrTextBlockTyp'], text= checkInput)
        
        # Prgrammänderung
        self.programChange = True

    def dialog_block_input(self, app):
        global blockPositionFokus, blocks
        inputNr = ''
        blockNr = ''
        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                inputNr = block['in1']
                blockNr = blockPositionFokus[2]

        dialog = DialogBlockInput(title="Block Input", parent=app, blockNrFockus=blockNr, inputNrFockus=inputNr)
        return dialog.blockNr, dialog.inputNr

    def show_dialog_block_input(self):
        global blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        answer = self.dialog_block_input(self.main_win)

        # check input
        checkInput = self.check_input_block_input(answer[1])
        if not checkInput:
            tkinter.messagebox.showerror('Input', 'input incorrect')
            return

        for block in blocks:
            if block['blockNr'] == answer[0]:
                block['in1'] = checkInput # alt answer[1]
                self.main_window_frame.zeichenwand.itemconfig(block['objectNrTextBlockTyp'], text= checkInput)
                #self.main_window_frame.zeichenwand.itemconfig(block['objectNrTextBlockTyp'], text= answer[1]) alt
        #print(answer)

        # Prgrammänderung
        self.programChange = True

    def onClickInformation(self):
        tkinter.messagebox.showinfo("Information", \
        "pyblockplc Freeware                                                        \
        -----------------------------------------------------------------   \
        Created with :\
        Tkinter\
        Python 3.7\
        -----------------------------------------------------------------        \
        This Programm is experimental there no garantie.                    You use in your own risk. \
        Copyright by Herbert Schneider ")
    
    def check_input_block_input(self, value):
        checkValue = str(value)
        checkValue = checkValue.upper()
        checkValue = checkValue.lstrip()
        zeichen = checkValue[0]
        zahl = checkValue[1:]
        zahl = zahl.lstrip()
        zahl = zahl.rstrip()
        zeichenOk = False
        zahlOk = False
        #print(zeichen)
        #print(zahl)
        # Zeichen überprüfen
        if zeichen == 'I' or zeichen == 'B':
            zeichenOk = True
        else:
            return False
        # Zahl überprüfen
        if int(zahl) > 0 and int(zahl) < 1000:
            zahlOk = True
        else:
            return False
        #Ergbenis überprüfen
        if zeichenOk and zahlOk:
            return str(zeichen) + str(zahl)
        else:
            return False

    def check_input_block_output(self, value):
            checkValue = str(value)
            checkValue = checkValue.upper()
            checkValue = checkValue.lstrip()
            zeichen = checkValue[0]
            zahl = checkValue[1:]
            zahl = zahl.lstrip()
            zahl = zahl.rstrip()
            zeichenOk = False
            zahlOk = False
            #print(zeichen)
            #print(zahl)
            # Zeichen überprüfen
            if zeichen == 'Q':
                zeichenOk = True
            else:
                return False
            # Zahl überprüfen
            if int(zahl) > 0 and int(zahl) < 1000:
                zahlOk = True
            else:
                return False
            #Ergbenis überprüfen
            if zeichenOk and zahlOk:
                return str(zeichen) + str(zahl)
            else:
                return False

    def check_input_timer_set(self, value):
            checkValue = str(value)
            checkValue = checkValue.lstrip()
            checkValue = checkValue.rstrip()

            # prüfen ob es eine dezimalzahl ist
            if checkValue.isdecimal():
                zahl = str(checkValue)
            else:
                return False
            zahlOk = False
            #print(zeichen)
            #print(zahl)

            # Zahl überprüfen
            if int(zahl) >= 0 and int(zahl) < 100000:
                zahlOk = True
            else:
                return False

            #Ergbenis überprüfen
            if zahlOk:
                return str(zahl)
            else:
                return False

    def check_input_int_value(self, value):
            checkValue = str(value)
            checkValue = checkValue.lstrip()
            checkValue = checkValue.rstrip()

            # prüfen ob es eine dezimalzahl ist
            if checkValue[0] == '-':
                valueInt = checkValue[1:]
                if valueInt.isdecimal():
                    zahl = str(checkValue)
                else:
                    return False
            else:
                if checkValue.isdecimal():
                    zahl = str(checkValue)
                else:
                    return False

            zahlOk = False
            #print(zeichen)
            #print(zahl)

            # Zahl überprüfen
            if int(zahl) > -100000 and int(zahl) < 100000:
                zahlOk = True
            else:
                print('zahl prüfen false')
                return False

            #Ergbenis überprüfen
            if zahlOk:
                return str(zahl)
            else:
                return False

    def check_int(self, value):
            checkValue = str(value)
            checkValue = checkValue.lstrip()
            checkValue = checkValue.rstrip()

            # prüfen ob es eine dezimalzahl ist
            if checkValue[0] == '-':
                valueInt = checkValue[1:]
                if valueInt.isdecimal():
                    zahl = str(checkValue)
                else:
                    return False
            else:
                if checkValue.isdecimal():
                    zahl = str(checkValue)
                else:
                    return False

            zahlOk = False
            #print(zeichen)
            #print(zahl)

            # Zahl überprüfen
            if int(zahl) > -100000 and int(zahl) < 100000:
                zahlOk = True
            else:
                print('zahl prüfen false')
                return False

            #Ergbenis überprüfen
            if zahlOk:
                return True
            else:
                return False

    def check_input_mw_cud_ton_tof(self, value):
        checkValue = str(value)
        checkValue = checkValue.upper()
        checkValue = checkValue.lstrip()
        # welcher typ mw cud ton tof
        zeichen = ''
        if 'MW' in checkValue:
            zeichen = checkValue[:2]
            zahl = checkValue[2:]
            zahl = zahl.lstrip()
            zahl = zahl.rstrip()
        if 'CUD' in checkValue:
            zeichen = checkValue[:3]
            zahl = checkValue[3:]
            zahl = zahl.lstrip()
            zahl = zahl.rstrip()
        if 'TON' in checkValue:
            zeichen = checkValue[:3]
            zahl = checkValue[3:]
            zahl = zahl.lstrip()
            zahl = zahl.rstrip()
        if 'TOF' in checkValue:
            zeichen = checkValue[:3]
            zahl = checkValue[3:]
            zahl = zahl.lstrip()
            zahl = zahl.rstrip()
        
        zeichenOk = False
        zahlOk = False
        #print(zeichen)
        #print(zahl)
        # Zeichen überprüfen
        if zeichen == 'MW' or zeichen == 'CUD' or zeichen == 'TON' or zeichen == 'TOF':
            zeichenOk = True
        else:
            return False
        # Zahl überprüfen
        if int(zahl) > 0 and int(zahl) < 1000:
            zahlOk = True
        else:
            return False
        #Ergbenis überprüfen
        if zeichenOk and zahlOk:
            return str(zeichen) + str(zahl)
        else:
            return False

    def check_input_mw(self, value):
        checkValue = str(value)
        checkValue = checkValue.upper()
        checkValue = checkValue.lstrip()
        # welcher typ mw cud ton tof
        zeichen = ''
        if 'MW' in checkValue:
            zeichen = checkValue[:2]
            zahl = checkValue[2:]
            zahl = zahl.lstrip()
            zahl = zahl.rstrip()
        
        zeichenOk = False
        zahlOk = False
        #print(zeichen)
        #print(zahl)
        # Zeichen überprüfen
        if zeichen == 'MW':
            zeichenOk = True
        else:
            return False
        # Zahl überprüfen
        if int(zahl) > 0 and int(zahl) < 1000:
            zahlOk = True
        else:
            return False
        #Ergbenis überprüfen
        if zeichenOk and zahlOk:
            return str(zeichen) + str(zahl)
        else:
            return False

    def onClickSetting(self):
        settingDialog = DialogSetting(self.main_win)
        self.main_win.wait_window(settingDialog.top)

        # Look is a entry( ist ein exe Pfad eingetragen)
        global uploadPathExe
        configDaten = {'uploadPathExe': ''}
        if settingDialog.paramter1:
            uploadPathExe = settingDialog.paramter1
            configDaten['uploadPathExe'] = str(uploadPathExe)
            try:
                with open('config.txt', 'w') as fp:
                    json.dump(configDaten, fp)
            except:
                print('Conig File not Write')

    def loeschen_block(self):       
        global blockFokusInput
        self.main_window_frame.zeichenwand.delete(blockFokusInput)
        
    def block_input_erzeugen(self, Nr, typ):
        self.x = 140
        self.y = 140
        self.breite = 40
        self.hoehe = 20
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x + self.breite + 5 ,
                                                                            self.y + self.hoehe -5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= typ )
        
        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'objectNrOutput': self.objectNrOutput,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'typ': 'INPUT', 'in1': typ,
                'out1': ''}

    def block_input_erzeugen_von_file(self, Nr, typ, x, y):
        self.x = x
        self.y = y
        self.breite = 40
        self.hoehe = 20
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x + self.breite + 5 ,
                                                                            self.y + self.hoehe -5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= typ )
        
        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'objectNrOutput': self.objectNrOutput,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'outX1': (self.x - 5), 'outY1': (self.y + self.hoehe - 5),
                'typ': 'INPUT', 'in1': typ,
                'out1': ''}

    def block_zuweisung_erzeugen(self, Nr, typ):
        self.x = 140
        self.y = 140
        self.breite = 40
        self.hoehe = 20
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= typ )
        
        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'objectNrInput1': self.objectNrInput1,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'inX1': (self.x - 5), 'inY1': (self.y + self.hoehe - 5),
                'typ': 'ZUW', 'OUT': typ,
                'in1': ''}
    
    def block_zuweisung_erzeugen_von_file(self, Nr, typ, x, y):
        self.x = x
        self.y = y
        self.breite = 40
        self.hoehe = 20
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= typ )
        
        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'objectNrInput1': self.objectNrInput1,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'inX1': (self.x - 5), 'inY1': (self.y + self.hoehe - 5),
                'typ': 'ZUW', 'OUT': typ,
                'in1': ''}

    def block_timer(self, Nr, x, y, typ, parameter1):
        self.x = x
        self.y = y
        self.breite = 40
        self.hoehe = 40
        nrTon = typ.isdigit()
        typVar = ''
        if 'TON' in typ:
            typVar = 'TON'
        if 'TOF' in typ:
            typVar = 'TOF'
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + 5,
                                                                            self.x,
                                                                            self.y + 5), width=5, fill="Black")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x + self.breite + 5 ,
                                                                            self.y + self.hoehe -5), width=5, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= typVar )
        self.objectTextTimerNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + self.hoehe + 10), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= typ )
        self.objectParameterSet = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + self.hoehe + 20), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter1 )
        self.objectParameterActual = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + self.hoehe + 30), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter1 )

        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'inX1': (self.x - 5), 'inY1': (self.y + 5),
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'in1': '', 'out1': '', 'timerNr': typ,
                'typ': typVar, 'parameter1': parameter1,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'objectTextTimerNr': self.objectTextTimerNr,
                'objectParameterSet': self.objectParameterSet,
                'objectParameterActual': self.objectParameterActual,
                'objectNrInput1': self.objectNrInput1,
                'objectNrOutput': self.objectNrOutput}

    def block_and_2(self, Nr, x, y, typ):
        self.x = x
        self.y = y
        self.breite = 40
        self.hoehe = 40
        typVar = ''
        if typ == '>I':
            typVar = 'OR'
        if typ == '&':
            typVar = 'AND'
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + 5,
                                                                            self.x,
                                                                            self.y + 5), width=2, fill="Black")
        self.objectNrInput2 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x + self.breite + 5 ,
                                                                            self.y + self.hoehe -5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= typ )

        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'inX1': (self.x - 5), 'inY1': (self.y + 5),
                'inX2': (self.x - 5), 'inY2': (self.y + self.hoehe - 5),
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'in1': '', 'in2': '', 'out1': '',
                'typ': typVar,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'objectNrInput1': self.objectNrInput1,
                'objectNrInput2': self.objectNrInput2,
                'objectNrOutput': self.objectNrOutput}

    def block_compare_erzeugen(self, Nr, x, y, typ, parameter1, parameter2):
        self.x = x
        self.y = y
        self.breite = 40
        self.hoehe = 40
        typVar = ''
        if typ == '<I':
            typVar = 'LT'
        if typ == '>I':
            typVar = 'GT'
        if typ == '<=I':
            typVar = 'LIT'
        if typ == '>=I':
            typVar = 'GIT'
        if typ == '==I':
            typVar = 'IT'
        if typ == '!=I':
            typVar = 'NIT'
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + 5,
                                                                            self.x,
                                                                            self.y + 5), width=2, fill="Black")
        self.objectNrInput2 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x + self.breite + 5 ,
                                                                            self.y + self.hoehe -5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= typ )
        self.objectParameter1 = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter1 )
        self.objectParameter2 = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + self.hoehe - 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter2 )
        self.objectParameter1actual = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + 15), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter1 )
        self.objectParameter2actual = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + self.hoehe + 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter2 )

        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'inX1': (self.x - 5), 'inY1': (self.y + 5),
                'inX2': (self.x - 5), 'inY2': (self.y + self.hoehe - 5),
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'in1': parameter1, 'in2': parameter2, 'out1': '',
                'typ': typVar, 'parameter1': parameter1, 'parameter2': parameter2,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'objectParameter1': self.objectParameter1,
                'objectParameter2': self.objectParameter2,
                'objectParameter1actual': self.objectParameter1actual,
                'objectParameter2actual': self.objectParameter2actual,
                'objectNrInput1': self.objectNrInput1,
                'objectNrInput2': self.objectNrInput2,
                'objectNrOutput': self.objectNrOutput}

    def block_aritmetic_erzeugen(self, Nr, x, y, typ, parameter1, parameter2, parameter3):
        self.x = x
        self.y = y 
        self.breite = 40
        self.hoehe = 80
        typVar = ''
        if typ == 'ADD':
            typVar = 'ADD'
        if typ == 'SUB':
            typVar = 'SUB'
        if typ == 'MUL':
            typVar = 'MUL'
        if typ == 'DIV':
            typVar = 'DIV'
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + 5,
                                                                            self.x,
                                                                            self.y + 5), width=2, fill="Black")
        self.objectNrInput2 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + (self.hoehe/2),
                                                                            self.x,
                                                                            self.y + (self.hoehe/2)), width=2, fill="Black")
        self.objectNrInput3 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x + self.breite + 5,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= typ )
        self.objectParameter1 = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + (self.hoehe / 2) + 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter1 )
        self.objectParameter2 = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + self.hoehe - 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter2 )
        self.objectParameter3 = self.main_window_frame.zeichenwand.create_text((self.x + self.breite + 20), (self.y + self.hoehe - 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter3 )
        self.objectParameter1actual = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + (self.hoehe / 2) + 15), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter1 )
        self.objectParameter2actual = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + self.hoehe + 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter2 )
        self.objectParameter3actual = self.main_window_frame.zeichenwand.create_text((self.x + self.breite + 20), (self.y + self.hoehe + 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter3 )

        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'inX1': (self.x - 5), 'inY1': (self.y + 5),
                'inX2': (self.x - 5), 'inY2': (self.y + (self.hoehe/2)),
                'inX3': (self.x - 5), 'inY3': (self.y + self.hoehe - 5),
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'in1': '', 'in2': '', 'in3': '', 'out1': '',
                'typ': typVar,
                'parameter1': parameter1, 'parameter2': parameter2, 'parameter3': parameter3,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'objectParameter1': self.objectParameter1,
                'objectParameter2': self.objectParameter2,
                'objectParameter3': self.objectParameter3,
                'objectParameter1actual': self.objectParameter1actual,
                'objectParameter2actual': self.objectParameter2actual,
                'objectParameter3actual': self.objectParameter3actual,
                'objectNrInput1': self.objectNrInput1,
                'objectNrInput2': self.objectNrInput2,
                'objectNrInput3': self.objectNrInput3,
                'objectNrOutput': self.objectNrOutput}

    def block_move_erzeugen(self, Nr, x, y, parameter1, parameter2):
        self.x = x
        self.y = y 
        self.breite = 40
        self.hoehe = 40
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + 5,
                                                                            self.x,
                                                                            self.y + 5), width=2, fill="Black")
        self.objectNrInput2 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x + self.breite + 5,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 8 italic bold",
                                                        text= 'MOVE' )
        self.objectParameter1 = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + self.hoehe - 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter1 )
        self.objectParameter2 = self.main_window_frame.zeichenwand.create_text((self.x + self.breite + 20), (self.y + self.hoehe - 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter2 )
        self.objectParameter1actual = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + self.hoehe + 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter1 )
        self.objectParameter2actual = self.main_window_frame.zeichenwand.create_text((self.x + self.breite + 20), (self.y + self.hoehe + 5), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter2 )

        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'inX1': (self.x - 5), 'inY1': (self.y + 5),
                'inX2': (self.x - 5), 'inY2': (self.y + (self.hoehe/2)),
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'in1': '', 'in2': '', 'out1': '',
                'typ': 'MOVE',
                'parameter1': parameter1, 'parameter2': parameter2,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'objectParameter1': self.objectParameter1,
                'objectParameter2': self.objectParameter2,
                'objectParameter1actual': self.objectParameter1actual,
                'objectParameter2actual': self.objectParameter2actual,
                'objectNrInput1': self.objectNrInput1,
                'objectNrInput2': self.objectNrInput2,
                'objectNrOutput': self.objectNrOutput}

    def block_comment_erzeugen(self, Nr, x, y, parameter1):
        self.x = x
        self.y = y 
        self.breite = 10
        self.hoehe = 10
        self.objectNr = self.main_window_frame.zeichenwand.create_oval((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="lightblue")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x - 20), (self.y + (self.hoehe / 2)), 
                                                        fill="black",font="Times 8 italic bold", anchor="w",
                                                        text= Nr )
        self.objectParameter1 = self.main_window_frame.zeichenwand.create_text((self.x + self.breite + 5), (self.y + (self.hoehe / 2)), 
                                                        fill="black",font="Times 12 italic bold", anchor="w",
                                                        text= parameter1 )

        return {'objectNr': self.objectNr, 'commentNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'typ': 'COMMENT',
                'parameter1': parameter1, 
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectParameter1': self.objectParameter1}

    def block_inv_erzeugen(self, Nr, x, y, typ):
        self.x = x
        self.y = y
        self.breite = 40
        self.hoehe = 20
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + 10,
                                                                            self.x,
                                                                            self.y + 10), width=2, fill="Black")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 10,
                                                                            self.x + self.breite + 5 ,
                                                                            self.y + self.hoehe - 10), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= typ )

        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'inX1': (self.x - 5), 'inY1': (self.y + 5),
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'in1': '', 'out1': '',
                'typ': typ,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'objectNrInput1': self.objectNrInput1,
                'objectNrOutput': self.objectNrOutput}

    def block_ip_erzeugen(self, Nr, x, y, typ):
        self.x = x
        self.y = y
        self.breite = 40
        self.hoehe = 20
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + 10,
                                                                            self.x,
                                                                            self.y + 10), width=2, fill="Black")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 10,
                                                                            self.x + self.breite + 5 ,
                                                                            self.y + self.hoehe - 10), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= 'IP' )
        self.objectTextIpNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + self.hoehe + 10), 
                                                        fill="gray",font="Times 8 italic bold",
                                                        text= typ )

        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'inX1': (self.x - 5), 'inY1': (self.y + 5),
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'in1': '', 'out1': '',
                'typ': 'IP', 'ipNr': typ,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'objectTextIpNr': self.objectTextIpNr,
                'objectNrInput1': self.objectNrInput1,
                'objectNrOutput': self.objectNrOutput}

    def block_sr_rs(self, Nr, x, y, typ):
        self.x = x
        self.y = y
        self.breite = 40
        self.hoehe = 40
        typVar = ''
        if 'SR' in typ:
            typVar = 'SR'
        if 'RS' in typ:
            typVar = 'RS'
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + 5,
                                                                            self.x,
                                                                            self.y + 5), width=2, fill="Black")
        self.objectNrInput2 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x + self.breite + 5 ,
                                                                            self.y + self.hoehe -5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 10 italic bold",
                                                        text= typ )
        self.objectTextSet = self.main_window_frame.zeichenwand.create_text((self.x - 5), (self.y + 15), 
                                                        fill="gray",font="Times 8 italic bold",
                                                        text= 'S' )
        self.objectTextReset = self.main_window_frame.zeichenwand.create_text((self.x - 5), (self.y + self.hoehe + 5), 
                                                        fill="gray",font="Times 8 italic bold",
                                                        text= 'R' )

        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'inX1': (self.x - 5), 'inY1': (self.y + 5),
                'inX2': (self.x - 5), 'inY2': (self.y + self.hoehe - 5),
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'in1': '', 'in2': '', 'out1': '',
                'typ': typVar, 'srNr': typ,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'objectTextSet': self.objectTextSet,
                'objectTextReset': self.objectTextReset,
                'objectNrInput1': self.objectNrInput1,
                'objectNrInput2': self.objectNrInput2,
                'objectNrOutput': self.objectNrOutput}

    def block_cud_erzeugen(self, Nr, x, y, typ, parameter1, parameter2):
        self.x = x
        self.y = y 
        self.breite = 40
        self.hoehe = 80
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + 5,
                                                                            self.x,
                                                                            self.y + 5), width=2, fill="Black")
        self.objectNrInput2 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + (self.hoehe/2),
                                                                            self.x,
                                                                            self.y + (self.hoehe/2)), width=2, fill="Black")
        self.objectNrInput3 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x + self.breite + 5,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= 'CUD' )
        self.objectTextCounterNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + self.hoehe + 10), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= typ )
        self.objectParameterPreset = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + self.hoehe + 20), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter1 )
        self.objectParameterSet = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + self.hoehe + 30), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter2 )
        self.objectParameterActual = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + self.hoehe + 40), 
                                                        fill="gray",font="Times 10 italic bold",
                                                        text= parameter1 )
        self.objectTextUp = self.main_window_frame.zeichenwand.create_text((self.x - 5), (self.y + 15), 
                                                        fill="gray",font="Times 8 italic bold",
                                                        text= 'UP' )
        self.objectTextDown = self.main_window_frame.zeichenwand.create_text((self.x - 5), (self.y + (self.hoehe / 2) + 10), 
                                                        fill="gray",font="Times 8 italic bold",
                                                        text= 'DOWN' )
        self.objectTextSet = self.main_window_frame.zeichenwand.create_text((self.x - 5), (self.y + self.hoehe + 5), 
                                                        fill="gray",font="Times 8 italic bold",
                                                        text= 'SET' )

        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'inX1': (self.x - 5), 'inY1': (self.y + 5),
                'inX2': (self.x - 5), 'inY2': (self.y + (self.hoehe/2)),
                'inX3': (self.x - 5), 'inY3': (self.y + self.hoehe - 5),
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'in1': '', 'in2': '', 'in3': '', 'out1': '',
                'typ': 'CUD', 'cudNr': typ,
                'parameter1': parameter1, 'parameter2': parameter2,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'objectTextCounterNr': self.objectTextCounterNr,
                'objectParameterPreset': self.objectParameterPreset,
                'objectParameterSet': self.objectParameterSet,
                'objectParameterActual': self.objectParameterActual,
                'objectTextUp': self.objectTextUp,
                'objectTextDown': self.objectTextDown,
                'objectTextSet': self.objectTextSet,
                'objectNrInput1': self.objectNrInput1,
                'objectNrInput2': self.objectNrInput2,
                'objectNrInput3': self.objectNrInput3,
                'objectNrOutput': self.objectNrOutput}

    def block_and_3(self, Nr, x, y, typ):
        self.x = x
        self.y = y 
        self.breite = 40
        self.hoehe = 80
        typVar = ''
        if typ == '>I':
            typVar = 'OR'
        if typ == '&':
            typVar = 'AND'
        self.objectNr = self.main_window_frame.zeichenwand.create_rectangle((self.x,
                                                                            self.y,
                                                                            self.x + self.breite,
                                                                            self.y + self.hoehe), width=1, fill="Lightyellow")
        self.objectNrInput1 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + 5,
                                                                            self.x,
                                                                            self.y + 5), width=2, fill="Black")
        self.objectNrInput2 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + (self.hoehe/2),
                                                                            self.x,
                                                                            self.y + (self.hoehe/2)), width=2, fill="Black")
        self.objectNrInput3 = self.main_window_frame.zeichenwand.create_line((self.x - 5,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrOutput = self.main_window_frame.zeichenwand.create_line((self.x + self.breite,
                                                                            self.y + self.hoehe - 5,
                                                                            self.x + self.breite + 5,
                                                                            self.y + self.hoehe - 5), width=2, fill="Black")
        self.objectNrTextBlockNr = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y - 5), 
                                                        fill="darkblue",font="Times 10 italic bold",
                                                        text= Nr )
        self.objectNrTextBlockTyp = self.main_window_frame.zeichenwand.create_text((self.x + 20), (self.y + 10), 
                                                        fill="black",font="Times 12 italic bold",
                                                        text= typ )

        return {'objectNr': self.objectNr, 'blockNr': Nr, 'x': self.x, 
                'y': self.y, 'breite': self.breite, 'hoehe': self.hoehe,
                'inX1': (self.x - 5), 'inY1': (self.y + 5),
                'inX2': (self.x - 5), 'inY2': (self.y + (self.hoehe/2)),
                'inX3': (self.x - 5), 'inY3': (self.y + self.hoehe - 5),
                'outX1': (self.x + self.breite), 'outY1': (self.y + self.hoehe - 5),
                'in1': '', 'in2': '', 'in3': '', 'out1': '',
                'typ': typVar,
                'objectNrTextBlockNr': self.objectNrTextBlockNr,
                'objectNrTextBlockTyp': self.objectNrTextBlockTyp,
                'objectNrInput1': self.objectNrInput1,
                'objectNrInput2': self.objectNrInput2,
                'objectNrInput3': self.objectNrInput3,
                'objectNrOutput': self.objectNrOutput}

    def line(self, lineNummer, positionDaten):
        self.x = positionDaten[0]
        self.y = positionDaten[1]
        self.x2 = positionDaten[2]
        self.y2 = positionDaten[3]
        self.linie_1_x2 = int(((self.x2 - self.x) / 2) + self.x)
        self.linie_1_y2 = positionDaten[1]
        self.linie_2_x1 = self.linie_1_x2
        self.linie_2_y1 = positionDaten[1]
        self.linie_2_x2 = self.linie_1_x2
        self.linie_2_y2 = positionDaten[3]
        self.linie_3_x1 = self.linie_1_x2
        self.linie_3_y1 = positionDaten[3]

        self.objectNr = self.main_window_frame.zeichenwand.create_line((self.x,
                                                                        self.y,
                                                                        self.linie_1_x2,
                                                                        self.linie_1_y2), width=1, fill="Black")
        self.objectNr2 = self.main_window_frame.zeichenwand.create_line((self.linie_2_x1,
                                                                        self.linie_2_y1,
                                                                        self.linie_2_x2,
                                                                        self.linie_2_y2), width=1, fill="Black")
        self.objectNr3 = self.main_window_frame.zeichenwand.create_line((self.linie_3_x1,
                                                                        self.linie_3_y1,
                                                                        self.x2,
                                                                        self.y2), width=1, fill="Black")
        
        return {'objectNr': self.objectNr, 'lineNr': lineNummer, 
                'objectNr2': self.objectNr2,
                'objectNr3': self.objectNr3,
                'x': self.x,'y': self.y, 'x2': self.x2, 'y2': self.y2,
                'l1_x2': self.linie_1_x2,'l1_y2': self.linie_1_y2, 
                'l2_x1': self.linie_2_x1, 'l2_y1': self.linie_2_x1,
                'l2_x2': self.linie_2_x2, 'l2_y2': self.linie_2_x2,
                'l3_x1': self.linie_3_x1, 'l3_y1': self.linie_3_x1,
                'start': positionDaten[4], 'ziel': positionDaten[5], 'zielIn': positionDaten[6]}

    def erzeuge_ton(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # überpfüfen ob Timer On Nummer schon vorhanden
        timerFound = True
        self.aktuelleTonNr = 0
        while timerFound:
            self.aktuelleTonNr = self.aktuelleTonNr + 1
            typ = 'TON' + str(self.aktuelleTonNr)
            timerFound = False
            if blocks:
                for block in blocks:
                    if 'timerNr' in block:
                        if block['timerNr'] == typ:
                            timerFound = True
                            continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        parameter1 = 0

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_timer(blockNr, x, y, typ, parameter1)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_tof(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # überpfüfen ob Timer On Nummer schon vorhanden
        timerFound = True
        self.aktuelleTofNr = 0
        while timerFound:
            self.aktuelleTofNr = self.aktuelleTofNr + 1
            typ = 'TOF' + str(self.aktuelleTofNr)
            timerFound = False
            if blocks:
                for block in blocks:
                    if 'timerNr' in block:
                        if block['timerNr'] == typ:
                            timerFound = True
                            continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        parameter1 = 0

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_timer(blockNr, x, y, typ, parameter1)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_cud(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # überpfüfen ob counter Nummer schon vorhanden
        counterFound = True
        self.aktuelleCudNr = 0
        while counterFound:
            self.aktuelleCudNr = self.aktuelleCudNr + 1
            typ = 'CUD' + str(self.aktuelleCudNr)
            counterFound = False
            if blocks:
                for block in blocks:
                    if 'cudNr' in block:
                        if block['cudNr'] == typ:
                            counterFound = True
                            continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        parameter1 = 0
        parameter2 = 0

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_cud_erzeugen(blockNr, x, y, typ, parameter1, parameter2)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_sr(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # überpfüfen ob Timer On Nummer schon vorhanden
        srFound = True
        self.aktuelleSrNr = 0
        while srFound:
            self.aktuelleSrNr = self.aktuelleSrNr + 1
            typ = 'SR' + str(self.aktuelleSrNr)
            srFound = False
            if blocks:
                for block in blocks:
                    if 'srNr' in block:
                        if block['srNr'] == typ:
                            srFound = True
                            continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_sr_rs(blockNr, x, y, typ)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_and_2(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = '&'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_and_2(blockNr, x, y, typ)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

        # Prgrammänderung
        self.programChange = True
    
    def erzeuge_lt(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = '<I'
        parameter1 = '0'
        parameter2 = '0'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_compare_erzeugen(blockNr, x, y, typ, parameter1, parameter2)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_lit(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = '<=I'
        parameter1 = '0'
        parameter2 = '0'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_compare_erzeugen(blockNr, x, y, typ, parameter1, parameter2)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_gt(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = '>I'
        parameter1 = '0'
        parameter2 = '0'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_compare_erzeugen(blockNr, x, y, typ, parameter1, parameter2)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True
    
    def erzeuge_git(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = '>=I'
        parameter1 = '0'
        parameter2 = '0'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_compare_erzeugen(blockNr, x, y, typ, parameter1, parameter2)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_it(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = '==I'
        parameter1 = '0'
        parameter2 = '0'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_compare_erzeugen(blockNr, x, y, typ, parameter1, parameter2)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True
    
    def erzeuge_nit(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = '!=I'
        parameter1 = '0'
        parameter2 = '0'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_compare_erzeugen(blockNr, x, y, typ, parameter1, parameter2)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_add(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = 'ADD'
        parameter1 = 0
        parameter2 = 0
        parameter3 = 0

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_aritmetic_erzeugen(blockNr, x, y, typ, parameter1, parameter2, parameter3)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_sub(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = 'SUB'
        parameter1 = 0
        parameter2 = 0
        parameter3 = 0

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_aritmetic_erzeugen(blockNr, x, y, typ, parameter1, parameter2, parameter3)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True
    
    def erzeuge_mul(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = 'MUL'
        parameter1 = 0
        parameter2 = 0
        parameter3 = 0

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_aritmetic_erzeugen(blockNr, x, y, typ, parameter1, parameter2, parameter3)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_div(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = 'DIV'
        parameter1 = 0
        parameter2 = 0
        parameter3 = 0

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_aritmetic_erzeugen(blockNr, x, y, typ, parameter1, parameter2, parameter3)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_move(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        parameter1 = '0'
        parameter2 = '0'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_move_erzeugen(blockNr, x, y, parameter1, parameter2)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_comm(self):
        global comments, blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # zuerst einen Block wählen
        if not blocks:
            tkinter.messagebox.showerror('Comment', 'first you use a block')
            return

        # überpfüfen ob Kommentar Nummer schon vorhanden
        commentFound = True
        self.aktuelleCommentNr = 0
        while commentFound:
            self.aktuelleCommentNr = self.aktuelleCommentNr + 1
            commentNr = 'C' + str(self.aktuelleCommentNr)
            commentFound = False
            if comments:
                for comment in comments:
                    if comment['commentNr'] == commentNr:
                        commentFound = True
                        continue

        # 199 comments begrenzt
        if self.aktuelleCommentNr >= 199:
            tkinter.messagebox.showerror('Comment', ' max comennt achieved')
            return
        
        # position für erzeugen
        x = 100
        y = 100
        parameter1 = 'Text'

        # in aktuelle Kommentar in Seite speichern
        self.page_daten(commentNr)

        comment = self.block_comment_erzeugen(commentNr, x, y, parameter1)
        comments.append(comment)

    def erzeuge_inv(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = 'INV'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_inv_erzeugen(blockNr, x, y, typ)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_ip(self):
        global blocks, blockPositionFokus, ip

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue
        
        # überpfüfen ob Timer On Nummer schon vorhanden
        ipFound = True
        self.aktuelleIpNr = 0
        while ipFound:
            self.aktuelleIpNr = self.aktuelleIpNr + 1
            typ = 'IP' + str(self.aktuelleIpNr)
            ipFound = False
            if blocks:
                for block in blocks:
                    if 'ipNr' in block:
                        if block['ipNr'] == typ:
                            ipFound = True
                            continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_ip_erzeugen(blockNr, x, y, typ)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_and_3(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = '&'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_and_3(blockNr, x, y, typ)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_or_2(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = '>I'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_and_2(blockNr, x, y, typ)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def erzeuge_or_3(self):
        global blocks, blockPositionFokus

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # aktuell BlockNr ausgang in Eingeng schreiebn
        x = 100
        y = 100
        typ = '>I'

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_and_3(blockNr, x, y, typ)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def zeichne_line(self):
        global lines, blocks
        
        # überpfüfen ob Linie Nummer schon vorhanden
        lineFound = True
        while lineFound:
            self.aktuelleLineNr = self.aktuelleLineNr + 1
            lineNr = 'L' + str(self.aktuelleLineNr)
            lineFound = False
            if lines:
                for line in lines:
                    if line['lineNr'] == lineNr:
                        lineFound = True
                        continue
        
        # in aktuelle Linie in Seite speichern
        self.page_daten(lineNr)

        line = self.line(lineNr, self.liniePos)
        lines.append(line)
        
        # quelle und Ziel in Block eintragen     
            # self.liniePos[0] -> line x
            # self.liniePos[1] -> line y
            # self.liniePos[2] -> line x2
            # self.liniePos[3] -> line y2
            # self.liniePos[4] -> start BlockNr
            # self.liniePos[5] -> ziel BlockNr
            # self.liniePos[6] -> ziel input nr ('in1'- 'in3')
        for block in blocks:
            # in Quellblock Ziel eintragen
            if block['blockNr'] == self.liniePos[4]:
                block['out1'] = self.liniePos[5] + '-' + self.liniePos[6] 
            # in Zielblock Quelle eintragen          
            if block['blockNr'] == self.liniePos[5]:
                if 'in1' == self.liniePos[6]:
                    block['in1'] = self.liniePos[4]
                if 'in2' == self.liniePos[6]:
                    block['in2'] = self.liniePos[4]
                if 'in3' == self.liniePos[6]:
                    block['in3'] = self.liniePos[4]
        
        # Prgrammänderung
        self.programChange = True

    def zeichne_line_von_online(self, blockNr, zielBlockNr, zielBlockInput):
        global lines, blocks
        self.aktuelleLineNr = self.aktuelleLineNr + 1
        lineNr = 'L' + str(self.aktuelleLineNr)

        # quelle und Ziel in Block eintragen     
            # self.liniePos[0] -> line x
            # self.liniePos[1] -> line y
            # self.liniePos[2] -> line x2
            # self.liniePos[3] -> line y2
            # self.liniePos[4] -> start BlockNr
            # self.liniePos[5] -> ziel BlockNr
            # self.liniePos[6] -> ziel input nr ('in1'- 'in3')
        for block in blocks:
            # self.liniePos[0] -> line x
            if block['blockNr'] == blockNr:
                self.liniePos[0] = block['outX1']
                self.liniePos[1] = block['outY1']
            if block['blockNr'] == zielBlockNr:
                if zielBlockInput == 'in1':
                    self.liniePos[2] = block['inX1']
                    self.liniePos[3] = block['inY1']
                if zielBlockInput == 'in2':
                    self.liniePos[2] = block['inX2']
                    self.liniePos[3] = block['inY2']
                if zielBlockInput == 'in3':
                    self.liniePos[2] = block['inX3']
                    self.liniePos[3] = block['inY3']
        self.liniePos[4] = blockNr
        self.liniePos[5] = zielBlockNr      
        self.liniePos[6] = zielBlockInput

        for block in blocks:
            # in Quellblock Ziel eintragen
            if block['blockNr'] == self.liniePos[4]:
                block['out1'] = self.liniePos[5] + '-' + self.liniePos[6] 

        # zeichne Linie
        line = self.line(lineNr, self.liniePos)
        lines.append(line)

    def achseAuf(self):
        pass

    def laden_programm(self):
        global sd2, blocks, letzterBlockNr
        daten = sd2.pop(0)
        for key, value in daten.items():
            if value == 'ZUW':
                block = self.block_zuweisung_erzeugen(key, daten['OUT'])
                blocks.append(block)

            if value == 'INPUT':
                if 'IN1' in daten:             
                    block = self.block_input_erzeugen(key, daten['IN1'])
                    blocks.append(block)

                # linie zeichnen
                ziel = daten['OUT'].split('-')
                zielBlockNr = ziel[0]
                zielBlockInput = ziel[1]
                if zielBlockInput == 'I1':
                    zielBlockInput = 'in1'
                if zielBlockInput == 'I2':
                    zielBlockInput = 'in2'
                if zielBlockInput == 'I3':
                    zielBlockInput = 'in3'
                self.zeichne_line_von_online(key, zielBlockNr, zielBlockInput)

            if value == 'OR':
                if 'IN3' in daten:             
                    block = self.block_and_3(key, self.lPx, self.lPy, '>I')
                    blocks.append(block)
                else:
                    block = self.block_and_2(key, self.lPx, self.lPy, '>I')
                    blocks.append(block)

                # linie zeichnen
                ziel = daten['OUT'].split('-')
                zielBlockNr = ziel[0]
                zielBlockInput = ziel[1]
                if zielBlockInput == 'I1':
                    zielBlockInput = 'in1'
                if zielBlockInput == 'I2':
                    zielBlockInput = 'in2'
                if zielBlockInput == 'I3':
                    zielBlockInput = 'in3'
                self.zeichne_line_von_online(key, zielBlockNr, zielBlockInput)

            if value == 'AND':
                if 'IN3' in daten:              
                    block = self.block_and_3(key, self.lPx, self.lPy, '&')
                    blocks.append(block)
                else:
                    block = self.block_and_2(key, self.lPx, self.lPy, '&')
                    blocks.append(block)

                # linie zeichnen
                ziel = daten['OUT'].split('-')
                zielBlockNr = ziel[0]
                zielBlockInput = ziel[1]
                if zielBlockInput == 'I1':
                    zielBlockInput = 'in1'
                if zielBlockInput == 'I2':
                    zielBlockInput = 'in2'
                if zielBlockInput == 'I3':
                    zielBlockInput = 'in3'
                self.zeichne_line_von_online(key, zielBlockNr, zielBlockInput)

            #letzter Block Nr der gezeichnet worden ist
            self.lPx += 10
            self.lPy += 10
            letzterBlockNr = key
       
    def zuweisung(self):
        global blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        # überpfüfen ob Output Nummer schon vorhanden
        outFound = True
        self.aktuelleOutputNr = 0
        while outFound:
            self.aktuelleOutputNr = self.aktuelleOutputNr + 1
            typ = 'Q' + str(self.aktuelleOutputNr)
            outFound = False
            if blocks:
                for block in blocks:
                    if 'OUT' in block:
                        if block['OUT'] == typ:
                            outFound = True
                            continue
        
        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_zuweisung_erzeugen(blockNr, typ)
        blocks.append(block)
        #print(len(blocks))

        # Prgrammänderung
        self.programChange = True

    def input(self):
        global blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # überpfüfen ob Block Nummer schon vorhanden
        blockFound = True
        self.aktuelleBlockNr = 0
        while blockFound:
            self.aktuelleBlockNr = self.aktuelleBlockNr + 1
            blockNr = 'B' + str(self.aktuelleBlockNr)
            blockFound = False
            if blocks:
                for block in blocks:
                    if block['blockNr'] == blockNr:
                        blockFound = True
                        continue

        #self.aktuelleInputNr = self.aktuelleInputNr + 1
        #typ = 'I' + str(self.aktuelleInputNr)

        # überpfüfen ob input Nummer schon vorhanden
        inFound = True
        self.aktuelleInputNr = 0
        while inFound:
            self.aktuelleInputNr = self.aktuelleInputNr + 1
            typ = 'I' + str(self.aktuelleInputNr)
            inFound = False
            if blocks:
                for block in blocks:
                    if 'in1' in block:
                        if block['in1'] == typ:
                            inFound = True
                            continue

        # in aktuelle Seite speichern
        self.page_daten(blockNr)

        block = self.block_input_erzeugen(blockNr, typ)
        blocks.append(block)

        # Prgrammänderung
        self.programChange = True

    def page_daten(self, daten):
        global pageFokus, page1, page2, page3, page4, page5, page6

        if pageFokus == 0:
            page1.append(daten)
        if pageFokus == 1:
            page2.append(daten)
        if pageFokus == 2:
            page3.append(daten)
        if pageFokus == 3:
            page4.append(daten)
        if pageFokus == 4:
            page5.append(daten)
        if pageFokus == 5:
            page6.append(daten)

    def zeichnen_aktuelle_page1(self):
        global page1
        self.zeichnen_aktuelle_page_block(page1)

    def zeichnen_aktuelle_page2(self):
        global page2
        self.zeichnen_aktuelle_page_block(page2)

    def zeichnen_aktuelle_page3(self):
        global page3
        self.zeichnen_aktuelle_page_block(page3)

    def zeichnen_aktuelle_page4(self):
        global page4
        self.zeichnen_aktuelle_page_block(page4)

    def zeichnen_aktuelle_page5(self):
        global page5
        self.zeichnen_aktuelle_page_block(page5)
    
    def zeichnen_aktuelle_page6(self):
        global page6
        self.zeichnen_aktuelle_page_block(page6)
    
    def zeichnen_aktuelle_page_block(self, page):
        global blocks, lines, comments
        blocksCopy = copy.deepcopy(blocks)
        linesCopy = copy.deepcopy(lines)
        commentsCopy = copy.deepcopy(comments)
        pageCopy = copy.deepcopy(page)

        # aktuell objekte anzeigen
        #https://stackoverflow.com/questions/53499669/how-to-hide-and-show-canvas-items-on-tkinter
        while pageCopy:
            aktuellePageBlock = pageCopy.pop()  
            for block in blocks:
                if block['blockNr'] == aktuellePageBlock:
                    blocksCopy.remove(block)
                    if 'objectNrInput1' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrInput1'], state='normal')
                    if 'objectNrInput2' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrInput2'], state='normal')
                    if 'objectNrInput3' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrInput3'], state='normal')
                    if 'objectNrOutput' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrOutput'], state='normal')
                    if 'objectNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNr'], state='normal')
                    if 'objectNrTextBlockNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrTextBlockNr'], state='normal')
                    if 'objectNrTextBlockTyp' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrTextBlockTyp'], state='normal')
                    if 'objectTextTimerNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextTimerNr'], state='normal')
                    if 'objectParameterSet' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameterSet'], state='normal')
                    if 'objectParameterActual' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameterActual'], state='normal')
                    if 'objectTextSet' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextSet'], state='normal')
                    if 'objectTextReset' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextReset'], state='normal')
                    if 'objectTextIpNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextIpNr'], state='normal')
                    if 'objectTextCounterNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextCounterNr'], state='normal')
                    if 'objectParameterPreset' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameterPreset'], state='normal')
                    if 'objectTextUp' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextUp'], state='normal')
                    if 'objectTextDown' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextDown'], state='normal')
                    if 'objectParameter1' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter1'], state='normal')
                    if 'objectParameter2' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter2'], state='normal')
                    if 'objectParameter3' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter3'], state='normal')
                    if 'objectParameter1actual' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter1actual'], state='normal')
                    if 'objectParameter2actual' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter2actual'], state='normal')
                    if 'objectParameter3actual' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter3actual'], state='normal')

            # lines zeichnen
            for line in lines:
                if line['lineNr'] == aktuellePageBlock:
                    if 'objectNr' in line:
                        linesCopy.remove(line)
                        self.main_window_frame.zeichenwand.itemconfigure(line['objectNr'], state='normal')
                        self.main_window_frame.zeichenwand.itemconfigure(line['objectNr2'], state='normal')
                        self.main_window_frame.zeichenwand.itemconfigure(line['objectNr3'], state='normal')

            # Kommentar zeichnen
            for comment in comments:
                if comment['commentNr'] == aktuellePageBlock:
                    commentsCopy.remove(comment)
                    if 'objectNr' in comment:      
                        self.main_window_frame.zeichenwand.itemconfigure(comment['objectNr'], state='normal')
                    if 'objectNrTextBlockNr' in comment:      
                        self.main_window_frame.zeichenwand.itemconfigure(comment['objectNrTextBlockNr'], state='normal')
                    if 'objectParameter1' in comment:      
                        self.main_window_frame.zeichenwand.itemconfigure(comment['objectParameter1'], state='normal')

        # Block verstecken
        while blocksCopy:
            aktuelleBlock = blocksCopy.pop() 
            for block in blocks:
                if block['blockNr'] == aktuelleBlock['blockNr']:
                    if 'objectNrInput1' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrInput1'], state='hidden')
                    if 'objectNrInput2' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrInput2'], state='hidden')
                    if 'objectNrInput3' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrInput3'], state='hidden')
                    if 'objectNrOutput' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrOutput'], state='hidden')
                    if 'objectNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNr'], state='hidden')
                    if 'objectNrTextBlockNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrTextBlockNr'], state='hidden')
                    if 'objectNrTextBlockTyp' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectNrTextBlockTyp'], state='hidden')
                    if 'objectTextTimerNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextTimerNr'], state='hidden')
                    if 'objectParameterSet' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameterSet'], state='hidden')
                    if 'objectParameterActual' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameterActual'], state='hidden')
                    if 'objectTextSet' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextSet'], state='hidden')
                    if 'objectTextReset' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextReset'], state='hidden')
                    if 'objectTextIpNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextIpNr'], state='hidden')
                    if 'objectTextCounterNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextCounterNr'], state='hidden')
                    if 'objectParameterPreset' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameterPreset'], state='hidden')
                    if 'objectTextUp' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextUp'], state='hidden')
                    if 'objectTextDown' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectTextDown'], state='hidden')
                    if 'objectParameter1' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter1'], state='hidden')
                    if 'objectParameter2' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter2'], state='hidden')
                    if 'objectParameter3' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter3'], state='hidden')
                    if 'objectParameter1actual' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter1actual'], state='hidden')
                    if 'objectParameter2actual' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter2actual'], state='hidden')
                    if 'objectParameter3actual' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(block['objectParameter3actual'], state='hidden')

        # Linen verstecken
        while linesCopy:
            aktuelleLinie = linesCopy.pop() 
            for line in lines:
                if line['lineNr'] == aktuelleLinie['lineNr']:
                    if 'objectNr' in block:
                        self.main_window_frame.zeichenwand.itemconfigure(line['objectNr'], state='hidden')
                        self.main_window_frame.zeichenwand.itemconfigure(line['objectNr2'], state='hidden')
                        self.main_window_frame.zeichenwand.itemconfigure(line['objectNr3'], state='hidden')

        # Kommentar verstecken
        while commentsCopy:
            aktuelleComment = commentsCopy.pop() 
            for comment in comments:
                if comment['commentNr'] == aktuelleComment['commentNr']:
                    if 'objectNr' in comment:      
                        self.main_window_frame.zeichenwand.itemconfigure(comment['objectNr'], state='hidden')
                    if 'objectNrTextBlockNr' in comment:      
                        self.main_window_frame.zeichenwand.itemconfigure(comment['objectNrTextBlockNr'], state='hidden')
                    if 'objectParameter1' in comment:      
                        self.main_window_frame.zeichenwand.itemconfigure(comment['objectParameter1'], state='hidden')

    def load_max_fbd(self):
        global blocks
        maxFbd = {}

        # blocks anzahl
        maxBlock = 0
        for block in blocks:
            if 'blockNr' in block:
                blockNr = block['blockNr']
                nr = int(blockNr[1:])
                if nr > maxBlock:
                    maxBlock = nr
                    self.aktuelleBlockNr = maxBlock          
        item = {'maxBlock': self.aktuelleBlockNr}
        maxFbd.update(item)

        # input anzahl
        maxInput = 0
        for block in blocks:
            if 'typ' in block:
                typ = block['typ']
                if typ == 'INPUT':
                    in1 = block['in1']
                    if in1[0] == 'I':
                        nr = int(in1[1:])
                        if nr > maxInput:
                            maxInput = nr
                            self.aktuelleInputNr = maxInput 
        item = {'maxInput': self.aktuelleInputNr}
        maxFbd.update(item)

        # output anzahl
        maxOutput = 0
        for block in blocks:
            if 'typ' in block:
                typ = block['typ']
                if typ == 'ZUW':
                    out = block['OUT']
                    if out[0] == 'Q':
                        nr = int(out[1:])
                        if nr > maxOutput:
                            maxOutput = nr
                            self.aktuelleOutputNr = maxOutput
        item = {'maxOutput': self.aktuelleOutputNr}
        maxFbd.update(item)

        # timer on anzahl
        maxTon = 0
        for block in blocks:
            if 'typ' in block:
                typ = block['typ']
                if typ == 'TON':
                    timerNr = block['timerNr']
                    if timerNr[:3] == 'TON':
                        nr = int(timerNr[3:])
                        if nr > maxTon:
                            maxTon = nr
                            self.aktuelleTonNr = maxTon
        item = {'maxTon': self.aktuelleTonNr}
        maxFbd.update(item)

        # timer of anzahl
        maxTof = 0
        for block in blocks:
            if 'typ' in block:
                typ = block['typ']
                if typ == 'TOF':
                    timerNr = block['timerNr']
                    if timerNr[:3] == 'TOF':
                        nr = int(timerNr[3:])
                        if nr > maxTof:
                            maxTof = nr
                            self.aktuelleTofNr = maxTof
        item = {'maxTof': self.aktuelleTofNr}
        maxFbd.update(item)

        # Set Reset FlipFlop anzahl
        maxSr = 0
        for block in blocks:
            if 'typ' in block:
                typ = block['typ']
                if typ == 'SR':
                    srNr = block['srNr']
                    if srNr[:2] == 'SR':
                        nr = int(srNr[2:])
                        if nr > maxSr:
                            maxSr = nr
                            self.aktuelleSrNr = maxSr
        item = {'maxSr': self.aktuelleSrNr}
        maxFbd.update(item)

        # impul posive anzahl
        maxIp = 0
        for block in blocks:
            if 'typ' in block:
                typ = block['typ']
                if typ == 'IP':
                    ipNr = block['ipNr']
                    if ipNr[:2] == 'IP':
                        nr = int(ipNr[2:])
                        if nr > maxIp:
                            maxIp = nr
                            self.aktuelleIpNr = maxIp
        item = {'maxIp': self.aktuelleIpNr}
        maxFbd.update(item)

        # counter up down anzahl
        maxCud = 0
        for block in blocks:
            if 'typ' in block:
                typ = block['typ']
                if typ == 'CUD':
                    cudNr = block['cudNr']
                    if cudNr[:3] == 'CUD':
                        nr = int(cudNr[3:])
                        if nr > maxCud:
                            maxCud = nr
                            self.aktuelleCudNr = maxCud
        item = {'maxCud': self.aktuelleCudNr}
        maxFbd.update(item)

        # merker word anzahl
        maxMw = 0
        for block in blocks:
            if 'in1' in block:
                in1 = block['in1']
                if isinstance(in1, str):
                    if 'MW' in in1:
                        nr = int(in1[2:])
                        if nr > maxMw:
                                maxMw = nr
            if 'in2' in block:
                in2 = block['in2']
                if isinstance(in2, str):
                    if 'MW' in in2:
                        nr = int(in2[2:])
                        if nr > maxMw:
                                maxMw = nr
            if 'in3' in block:
                in3 = block['in3']
                if isinstance(in3, str):
                    if 'MW' in in3:
                        nr = int(in3[2:])
                        if nr > maxMw:
                                maxMw = nr
            if 'out1' in block:
                out1 = block['out1']
                if 'MW' in out1:
                    nr = int(out1[2:])
                    if nr > maxMw:
                            maxMw = nr
        item = {'maxMw': maxMw}
        maxFbd.update(item)

        return maxFbd

    def sxor(self, s1, s2):
        #https://stackoverflow-com.translate.goog/questions/2612720/how-to-do-bitwise-exclusive-or-of-two-strings-in-python?    
        # convert strings to a list of character pair tuples
        # go through each tuple, converting them to ASCII code (ord)
        # perform exclusive or on the ASCII code
        # then convert the result back to ASCII (chr)
        # merge the resulting array of characters as a string
        return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

    def encrypt(self, text, pw):
        textListe = list(text)
        pwListShort = list(pw)
        encListe = []

        textLen = int(len(textListe) / len(pwListShort) + 1)

        password = ''
        for a in range(1, textLen+ 1):
            password += pw
        pwListe = list(password)
            
        while textListe:
            char = textListe.pop(0)
            pwChar = pwListe.pop(0)
            encChar = self.sxor(char, pwChar)
            encListe.append(encChar)

        enc = ''.join(encListe)
        return enc

    def decrypt(self, text, pw):
        textListe = list(text)
        pwListShort = list(pw)
        encListe = []
        
        textLen = int(len(textListe) / len(pwListShort) + 1)

        password = ''
        for a in range(1, textLen+ 1):
            password += pw
        pwListe = list(password)
        
        while textListe:
            char = textListe.pop(0)
            pwChar = pwListe.pop(0)
            encChar = self.sxor(char, pwChar)
            encListe.append(encChar)

        enc = ''.join(encListe)
        return enc

    def simulator_varibalen(self, config):
        global input, output, block, mw, ip, sr, cud, tof, ton

        input = {}
        for nummer in range(1, config['maxInput'] + 1):
            item = {('I' + str(nummer)): '0'}
            input.update(item)
        
        output = {}
        for nummer in range(1, config['maxOutput'] + 1):
            item = {('Q' + str(nummer)): '0'}
            output.update(item)

        block = {}
        for nummer in range(1, config['maxBlock'] + 1):
            item = {('B' + str(nummer)): '0'}
            block.update(item)

        mw = {}
        for nummer in range(1, config['maxMw'] + 1):
            item = {('MW' + str(nummer)): 0}
            mw.update(item)

        ip = {}
        for nummer in range(1, config['maxIp'] + 1):
            item = {('IP' + str(nummer)): '0'}
            ip.update(item)
        
        sr = {}
        for nummer in range(1, config['maxSr'] + 1):
            item = {('SR' + str(nummer)): '0'}
            sr.update(item)

        countTyp = {'presetValue': 0, 'setValue': 0, 'actualValue': 0,
            'countUpFlanke': '0', 'countDownFlanke': '0', 'init': '0'}
        cud = {}
        item = {}
        for numberCud in range(1, config['maxCud'] + 1):
            item[('CUD'+ str(numberCud))] = {}
            item[('CUD'+ str(numberCud))] = dict(countTyp)
            cud.update(item)
        
        tofTyp = {'in1': '', 'paramter': '', 'startTime': 0, 'actualTime': 0, 'setTime': 0, 'isWork': '0'}
        tof = {}
        item = {}
        for numberTof in range(1, config['maxTof'] + 1):
            item[('TOF'+ str(numberTof))] = {}
            item[('TOF'+ str(numberTof))] = dict(tofTyp)
            tof.update(item)
        
        tonTyp = {'in1': '', 'paramter': '', 'startTime': 0, 'actualTime': 0, 'setTime': 0, 'isWork': '0'}
        ton = {}
        item = {}
        for number in range(1, config['maxTon'] + 1):
            item[('TON'+ str(number))] = {}
            item[('TON'+ str(number))] = dict(tonTyp)
            ton.update(item)

    def sortList(self, blockListe):
        global page1, page2, page3, page4, page5, page6

        listePage1 = []
        listePage2 = []
        listePage3 = []
        listePage4 = []
        listePage5 = []
        listePage6 = []
        sortBlock =[]

        if page1:
            for item in page1:
                for block in blockListe:
                    if block['blockNr'] == item:
                        listePage1.append(block)      
            # sortiren
            sortListePage1_x  = sorted(listePage1, key=lambda d: d['x']) 
            #sortListePage1_y  = sorted(listePage1, key=lambda d: d['y']) 
            sortListePage1_x.reverse()

        if page2:
            for item in page2:
                for block in blockListe:
                    if block['blockNr'] == item:
                        listePage2.append(block)      
            # sortiren
            sortListePage2_x  = sorted(listePage2, key=lambda d: d['x']) 
            #sortListePage1_y  = sorted(listePage1, key=lambda d: d['y']) 
            sortListePage2_x.reverse()

        if page3:
            for item in page3:
                for block in blockListe:
                    if block['blockNr'] == item:
                        listePage3.append(block)      
            # sortiren
            sortListePage3_x  = sorted(listePage3, key=lambda d: d['x']) 
            #sortListePage1_y  = sorted(listePage1, key=lambda d: d['y']) 
            sortListePage3_x.reverse()

        if page4:
            for item in page4:
                for block in blockListe:
                    if block['blockNr'] == item:
                        listePage4.append(block)      
            # sortiren
            sortListePage4_x  = sorted(listePage4, key=lambda d: d['x']) 
            #sortListePage1_y  = sorted(listePage1, key=lambda d: d['y']) 
            sortListePage4_x.reverse()
        
        if page5:
            for item in page5:
                for block in blockListe:
                    if block['blockNr'] == item:
                        listePage5.append(block)      
            # sortiren
            sortListePage5_x  = sorted(listePage5, key=lambda d: d['x']) 
            #sortListePage1_y  = sorted(listePage1, key=lambda d: d['y']) 
            sortListePage5_x.reverse()

        if page6:
            for item in page6:
                for block in blockListe:
                    if block['blockNr'] == item:
                        listePage6.append(block)      
            # sortiren
            sortListePage6_x  = sorted(listePage6, key=lambda d: d['x']) 
            #sortListePage1_y  = sorted(listePage1, key=lambda d: d['y']) 
            sortListePage6_x.reverse()

        if page6:
            sortBlock += sortListePage6_x
        if page5:
            sortBlock += sortListePage5_x
        if page4:
            sortBlock += sortListePage4_x
        if page3:
            sortBlock += sortListePage3_x
        if page2:
            sortBlock += sortListePage2_x
        if page1:
            sortBlock += sortListePage1_x

        return sortBlock

    def compelieren2(self):
        global blocks, sd

        saveList = []
        # Programm
        #sd = compelier(blocks)
        sd = compelier(self.sortList(blocks))

        # config max 
        config = self.load_max_fbd()

        # zur einerListe
        saveList.append(config)
        saveList.append(sd)

        # ohne encrypt
        # blockprogramm speichern
        #with open('blockprogramm.json', 'w') as fp:
            #json.dump(saveList, fp)

        # mit encrypt
        password = 'welt'
        text = json.dumps(saveList)
        encText = self.encrypt(text, password)
        with open('plc_blockprogram.plc', 'w') as fp:
            json.dump(encText, fp)

        # variablen für Simulation generieren
        self.simulator_varibalen(config)

        # Prgrammänderung
        self.programChange = False

    def compelieren(self):
        global blocks, lines, blocksQuelle, blockProgram, sd
        blocksQuelle = copy.deepcopy(blocks)
        speicher =[]
        for block in blocksQuelle:
            if 'typ' in block:
                if block['typ'] == 'ZUW':
                    blockP ={block['blockNr']:block['typ'], 'OUT':block['OUT'], 'IN1': block['in1']}
                    blockProgram.append(blockP)
                    blocksQuelle.remove(block)

        zuweisung = blockProgram[0]
        for block in blocksQuelle:
            if zuweisung['IN1'] == block['blockNr']:
                bNr = ''
                for key, value in zuweisung.items():
                    if value == 'ZUW':
                        bNr = key
                out = bNr + '-' + 'I1'
                if 'in1' in block:
                    blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1']}
                if 'in2' in block:
                    blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1'], 'IN2': block['in2']}
                if 'in3' in block:
                    blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1'], 'IN2': block['in2'], 'IN3': block['in3']}
                if block['typ'] == 'INPUT':
                    blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1']}
                blockProgram.append(blockP)
                blocksQuelle.remove(block)
        
        if blockProgram[1]:
            block_1 = blockProgram[1]
            if 'IN3' in block_1:
                for block in blocksQuelle:
                    if block['blockNr'] == block_1['IN3']:
                        for key, value in block_1.items():
                            if value == 'OR' or value == 'AND':
                                bNr = key
                        out = bNr + '-' + 'I3'
                    if 'in1' in block:
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1']}
                    if 'in2' in block:
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1'], 'IN2': block['in2']}
                    if 'in3' in block:
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1'], 'IN2': block['in2'], 'IN3': block['in3']}
                    if block['typ'] == 'INPUT':
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1']}
                    blockProgram.append(blockP)
                    blocksQuelle.remove(block)
            if 'IN2' in block_1:
                for block in blocksQuelle:
                    if block['blockNr'] == block_1['IN2']:
                        for key, value in block_1.items():
                            if value == 'OR' or value == 'AND':
                                bNr = key
                        out = bNr + '-' + 'I2'
                    if 'in1' in block:
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1']}
                    if 'in2' in block:
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1'], 'IN2': block['in2']}
                    if 'in3' in block:
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1'], 'IN2': block['in2'], 'IN3': block['in3']}
                    if block['typ'] == 'INPUT':
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1']}
                    blockProgram.append(blockP)
                    blocksQuelle.remove(block)
            if 'IN1' in block_1:
                for block in blocksQuelle:
                    if block['blockNr'] == block_1['IN1']:
                        for key, value in block_1.items():
                            if value == 'OR' or value == 'AND':
                                bNr = key
                        out = bNr + '-' + 'I2'
                    if 'in1' in block:
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1']}
                    if 'in2' in block:
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1'], 'IN2': block['in2']}
                    if 'in3' in block:
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1'], 'IN2': block['in2'], 'IN3': block['in3']}
                    if block['typ'] == 'INPUT':
                        blockP ={block['blockNr']:block['typ'], 'OUT':out, 'IN1': block['in1']}
                    blockProgram.append(blockP)
                    blocksQuelle.remove(block)
                    
        #print(sprung)
        sd = blockProgram
        print(blockProgram)

    def block_and(self, blockNr, daten):
        global block
        l_add= []
        for key in daten:
            if key[:1] == 'B':
                #print(key)
                #global block
                value = block[key]
            if key[:1] == 'I':
                #print(key)
                #global input
                value = input[key]
            # neu 1.11.21
            if not key:
                value = '0'
            l_add.append(value)

        result = l_add.count('1')

        if result == len(l_add):
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}

    def block_or(self, blockNr, daten):
        global block
        l_add= []
        for key in daten:
            if key[:1] == 'B':
                #print(key)
                #global block
                value = block[key]
            if key[:1] == 'I':
                #print(key)
                #global input
                value = input[key]
            # neu 1.11.21
            if not key:
                value = '0'
            l_add.append(value)

        result = l_add.count('1')

        if result > 0:
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}

    def block_compare(self, blockNr ,daten, art):
        global block, cud, ton, tof, mw
        in1 = 0
        in2 = 0
        
        # IN1 daten[0]
        strIn1 = str(daten[0])
        if strIn1.isdigit():
            in1 = int(daten[0])
        else:
            if 'MW' in daten[0]:     
                in1 = mw[daten[0]]
            if 'CUD' in daten[0]:     
                in1 = cud[daten[0]]['actualValue']
            if 'TON' in daten[0]:     
                in1 = ton[daten[0]]['actualTime']
            if 'TOF' in daten[0]:     
                in1 = tof[daten[0]]['actualTime']
        
        # IN2 daten[1]
        strIn2 = str(daten[1])
        if strIn2.isdigit():
            in2 = int(daten[1])
        else:
            if 'MW' in daten[1]:     
                in2 = mw[daten[1]]
            if 'CUD' in daten[1]:
                in2 = cud[daten[1]]['actualValue']
            if 'TON' in daten[1]:     
                in2 = ton[daten[1]]['actualTime']
            if 'TOF' in daten[1]:     
                in2 = tof[daten[1]]['actualTime']
        
        # Ausgang
        if art == 'LT':
            if in1 < in2:
                return { blockNr: '1'}
            else:
                return { blockNr: '0'}
        if art == 'LIT':
            if in1 <= in2:
                return { blockNr: '1'}
            else:
                return { blockNr: '0'}
        if art == 'GT':
            if in1 > in2:
                return { blockNr: '1'}
            else:
                return { blockNr: '0'}
        if art == 'GIT':
            if in1 >= in2:
                return { blockNr: '1'}
            else:
                return { blockNr: '0'}
        if art == 'IT':
            if in1 == in2:
                return { blockNr: '1'}
            else:
                return { blockNr: '0'}
        if art == 'NIT':
            if in1 != in2:
                return { blockNr: '1'}
            else:
                return { blockNr: '0'}

    def block_aritmetic(self, blockNr, daten, art, out):
        global block, cud, ton, tof, mw
        in2 = 0
        in3 = 0
        value = ''
        # abfrage Eingang 1
        if daten[0]:
            if 'B' in daten[0]:
                value = block[daten[0]]
        
        if value == '0':
            return { blockNr: '0'}
            
        # IN2 daten[1]
        strIn2 = str(daten[1])
        if strIn2.isdigit():
            in2 = int(daten[1])
        else:
            if 'MW' in daten[1]:     
                in2 = mw[daten[1]]
            if 'CUD' in daten[1]:     
                in2 = cud[daten[1]]['actualValue']
            if 'TON' in daten[1]:     
                in2 = ton[daten[1]]['actualTime']
            if 'TOF' in daten[1]:     
                in2 = tof[daten[1]]['actualTime']
        
        # IN3 daten[2]
        strIn3 = str(daten[2])
        if strIn3.isdigit():
            in3 = int(daten[2])
        else:
            if 'MW' in daten[2]:     
                in3 = mw[daten[2]]
            if 'CUD' in daten[2]:
                in3 = cud[daten[2]]['actualValue']
            if 'TON' in daten[2]:     
                in3 = ton[daten[2]]['actualTime']
            if 'TOF' in daten[2]:     
                in3 = tof[daten[2]]['actualTime']
        
        # Ausgang
        if art == 'ADD':
            mw[out] = int(in2 + in3)
            return { blockNr: '1'}
        if art == 'SUB':
            mw[out] = int(in2 - in3)
            return { blockNr: '1'}
        if art == 'MUL':
            mw[out] = int(in2 * in3)
            return { blockNr: '1'}
        if art == 'DIV':
            # neu 1.11.21
            if in2 == 0 or in3 == 0:
                mw[out] = 0
                return { blockNr: '1'}
            mw[out] = int(in2 / in3)
            return { blockNr: '1'}

    def block_move(self, blockNr, daten, out):
        global block, cud, ton, tof, mw
        in2 = ''
        value = ''
        # abfrage Eingang 1
        if daten[0]:
            if 'B' in daten[0]:
                value = block[daten[0]]
        # neu 1.11.21
        if not daten[0]:
            value = '0'

        if value == '0':
            return { blockNr: '0'}
            
        # IN2 daten[1]
        strIn2 = str(daten[1])
        if strIn2.isdigit():
            in2 = int(daten[1])
        else:
            if 'MW' in daten[1]:     
                in2 = mw[daten[1]]
            if 'CUD' in daten[1]:     
                in2 = cud[daten[1]]['actualValue']
            if 'TON' in daten[1]:     
                in2 = ton[daten[1]]['actualTime']
            if 'TOF' in daten[1]:     
                in2 = tof[daten[1]]['actualTime']
        
        # Ausgang
        if 'MW' in out:
            mw[out] = int(in2)
            return { blockNr: '1'}
        if 'CUD' in out:
            cud[out]['setValue'] = int(in2)
            return { blockNr: '1'}
        if 'TON' in out:     
            ton[out]['paramter'] = int(in2)
            return { blockNr: '1'}
        if 'TOF' in out:     
            tof[out]['paramter'] = int(in2)
            return { blockNr: '1'}
        # neu 10.11.21 wenn keine Angebe
        return { blockNr: '0'}

    def block_ton(self, blockNr ,daten, tonNr, parameter1):
        global block, input, ton
        l_add= []
        tonEin = False
        for key in daten:
            if key[:1] == 'B':
                value = block[key]
            if key[:1] == 'I':
                value = input[key]
            # neu 1.11.21
            if not key:
                value = '0'
            l_add.append(value)

        result = l_add.count('1')

        if result == len(l_add):
            #return { blockNr: '1'}
            tonEin = True
        else:
            #return { blockNr: '0'}
            tonEin = False
        # init Wert vom plc proramm kann dann überschrieben werden
        if not ton[tonNr]['paramter']:
            ton[tonNr]['paramter'] = parameter1
        ton[tonNr]['setTime'] = ton[tonNr]['paramter']

        if not tonEin and ton[tonNr]['isWork'] == '1':
            ton[tonNr]['isWork'] = '0'

        if tonEin and ton[tonNr]['isWork'] == '0':
            ton[tonNr]['actualTime']  = 0
            ton[tonNr]['startTime'] = int(1000 * time.perf_counter())
            ton[tonNr]['isWork'] = '1'

        if tonEin and ton[tonNr]['isWork'] == '1':
            if ton[tonNr]['actualTime'] <= ton[tonNr]['setTime']:
                ton[tonNr]['actualTime'] = int(1000 * time.perf_counter()) - ton[tonNr]['startTime']
        
        if tonEin and ton[tonNr]['actualTime'] >= ton[tonNr]['setTime']:
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}

    def block_tof(self, blockNr ,daten, tofNr, parameter1):
        global block, input, tof
        l_add= []
        tofEin = False
        for key in daten:
            if key[:1] == 'B':
                value = block[key]
            if key[:1] == 'I':
                value = input[key]
            # neu 1.11.21
            if not key:
                value = '0'
            l_add.append(value)

        result = l_add.count('1')

        if result == len(l_add):
            #return { blockNr: '1'}
            tofEin = True
        else:
            #return { blockNr: '0'}
            tofEin = False
        # init Wert vom plc proramm kann dann überschrieben werden
        if not tof[tofNr]['paramter']:
            tof[tofNr]['paramter'] = parameter1
        tof[tofNr]['setTime'] = tof[tofNr]['paramter']

        if not tofEin and tof[tofNr]['isWork'] == '1' and tof[tofNr]['actualTime'] >= tof[tofNr]['setTime']:
            tof[tofNr]['isWork'] = '0'

        if tofEin and tof[tofNr]['isWork'] == '0':
            tof[tofNr]['actualTime']  = 0
            #tof[tofNr]['startTime'] = time.ticks_ms()
            tof[tofNr]['isWork'] = '1'
            #print("tof ein")
        
        if tofEin:
            tof[tofNr]['startTime'] = int(1000 * time.perf_counter())
            
        if not tofEin and tof[tofNr]['isWork'] == '1':
            if tof[tofNr]['actualTime'] <= tof[tofNr]['setTime']:
                tof[tofNr]['actualTime'] = int(1000 * time.perf_counter()) - tof[tofNr]['startTime']
        
        if tofEin or tof[tofNr]['isWork'] == '1':
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}

    def block_inv(self, blockNr ,daten):
        l_add= []
        for key in daten:
            if key[:1] == 'B':
                #print(key)
                global block
                value = block[key]
            if key[:1] == 'I':
                #print(key)
                global input
                value = input[key]
            # neu 1.11.21
            if not key:
                value = '0'
            l_add.append(value)

        result = l_add.count('1')

        if result > 0:
            return { blockNr: '0'}
        else:
            return { blockNr: '1'}

    def block_sr(self, blockNr ,datenInput, srNr):
        global block, input, sr
        inputListe= []
        for key in datenInput:
            if key[:1] == 'B':
                value = block[key]
            if key[:1] == 'I':
                value = input[key]
            # neu 1.11.21
            if not key:
                value = '0'
            inputListe.append(value)
        #print(inputListe)
        if inputListe[0] == '1':
            sr[srNr] = '1'
        if inputListe[1] == '1':
            sr[srNr] = '0'
            
        if sr[srNr] == '1':
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}

    def block_ip(self, blockNr ,daten, ipNr):
        global block, input, ip
        inputListe= []
        for key in daten:
            if key[:1] == 'B':
                value = block[key]
            if key[:1] == 'I':
                value = input[key]
            # neu 1.11.21
            if not key:
                value = '0'
            inputListe.append(value)

        if inputListe[0] == '0':
            ip[ipNr] = '0'
            
        if ip[ipNr] == '0' and inputListe[0] == '1':
            ip[ipNr] = '1'
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}

    def block_cud(self, blockNr ,daten, cudNr, parameter1, parameter2):
        global block, input, cud
        inputListe= []
        for key in daten:
            if key[:1] == 'B':
                value = block[key]
            if key[:1] == 'I':
                value = input[key]
            # neu 1.11.21
            if not key:
                value = '0'
            inputListe.append(value)
        # init
        if cud[cudNr]['init'] == '0':
            cud[cudNr]['presetValue'] = parameter1
            cud[cudNr]['actualValue'] = cud[cudNr]['presetValue']
            cud[cudNr]['init'] = '1'
        
        # reset
        if inputListe[2] == '1':
            cud[cudNr]['presetValue'] = parameter1
            cud[cudNr]['actualValue'] = cud[cudNr]['presetValue']
            cud[cudNr]['init'] = '1'
            
        # flanke count UP
        if inputListe[0] == '0':
            cud[cudNr]['countUpFlanke'] = '0'
        
        # flanke count DOWN
        if inputListe[1] == '0':
            cud[cudNr]['countDownFlanke'] = '0'
        
        # count UP
        if cud[cudNr]['countUpFlanke'] == '0' and inputListe[0] == '1':
            cud[cudNr]['countUpFlanke'] = '1'
            cud[cudNr]['actualValue'] += 1
        
        # count DOWN
        if cud[cudNr]['countDownFlanke'] == '0' and inputListe[1] == '1':
            cud[cudNr]['countDownFlanke'] = '1'
            cud[cudNr]['actualValue'] -= 1
        
        # Block Output
        cud[cudNr]['setValue'] = parameter2
        if cud[cudNr]['actualValue'] >= cud[cudNr]['setValue']:
            return { blockNr: '1'}
        else:
            return { blockNr: '0'}

    def output_update(self, blockNr, outputNr, value):
        global output, block
        # neu 1.11.21 wenn in1 keine daten enhält
        if not value:
            wert = {outputNr: '0'}
            output.update(wert)
            return { blockNr: '0'} 

        wert = {outputNr: block[value]}
        output.update(wert)
        if block[value] == '1':
            return { blockNr: '1'}
        else:
            return { blockNr: '0'} 

    def periodicCallOff(self):
        self.simulatorEin = False
        self.runProgressbar = 0
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_20, fill="white")
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_40, fill="white")
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_60, fill="white")
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_80, fill="white")
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_100, fill="white")
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_text, fill="white")
        #print("aus")
        #Alle blocks wieder zurück auf yellow setzten
        global blocks
        #INPUT
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'INPUT':
                    iNr = blockItem['in1']
                    if 'I' in iNr:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightyellow')
                    if 'B' in iNr:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightyellow')
        #BLOCK
        for blockItem in blocks:
            if 'blockNr' in blockItem:
                 self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightyellow')
        #OUTPUT
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'ZUW':
                    self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightyellow')

    def input_output_aktualisieren(self):
        global input, output

        # INPUT
        if self.main_window_frame.checkI_1.get() == 1:
            input['I1'] = '1'
        else: 
            input['I1'] = '0'
        if self.main_window_frame.checkI_2.get() == 1:
            input['I2'] = '1'
        else: 
            input['I2'] = '0'
        if self.main_window_frame.checkI_3.get() == 1:
            input['I3'] = '1'
        else: 
            input['I3'] = '0'
        if self.main_window_frame.checkI_4.get() == 1:
            input['I4'] = '1'
        else: 
            input['I4'] = '0'
        if self.main_window_frame.checkI_5.get() == 1:
            input['I5'] = '1'
        else: 
            input['I5'] = '0'
        if self.main_window_frame.checkI_6.get() == 1:
            input['I6'] = '1'
        else: 
            input['I6'] = '0'
        if self.main_window_frame.checkI_7.get() == 1:
            input['I7'] = '1'
        else: 
            input['I7'] = '0'
        if self.main_window_frame.checkI_8.get() == 1:
            input['I8'] = '1'
        else: 
            input['I8'] = '0'

        #OUTPUT
        if 'Q1' in output:
            if output['Q1'] == '1':
                self.main_window_frame.check_O_1.select()
            else:
                self.main_window_frame.check_O_1.deselect()
        if 'Q2' in output:
            if output['Q2'] == '1':
                self.main_window_frame.check_O_2.select()
            else:
                self.main_window_frame.check_O_2.deselect()
        if 'Q3' in output:
            if output['Q3'] == '1':
                self.main_window_frame.check_O_3.select()
            else:
                self.main_window_frame.check_O_3.deselect()
        if 'Q4' in output:
            if output['Q4'] == '1':
                self.main_window_frame.check_O_4.select()
            else:
                self.main_window_frame.check_O_4.deselect()
        if 'Q5' in output:
            if output['Q5'] == '1':
                self.main_window_frame.check_O_5.select()
            else:
                self.main_window_frame.check_O_5.deselect()
        if 'Q6' in output:
            if output['Q6'] == '1':
                self.main_window_frame.check_O_6.select()
            else:
                self.main_window_frame.check_O_6.deselect()
        if 'Q7' in output:
            if output['Q7'] == '1':
                self.main_window_frame.check_O_7.select()
            else:
                self.main_window_frame.check_O_7.deselect()
        if 'Q8' in output:
            if output['Q8'] == '1':
                self.main_window_frame.check_O_8.select()
            else:
                self.main_window_frame.check_O_8.deselect()

    def i_o_zeichnen(self):
        global blocks, input, output, block, ton, cud, mw
        #INPUT
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'INPUT':
                    iNr = blockItem['in1']
                    if 'I' in iNr:
                        if input[iNr] == '1':
                            self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightgreen')
                        else:
                            self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightyellow')
                    if 'B' in iNr:
                        if block[iNr] == '1':
                            self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightgreen')
                        else:
                            self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightyellow')
        #BLOCK
        for blockItem in blocks:
            if 'blockNr' in blockItem:
                bNr = blockItem['blockNr']
                if block[bNr] == '1':
                    self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightgreen')
                else:
                    self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightyellow')
        #OUTPUT
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'ZUW':
                    oNr = blockItem['OUT']
                    if output[oNr] == '1':
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightgreen')
                    else:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectNr'], fill='lightyellow')
        #TON
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'TON':
                    self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameterActual'], 
                                                                    text= ton[blockItem['timerNr']]['actualTime'])
    
        #TOF
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'TOF':
                    self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameterActual'], 
                                                                    text= tof[blockItem['timerNr']]['actualTime'])

        #CUD
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'CUD':
                    self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameterActual'], 
                                                                    text= cud[blockItem['cudNr']]['actualValue'])
        
        #LT LIT GT
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'LT' or blockItem['typ'] == 'LIT' or blockItem['typ'] == 'GT':
                    if 'CUD' in blockItem['in1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= cud[blockItem['in1']]['actualValue'])
                    if 'TON' in blockItem['in1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= ton[blockItem['in1']]['actualTime'])
                    if 'TOF' in blockItem['in1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= tof[blockItem['in1']]['actualTime'])
                    if 'MW' in blockItem['in1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= mw[blockItem['in1']])
                    if 'CUD' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= cud[blockItem['in2']]['actualValue'])
                    if 'TON' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= ton[blockItem['in2']]['actualTime'])
                    if 'TOF' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= tof[blockItem['in2']]['actualTime'])
                    if 'MW' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= mw[blockItem['in2']])
        #GIT IT NIT
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'GIT' or blockItem['typ'] == 'IT' or blockItem['typ'] == 'NIT':
                    if 'CUD' in blockItem['in1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= cud[blockItem['in1']]['actualValue'])
                    if 'TON' in blockItem['in1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= ton[blockItem['in1']]['actualTime'])
                    if 'TOF' in blockItem['in1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= tof[blockItem['in1']]['actualTime'])
                    if 'MW' in blockItem['in1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= mw[blockItem['in1']])
                    if 'CUD' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= cud[blockItem['in2']]['actualValue'])
                    if 'TON' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= ton[blockItem['in2']]['actualTime'])
                    if 'TOF' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= tof[blockItem['in2']]['actualTime'])
                    if 'MW' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= mw[blockItem['in2']])
        #ADD
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'ADD':
                    if 'CUD' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= cud[blockItem['in2']]['actualValue'])
                    if 'TON' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= ton[blockItem['in2']]['actualTime'])
                    if 'TOF' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= tof[blockItem['in2']]['actualTime'])
                    if 'MW' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= mw[blockItem['in2']])
                    if 'CUD' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= cud[blockItem['in3']]['actualValue'])
                    if 'TON' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= ton[blockItem['in3']]['actualTime'])
                    if 'TOF' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= tof[blockItem['in3']]['actualTime'])
                    if 'MW' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= mw[blockItem['in3']])
                    if 'MW' in blockItem['out1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter3actual'], 
                                                                    text= mw[blockItem['out1']])
        #SUB
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'SUB':
                    if 'CUD' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= cud[blockItem['in2']]['actualValue'])
                    if 'TON' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= ton[blockItem['in2']]['actualTime'])
                    if 'TOF' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= tof[blockItem['in2']]['actualTime'])
                    if 'MW' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= mw[blockItem['in2']])
                    if 'CUD' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= cud[blockItem['in3']]['actualValue'])
                    if 'TON' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= ton[blockItem['in3']]['actualTime'])
                    if 'TOF' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= tof[blockItem['in3']]['actualTime'])
                    if 'MW' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= mw[blockItem['in3']])
                    if 'MW' in blockItem['out1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter3actual'], 
                                                                    text= mw[blockItem['out1']])
        #MUL
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'MUL':
                    if 'CUD' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= cud[blockItem['in2']]['actualValue'])
                    if 'TON' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= ton[blockItem['in2']]['actualTime'])
                    if 'TOF' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= tof[blockItem['in2']]['actualTime'])
                    if 'MW' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= mw[blockItem['in2']])
                    if 'CUD' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= cud[blockItem['in3']]['actualValue'])
                    if 'TON' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= ton[blockItem['in3']]['actualTime'])
                    if 'TOF' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= tof[blockItem['in3']]['actualTime'])
                    if 'MW' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= mw[blockItem['in3']])
                    if 'MW' in blockItem['out1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter3actual'], 
                                                                    text= mw[blockItem['out1']]) 
        #DIV
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'DIV':
                    if 'CUD' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= cud[blockItem['in2']]['actualValue'])
                    if 'TON' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= ton[blockItem['in2']]['actualTime'])
                    if 'TOF' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= tof[blockItem['in2']]['actualTime'])
                    if 'MW' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= mw[blockItem['in2']])
                    if 'CUD' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= cud[blockItem['in3']]['actualValue'])
                    if 'TON' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= ton[blockItem['in3']]['actualTime'])
                    if 'TOF' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= tof[blockItem['in3']]['actualTime'])
                    if 'MW' in blockItem['in3']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= mw[blockItem['in3']])
                    if 'MW' in blockItem['out1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter3actual'], 
                                                                    text= mw[blockItem['out1']]) 
        #MOVE
        for blockItem in blocks:
            if 'typ' in blockItem:
                if blockItem['typ'] == 'MOVE':
                    if 'CUD' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= cud[blockItem['in2']]['actualValue'])
                    if 'TON' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= ton[blockItem['in2']]['actualTime'])
                    if 'TOF' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= tof[blockItem['in2']]['actualTime'])
                    if 'MW' in blockItem['in2']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter1actual'], 
                                                                    text= mw[blockItem['in2']])
                    if 'CUD' in blockItem['out1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= cud[blockItem['out1']]['setValue'])
                    if 'TON' in blockItem['out1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= ton[blockItem['out1']]['setTime'])
                    if 'TOF' in blockItem['out1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= tof[blockItem['out1']]['setTime'])
                    if 'MW' in blockItem['out1']:
                        self.main_window_frame.zeichenwand.itemconfig(blockItem['objectParameter2actual'], 
                                                                    text= mw[blockItem['out1']])

    def run_prgogressbar_simulator(self):
        if self.runProgressbar > 5:
            self.runProgressbar = 0
            self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_20, fill="white")
            self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_40, fill="white")
            self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_60, fill="white")
            self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_80, fill="white")
            self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_100, fill="white")

        # zeichne forschrittbalken
        if self.runProgressbar == 1:
            self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_20, fill="lightgreen")
        if self.runProgressbar == 2:
            self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_40, fill="lightgreen")
        if self.runProgressbar == 3:
            self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_60, fill="lightgreen")
        if self.runProgressbar == 4:
            self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_80, fill="lightgreen")
        if self.runProgressbar == 5:
            self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_100, fill="lightgreen")

    def pre_periodicCall(self):

        # abfrage auf Programmänderung
        if self.programChange:
            tkinter.messagebox.showinfo('Sinulator', 'can not run simulator, first compile program')
            return

        self.simulatorEin = True
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.runProgressbar_text, fill="green")

        # periodicCall wird nur einmal gestartet dan läüft er durch weil canvas.after() aktiv
        if not self.zyklusTimeOn:
            self.periodicCall()

    def periodicCall(self):
        """
        Check every 200 ms if there is something new in the queue.
        """
        # nur Kopieren wenn Simulator ein ist (problem periodicCall einmal gestartet läüft dann immer)
        if self.simulatorEin:
            global sd, block, output
            sd2 = copy.deepcopy(sd)

        #self.input_output_aktualisieren()
        #self.i_o_zeichnen()

        #self.simulatorEin = True
        #if self.main_window_frame.check_modbus.get() == 1:
        if self.simulatorEin:

            fertig = True
            self.input_output_aktualisieren()
            self.i_o_zeichnen()
            # Varibale Fortschritsanzeige Simulator Prigessbar
            self.runProgressbar += 1
            self.run_prgogressbar_simulator()

            while fertig:

                if sd2:
                    daten = sd2.pop()
                    #Liste erzeugen
                    liste_input = []
                    blArt = ''
                    blNr = ''
                    tonNr = ''
                    tofNr = ''
                    parameter1 = ''
                    parameter2 = ''
                    srNr = ''
                    ipNr = ''
                    cudNr = ''
                    out = ''
                    #print(daten)
                    if 'IN1' in daten:
                        liste_input.append(daten['IN1'])
                    if 'IN2' in daten:
                        liste_input.append(daten['IN2'])
                    if 'IN3' in daten:
                        liste_input.append(daten['IN3'])
                    if 'OUT' in daten:
                        out = daten['OUT']
                    if 'TONNR' in daten:
                        tonNr = daten['TONNR']
                        parameter1 = daten['PARAMETER1']
                    if 'TOFNR' in daten:
                        tofNr = daten['TOFNR']
                        parameter1 = daten['PARAMETER1']
                    if 'SRNR' in daten:
                        srNr = daten['SRNR']
                    if 'IPNR' in daten:
                        ipNr = daten['IPNR']
                    if 'CUDNR' in daten:
                        cudNr = daten['CUDNR']
                        parameter1 = daten['PARAMETER1']
                        parameter2 = daten['PARAMETER2']
                    for key, value in daten.items():
                        if value == 'AND':
                            blArt = value
                            blNr = key
                        if value == 'OR':
                            blArt = value
                            blNr = key
                        if value == 'ZUW':
                            blArt = value
                            blNr = key
                        if value == 'INPUT':
                            blArt = value
                            blNr = key
                        if value == 'TON':
                            blArt = value
                            blNr = key
                        if value == 'TOF':
                            blArt = value
                            blNr = key
                        if value == 'SR':
                            blArt = value
                            blNr = key
                        if value == 'INV':
                            blArt = value
                            blNr = key
                        if value == 'IP':
                            blArt = value
                            blNr = key
                        if value == 'CUD':
                            blArt = value
                            blNr = key
                        if value == 'LT':
                            blArt = value
                            blNr = key
                        if value == 'LIT':
                            blArt = value
                            blNr = key
                        if value == 'GT':
                            blArt = value
                            blNr = key
                        if value == 'GIT':
                            blArt = value
                            blNr = key
                        if value == 'IT':
                            blArt = value
                            blNr = key
                        if value == 'NIT':
                            blArt = value
                            blNr = key
                        if value == 'ADD':
                            blArt = value
                            blNr = key
                        if value == 'SUB':
                            blArt = value
                            blNr = key
                        if value == 'MUL':
                            blArt = value
                            blNr = key
                        if value == 'DIV':
                            blArt = value
                            blNr = key
                        if value == 'MOVE':
                            blArt = value
                            blNr = key
                    if blArt == 'AND':
                        bl = self.block_and(blNr, liste_input)
                        block.update(bl)
                    if blArt == 'OR':
                        bl = self.block_or(blNr, liste_input)
                        block.update(bl)
                    if blArt == 'INPUT':
                        bl = self.block_and(blNr, liste_input)
                        block.update(bl)
                    if blArt == 'TON':
                        bl = self.block_ton(blNr, liste_input, tonNr, parameter1)
                        block.update(bl)
                    if blArt == 'TOF':
                        bl = self.block_tof(blNr, liste_input, tofNr, parameter1)
                        block.update(bl)
                    if blArt == 'SR':
                        bl = self.block_sr(blNr, liste_input, srNr)
                        block.update(bl)
                    if blArt == 'INV':
                        bl = self.block_inv(blNr, liste_input)
                        block.update(bl)
                    if blArt == 'IP':
                        bl = self.block_ip(blNr, liste_input, ipNr)
                        block.update(bl)
                    if blArt == 'CUD':
                        bl = self.block_cud(blNr, liste_input, cudNr, parameter1, parameter2)
                        block.update(bl)
                    if blArt == 'LT':
                        bl = self.block_compare(blNr, liste_input, blArt)
                        block.update(bl)
                    if blArt == 'LIT':
                        bl = self.block_compare(blNr, liste_input, blArt)
                        block.update(bl)
                    if blArt == 'GT':
                        bl = self.block_compare(blNr, liste_input, blArt)
                        block.update(bl)
                    if blArt == 'GIT':
                        bl = self.block_compare(blNr, liste_input, blArt)
                        block.update(bl)
                    if blArt == 'IT':
                        bl = self.block_compare(blNr, liste_input, blArt)
                        block.update(bl)
                    if blArt == 'NIT':
                        bl = self.block_compare(blNr, liste_input, blArt)
                        block.update(bl)
                    if blArt == 'ADD':
                        bl = self.block_aritmetic(blNr, liste_input, blArt, out)
                        block.update(bl)
                    if blArt == 'SUB':
                        bl = self.block_aritmetic(blNr, liste_input, blArt, out)
                        block.update(bl)
                    if blArt == 'MUL':
                        bl = self.block_aritmetic(blNr, liste_input, blArt, out)
                        block.update(bl)
                    if blArt == 'DIV':
                        bl = self.block_aritmetic(blNr, liste_input, blArt, out)
                        block.update(bl)
                    if blArt == 'MOVE':
                        bl = self.block_move(blNr, liste_input, out)
                        block.update(bl)
                    if blArt == 'ZUW':
                        bl = self.output_update(blNr, daten['OUT'], daten['IN1'])
                        block.update(bl)
                    #print(daten)
                if not sd2:
                    fertig = False

        #print(output['Q1'])
        #print("ton4: ", ton['TON4']['actualTime'])
        #print(ton)
        self.zyklusTimeOn = True
        self.main_window_frame.zeichenwand.after(200, self.periodicCall) 

    def page_daten_von_file(self, daten):
        global pageFokus, page1, page2, page3, page4, page5, page6

        if pageFokus == 0:
            page1.append(daten)
        if pageFokus == 1:
            page2.append(daten)
        if pageFokus == 2:
            page3.append(daten)
        if pageFokus == 3:
            page4.append(daten)
        if pageFokus == 4:
            page5.append(daten)
        if pageFokus == 5:
            page6.append(daten)

    def zeichnen_von_file_block(self):
        global blocksVonFile, blocks

        #blocks zeichnen
        while blocksVonFile:
            
            aktuelleBlock = blocksVonFile.pop()

            #f 'typ' in aktuelleBlock:
            if aktuelleBlock['typ'] == 'ZUW':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_zuweisung_erzeugen_von_file(aktuelleBlock['blockNr'], aktuelleBlock['OUT'], x, y)
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['OUT'] = aktuelleBlock['OUT']
                        block['in1'] = aktuelleBlock['in1']

            #if 'typ' in aktuelleBlock:
            if aktuelleBlock['typ'] == 'INPUT':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_input_erzeugen_von_file(aktuelleBlock['blockNr'], aktuelleBlock['in1'], x, y)
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
            
            #block_timer(self, Nr, x, y, typ, parameter1):
            if aktuelleBlock['typ'] == 'TON':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_timer(aktuelleBlock['blockNr'], x, y, 
                                        aktuelleBlock['timerNr'], aktuelleBlock['parameter1'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']

            #block_timer(self, Nr, x, y, typ, parameter1):
            if aktuelleBlock['typ'] == 'TOF':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_timer(aktuelleBlock['blockNr'], x, y, 
                                        aktuelleBlock['timerNr'], aktuelleBlock['parameter1'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']

            #block_sr_rs(self, Nr, x, y, typ):
            if aktuelleBlock['typ'] == 'SR':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_sr_rs(aktuelleBlock['blockNr'], x, y, 
                                        aktuelleBlock['srNr'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']

            #block_inv_erzeugen(self, Nr, x, y, typ):
            if aktuelleBlock['typ'] == 'INV':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_inv_erzeugen(aktuelleBlock['blockNr'], x, y, 'INV')
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']

            #block_ip_erzeugen(self, Nr, x, y, typ):
            if aktuelleBlock['typ'] == 'IP':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_ip_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        aktuelleBlock['ipNr'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']

            #block_cud_erzeugen(self, Nr, x, y, typ, parameter1, parameter2):
            if aktuelleBlock['typ'] == 'CUD':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_cud_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        aktuelleBlock['cudNr'], aktuelleBlock['parameter1'], aktuelleBlock['parameter2'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']
                        block['in3'] = aktuelleBlock['in3']

            #block_copare_erzeugen(self, Nr, x, y, typ, parameter1, parameter2):
            if aktuelleBlock['typ'] == 'LT':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_compare_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        '<I', aktuelleBlock['parameter1'], aktuelleBlock['parameter2'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']

            #block_copare_erzeugen(self, Nr, x, y, typ, parameter1, parameter2):
            if aktuelleBlock['typ'] == 'LIT':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_compare_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        '<=I', aktuelleBlock['parameter1'], aktuelleBlock['parameter2'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']

            #block_copare_erzeugen(self, Nr, x, y, typ, parameter1, parameter2):
            if aktuelleBlock['typ'] == 'GT':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_compare_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        '>I', aktuelleBlock['parameter1'], aktuelleBlock['parameter2'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']
            
            #block_copare_erzeugen(self, Nr, x, y, typ, parameter1, parameter2):
            if aktuelleBlock['typ'] == 'GIT':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_compare_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        '>=I', aktuelleBlock['parameter1'], aktuelleBlock['parameter2'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']

            #block_copare_erzeugen(self, Nr, x, y, typ, parameter1, parameter2):
            if aktuelleBlock['typ'] == 'IT':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_compare_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        '==I', aktuelleBlock['parameter1'], aktuelleBlock['parameter2'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']
            
            #block_compare_erzeugen(self, Nr, x, y, typ, parameter1, parameter2):
            if aktuelleBlock['typ'] == 'NIT':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_compare_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        '!=I', aktuelleBlock['parameter1'], aktuelleBlock['parameter2'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']

            #block_aritmetic_erzeugen(self, Nr, x, y, typ, parameter1, parameter2, parameter3):
            if aktuelleBlock['typ'] == 'ADD':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_aritmetic_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        'ADD', aktuelleBlock['parameter1'], aktuelleBlock['parameter2'], aktuelleBlock['parameter3'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']
                        block['in3'] = aktuelleBlock['in3']
            
            #block_aritmetic_erzeugen(self, Nr, x, y, typ, parameter1, parameter2, parameter3):
            if aktuelleBlock['typ'] == 'SUB':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_aritmetic_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        'SUB', aktuelleBlock['parameter1'], aktuelleBlock['parameter2'], aktuelleBlock['parameter3'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']
                        block['in3'] = aktuelleBlock['in3']

            #block_aritmetic_erzeugen(self, Nr, x, y, typ, parameter1, parameter2, parameter3):
            if aktuelleBlock['typ'] == 'MUL':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_aritmetic_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        'MUL', aktuelleBlock['parameter1'], aktuelleBlock['parameter2'], aktuelleBlock['parameter3'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']
                        block['in3'] = aktuelleBlock['in3']

            #block_aritmetic_erzeugen(self, Nr, x, y, typ, parameter1, parameter2, parameter3):
            if aktuelleBlock['typ'] == 'DIV':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_aritmetic_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        'DIV', aktuelleBlock['parameter1'], aktuelleBlock['parameter2'], aktuelleBlock['parameter3'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']
                        block['in3'] = aktuelleBlock['in3']

            #block_move_erzeugen(self, Nr, x, y, parameter1, parameter2):
            if aktuelleBlock['typ'] == 'MOVE':
                x = aktuelleBlock['x']
                y = aktuelleBlock['y']
                block = self.block_move_erzeugen(aktuelleBlock['blockNr'], x, y, 
                                        aktuelleBlock['parameter1'], aktuelleBlock['parameter2'])
                blocks.append(block)
                for block in blocks:
                    if block['blockNr'] == aktuelleBlock['blockNr']:
                        block['out1'] = aktuelleBlock['out1']
                        block['in1'] = aktuelleBlock['in1']
                        block['in2'] = aktuelleBlock['in2']

            if aktuelleBlock['typ'] == 'OR':
                if 'in3' in aktuelleBlock:
                    x = aktuelleBlock['x']
                    y = aktuelleBlock['y']
                    block = self.block_and_3(aktuelleBlock['blockNr'], x, y, '>I')
                    blocks.append(block)                        , 
                    for block in blocks:
                        if block['blockNr'] == aktuelleBlock['blockNr']:
                            block['out1'] = aktuelleBlock['out1']
                            block['in1'] = aktuelleBlock['in1']
                            block['in2'] = aktuelleBlock['in2'] 
                            block['in3'] = aktuelleBlock['in3']                        
                else:
                    x = aktuelleBlock['x']
                    y = aktuelleBlock['y']
                    block = self.block_and_2(aktuelleBlock['blockNr'], x, y, '>I')
                    blocks.append(block)                        , 
                    for block in blocks:
                        if block['blockNr'] == aktuelleBlock['blockNr']:
                            block['out1'] = aktuelleBlock['out1']
                            block['in1'] = aktuelleBlock['in1']
                            block['in2'] = aktuelleBlock['in2'] 

            if aktuelleBlock['typ'] == 'AND':
                if 'in3' in aktuelleBlock:
                    x = aktuelleBlock['x']
                    y = aktuelleBlock['y']
                    block = self.block_and_3(aktuelleBlock['blockNr'], x, y, '&')
                    blocks.append(block)                         
                    for block in blocks:
                        if block['blockNr'] == aktuelleBlock['blockNr']:
                            block['out1'] = aktuelleBlock['out1']
                            block['in1'] = aktuelleBlock['in1']
                            block['in2'] = aktuelleBlock['in2'] 
                            block['in3'] = aktuelleBlock['in3']                        
                else:
                    x = aktuelleBlock['x']
                    y = aktuelleBlock['y']
                    block = self.block_and_2(aktuelleBlock['blockNr'], x, y, '&')
                    blocks.append(block)                         
                    for block in blocks:
                        if block['blockNr'] == aktuelleBlock['blockNr']:
                            block['out1'] = aktuelleBlock['out1']
                            block['in1'] = aktuelleBlock['in1']
                            block['in2'] = aktuelleBlock['in2']
        blocks.reverse()

    def zeichnen_von_file_line(self):
        global linesVonFile, blocks, lines

        while linesVonFile:

            lineAktuell = linesVonFile.pop()
            linieDaten = [0, 0, 0, 0, '', '', '']

            linieDaten[0] = lineAktuell['x']
            linieDaten[1] = lineAktuell['y']
            linieDaten[2] = lineAktuell['x2']
            linieDaten[3] = lineAktuell['y2']
            linieDaten[4] = lineAktuell['start']
            linieDaten[5] = lineAktuell['ziel']
            linieDaten[6] = lineAktuell['zielIn']
            line = self.line(lineAktuell['lineNr'], linieDaten)
            lines.append(line)

    def zeichnen_von_file_comment(self):
        global commentsVonFile, comments

        #blocks zeichnen
        while commentsVonFile:
            
            aktuelleComment = commentsVonFile.pop()

            #f 'typ' in aktuelleBlock:
            if aktuelleComment['typ'] == 'COMMENT':
                x = aktuelleComment['x']
                y = aktuelleComment['y']
                comment = self.block_comment_erzeugen(aktuelleComment['commentNr'], x, y, aktuelleComment['parameter1'])
                comments.append(comment)           

    def file_save_as(self):
        global blocks, lines, comments, page1, page2, page3, page4, page5, page6
        '''with open('blocks.json', 'w') as fp:
            json.dump(blocks, fp)
        with open('lines.json', 'w') as fp:
            json.dump(lines, fp)'''
        pages = []
        pages.append(page1)
        pages.append(page2)
        pages.append(page3)
        pages.append(page4)
        pages.append(page5)
        pages.append(page6)
        blockProgramm = []     
        blockProgramm.append(lines)
        blockProgramm.append(blocks)
        blockProgramm.append(comments)
        blockProgramm.append(pages)
        blockProgrammJson = json.dumps(blockProgramm)

        # ohne encrypt
        #ftypes = [('Block Programm', '*.json'), ('Python files', '*.py'), ('All files', '*')]
        '''ftypes = [('Block Programm', '*.json')]
        f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".json", filetypes = ftypes)
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        #text2save = 'test' # starts from `1.0`, not `0.0`
        f.write(blockProgrammJson)
        f.close()'''

        # mit encrypt
        #ftypes = [('Block Programm', '*.json'), ('Python files', '*.py'), ('All files', '*')]
        ftypes = [('Block Programm', '*.fbd')]
        f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".json", filetypes = ftypes)
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        password = 'welt'
        encText = self.encrypt(blockProgrammJson, password)
        with open(f.name, 'w') as fp:
            json.dump(encText, fp)

         # write File name in Page File
        #ff = str(f)
        FileNameL = f.name.rsplit('/') 
        FileName = FileNameL[-1]

        self.main_window_frame.selectFileNamePath.config(text= f.name)
        self.main_window_frame.selectFileName.config(text= FileName)

        # Varibale für aktuelle Datei ausgewählt
        self.selectFile = f.name
    
    def file_save(self):
        global blocks, lines, comments, page1, page2, page3, page4, page5, page6
        '''with open('blocks.json', 'w') as fp:
            json.dump(blocks, fp)
        with open('lines.json', 'w') as fp:
            json.dump(lines, fp)'''
        pages = []
        pages.append(page1)
        pages.append(page2)
        pages.append(page3)
        pages.append(page4)
        pages.append(page5)
        pages.append(page6)
        blockProgramm = []     
        blockProgramm.append(lines)
        blockProgramm.append(blocks)
        blockProgramm.append(comments)
        blockProgramm.append(pages)
        #blockProgrammJson = json.dumps(blockProgramm)
        
        # blockprogramm speichern in selectierte File
        if not self.selectFile:
            tkinter.messagebox.showerror('File save', 'No file select! Please open or save as first.')
            return

        # ohne encrypt
        #with open(self.selectFile, 'w') as fp:
            #json.dump(blockProgramm, fp)
        
        # mit encrypt
        blockProgrammJson = json.dumps(blockProgramm)
        password = 'welt'
        encText = self.encrypt(blockProgrammJson, password)
        with open(self.selectFile, 'w') as fp:
            json.dump(encText, fp)

    def file_open(self):
        global blocksVonFile, linesVonFile, commentsVonFile, pageVonFile, page1, page2, page3, page4, page5, page6, blocks

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        # abfarge ob momentan projekt geladen
        yes = False
        if self.selectFile or blocks:   
            yes = tkinter.messagebox.askyesno('Project selected', 'You are sure you delete the current project want open new project?')
            if not yes:
                return
            if yes:
                self.del_projekt()

        ftypes = [('Block Programm', '*.fbd'), ('Python files', '*.py'), ('All files', '*')]
        dlg = tkinter.filedialog.askopenfilename(filetypes = ftypes)
        '''with open('blocks.json', 'r') as fp:
            blocksVonFile = json.load(fp)
        with open('lines.json', 'r') as fp:
            linesVonFile = json.load(fp)'''

        # wenn keine Datei ausgewählt beenden
        if not dlg:
            return

        # ohne encrypt
        #with open(dlg , 'r') as fp:
            #vonFile = json.load(fp)

        # mit encrypt
        with open(dlg , 'r') as fp:
            vonFileEnc = json.load(fp)
        password = 'welt'
        File = self.decrypt(vonFileEnc, password)
        vonFile = json.loads(File)

        linesVonFile = vonFile[0]
        blocksVonFile = vonFile[1]
        commentsVonFile = vonFile[2]
        pageVonFile = vonFile[3]
        self.zeichnen_von_file_block()
        self.zeichnen_von_file_line()
        self.zeichnen_von_file_comment()

        # Page 
        page1 = pageVonFile[0]
        page2 = pageVonFile[1]
        page3 = pageVonFile[2]
        page4 = pageVonFile[3]
        page5 = pageVonFile[4]
        page6 = pageVonFile[5]
        # erste Page zeigen
        self.zeichnen_aktuelle_page_block(page1)

        # write File name in Page File
        FileNameL = dlg.rsplit('/') 
        FileName = FileNameL[-1]
        self.main_window_frame.selectFileNamePath.config(text= dlg)
        self.main_window_frame.selectFileName.config(text= FileName)

        # Varibale für aktuelle Datei ausgewählt
        self.selectFile = dlg

        # Prgrammänderung
        self.programChange = True

    def page_export(self):

        tkinter.messagebox.showinfo('Page export', 'not available at the moment, implemented in the future.')
        return

        global blocks, lines, comments, page1, page2, page3, page4, page5, page6, pageFokus

        pages = []
        pages.append(page1)
        pages.append(page2)
        pages.append(page3)
        pages.append(page4)
        pages.append(page5)
        pages.append(page6)
        blockProgramm = []     
        blockProgramm.append(lines)
        blockProgramm.append(blocks)
        blockProgramm.append(comments)
        blockProgramm.append(pages)
        blockProgrammJson = json.dumps(blockProgramm)
        ftypes = [('Programm Page', '*.page')]
        f = tkinter.filedialog.asksaveasfile(mode='w', defaultextension=".page", filetypes = ftypes)
        if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
            return
        #text2save = 'test' # starts from `1.0`, not `0.0`
        f.write(blockProgrammJson)
        f.close()

    def page_import(self):
        tkinter.messagebox.showinfo('Page import', 'not available at the moment, implemented in the future.')

    def upload_plc(self):
        #file = "C:\Users\hs\Downloads\Micropython\Thonny IDE\thonny-3.3.10-windows\thonny.exe"
        #os.startfile(r"C:\Users\hs\Downloads\Micropython\Thonny IDE\thonny-3.3.10-windows\thonny.exe")
        global uploadPathExe
        if not uploadPathExe:
            tkinter.messagebox.showinfo('Sart upload programm', 'There no exe, write in setting the path from exe.')
            return
        #exe = 'r' + '"' + uploadPathExe + '"'
        #os.startfile(uploadPathExe) #für windows
        os.popen(uploadPathExe)
    
    def del_projekt(self):
        global blocks, lines, comments
        blocks = []
        lines = []
        comments = []
        #self.main_window_frame.zeichenwand.delete("all")
        allId = self.main_window_frame.zeichenwand.find_all()
        #print(allId)
        allIdList = list(allId)

        # alle softkey inder Zeichung Page1 - 6 aus Liste nehmen (id buttonBG)
        allIdList.remove(self.main_window_frame.buttonBG)
        allIdList.remove(self.main_window_frame.buttonBG2)
        allIdList.remove(self.main_window_frame.buttonBG3)
        allIdList.remove(self.main_window_frame.buttonBG4)
        allIdList.remove(self.main_window_frame.buttonBG5)
        allIdList.remove(self.main_window_frame.buttonBG6)
        allIdList.remove(self.main_window_frame.buttonTXT)
        allIdList.remove(self.main_window_frame.buttonTXT2)
        allIdList.remove(self.main_window_frame.buttonTXT3)
        allIdList.remove(self.main_window_frame.buttonTXT4)
        allIdList.remove(self.main_window_frame.buttonTXT5)
        allIdList.remove(self.main_window_frame.buttonTXT6)
        allIdList.remove(self.main_window_frame.runProgressbar_20)
        allIdList.remove(self.main_window_frame.runProgressbar_40)
        allIdList.remove(self.main_window_frame.runProgressbar_60)
        allIdList.remove(self.main_window_frame.runProgressbar_80)
        allIdList.remove(self.main_window_frame.runProgressbar_100)
        allIdList.remove(self.main_window_frame.runProgressbar_text)
   
        # losche alle id Objekte aus der Zeichnug alle Pages
        while allIdList:
            idObject = allIdList.pop()
            self.main_window_frame.zeichenwand.delete(idObject)

        #allId = self.main_window_frame.zeichenwand.find_all()
        #print(allId)

        #Anzahl der Blöcke und Linien und Komenntare
        self.aktuelleBlockNr = 0
        self.aktuelleLineNr = 0
        self.aktuelleInputNr = 0
        self.aktuelleOutputNr = 0
        self.aktuelleTonNr = 0
        self.aktuelleTofNr = 0
        self.aktuelleSrNr = 0
        self.aktuelleIpNr = 0
        self.aktuelleCudNr = 0
        self.aktuelleCommentNr = 0

        # aktuelle Verzeicniss löschen
        self.main_window_frame.selectFileNamePath.config(text= 'No file select!')
        self.main_window_frame.selectFileName.config(text= 'No file select!')

        # Varibale für aktuelle Datei ausgewählt
        self.selectFile = ''

        # Page1 auswählen
        global pageFokus, blockPositionFokus, page1, page2, page3, page4, page5, page6
        # Page daten
        page1 = []
        page2 = []
        page3 = []
        page4 = []
        page5 = []
        page6 = []
        pageFokus = 0
        blockPositionFokus = [0, 0, '', '']
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.buttonBG, fill="white")
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.buttonBG2, fill="grey80")
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.buttonBG3, fill="grey80")
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.buttonBG4, fill="grey80")
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.buttonBG5, fill="grey80")
        self.main_window_frame.zeichenwand.itemconfig(self.main_window_frame.buttonBG6, fill="grey80")
        self.zeichnen_aktuelle_page1()

    def del_all(self):

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        yesNo = False
        yesNo = tkinter.messagebox.askyesno('Delete project', 'You are sure you delete all data want a new project?')
        if not yesNo:
            return
        if yesNo:
            pass
        
        self.del_projekt()

    def del_object(self):
        global blocks, lines, blockPositionFokus, comments, pageFokus, page1, page2, page3, page4, page5, page6

        # simulator not run
        if self.simulatorEin:
            tkinter.messagebox.showinfo('Simulator', 'simulator run, stop simulator.')
            return

        for line in lines:
            if line['start'] == blockPositionFokus[2]:
                zielBlockNr = line['ziel']
                for block in blocks:
                    if block['blockNr'] == line['start']:
                        block['out1'] = ''
                if line['ziel'] == zielBlockNr:
                    for block in blocks:
                        if block['blockNr'] == line['ziel']:
                            if line['zielIn'] == 'in1':
                                block['in1'] = ''
                            if line['zielIn'] == 'in2':
                                block['in2'] = ''
                            if line['zielIn'] == 'in3':
                                block['in3'] = ''    
        for line in lines:       
            if line['ziel'] == blockPositionFokus[2]:
                self.main_window_frame.zeichenwand.delete(line["objectNr"])
                self.main_window_frame.zeichenwand.delete(line["objectNr2"])
                self.main_window_frame.zeichenwand.delete(line["objectNr3"])
                lines.remove(line)
                # line Nummer aus atuellen Page löschen
                if pageFokus == 0:
                    page1.remove(line["lineNr"])
                if pageFokus == 1:
                    page2.remove(line["lineNr"])
                if pageFokus == 2:
                    page3.remove(line["lineNr"])
                if pageFokus == 3:
                    page4.remove(line["lineNr"])
                if pageFokus == 4:
                    page5.remove(line["lineNr"])
                if pageFokus == 5:
                    page6.remove(line["lineNr"])

        for line in lines:
            if line['start'] == blockPositionFokus[2]:
                self.main_window_frame.zeichenwand.delete(line["objectNr"])
                self.main_window_frame.zeichenwand.delete(line["objectNr2"])
                self.main_window_frame.zeichenwand.delete(line["objectNr3"])
                lines.remove(line)
                # line Nummer aus atuellen Page löschen
                if pageFokus == 0:
                    page1.remove(line["lineNr"])
                if pageFokus == 1:
                    page2.remove(line["lineNr"])
                if pageFokus == 2:
                    page3.remove(line["lineNr"])
                if pageFokus == 3:
                    page4.remove(line["lineNr"])
                if pageFokus == 4:
                    page5.remove(line["lineNr"])
                if pageFokus == 5:
                    page6.remove(line["lineNr"])

        # zweiter aufruf Linie 2 wird jetzt gelöscht (warum ???)
        for line in lines:       
            if line['ziel'] == blockPositionFokus[2]:
                self.main_window_frame.zeichenwand.delete(line["objectNr"])
                self.main_window_frame.zeichenwand.delete(line["objectNr2"])
                self.main_window_frame.zeichenwand.delete(line["objectNr3"])
                lines.remove(line)
                # line Nummer aus atuellen Page löschen
                if pageFokus == 0:
                    page1.remove(line["lineNr"])
                if pageFokus == 1:
                    page2.remove(line["lineNr"])
                if pageFokus == 2:
                    page3.remove(line["lineNr"])
                if pageFokus == 3:
                    page4.remove(line["lineNr"])
                if pageFokus == 4:
                    page5.remove(line["lineNr"])
                if pageFokus == 5:
                    page6.remove(line["lineNr"])

        for block in blocks:
            if block['blockNr'] == blockPositionFokus[2]:
                self.main_window_frame.zeichenwand.delete(block["objectNr"])
                if 'objectNrInput1' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectNrInput1"])
                if 'objectNrInput2' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectNrInput2"])
                if 'objectNrInput3' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectNrInput3"])
                if 'objectNrOutput' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectNrOutput"])
                if 'objectNrTextBlockNr' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectNrTextBlockNr"])
                if 'objectNrTextBlockTyp' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectNrTextBlockTyp"])
                if 'objectTextTimerNr' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectTextTimerNr"])
                if 'objectParameterSet' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectParameterSet"])
                if 'objectParameterActual' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectParameterActual"])
                if 'objectTextSet' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectTextSet"])
                if 'objectTextReset' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectTextReset"])
                if 'objectTextIpNr' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectTextIpNr"])
                if 'objectTextUp' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectTextUp"])
                if 'objectTextDown' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectTextDown"])
                if 'objectTextCounterNr' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectTextCounterNr"])
                if 'objectParameterPreset' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectParameterPreset"])
                if 'objectParameter1' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectParameter1"])
                if 'objectParameter2' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectParameter2"])
                if 'objectParameter3' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectParameter3"])
                if 'objectParameter1actual' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectParameter1actual"])
                if 'objectParameter2actual' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectParameter2actual"])
                if 'objectParameter3actual' in block:
                    self.main_window_frame.zeichenwand.delete(block["objectParameter3actual"])
                blocks.remove(block)

        for comment in comments:
            if comment['commentNr'] == blockPositionFokus[2]:
                self.main_window_frame.zeichenwand.delete(comment["objectNr"])
                if 'objectNrTextBlockNr' in comment:
                    self.main_window_frame.zeichenwand.delete(comment["objectNrTextBlockNr"])
                if 'objectParameter1' in comment:
                    self.main_window_frame.zeichenwand.delete(comment["objectParameter1"])
                #neu 4.11.21
                comments.remove(comment)

        # aktuelle Page Block löschen
        if 'B' in blockPositionFokus[2]:
            if pageFokus == 0:
                page1.remove(blockPositionFokus[2])
            if pageFokus == 1:
                page2.remove(blockPositionFokus[2])
            if pageFokus == 2:
                page3.remove(blockPositionFokus[2])
            if pageFokus == 3:
                page4.remove(blockPositionFokus[2])
            if pageFokus == 4:
                page5.remove(blockPositionFokus[2])
            if pageFokus == 5:
                page6.remove(blockPositionFokus[2])

        # Prgrammänderung
        self.programChange = True

    def del_page(self):
        #global blocks
        #print(blocks)
        #return
        tkinter.messagebox.showinfo('Delete page', 'not available at the moment, implemented in the future.')
        return
        print('del page')
        # lade blockprogramm
        encText = ''
        with open('encBlockprogramm.json') as fp:
            encText = json.load(fp)

        password = 'welt'
        text = self.decrypt(encText, password)
        textDict = json.loads(text)
        print(textDict)
        sd_1 = textDict[1]
        config_1 = textDict[0]
        print(sd_1)
        print(config_1)

    def v_line(self):
        pass

def main():
    main_win = tk.Tk()
    app = Application(main_win, TITLE)
    main_win.mainloop()

main()
