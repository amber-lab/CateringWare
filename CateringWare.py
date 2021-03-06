#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Sat Oct 19 17:35:50 2019

@author: L.A.B
"""

import tkinter as tk
import sqlite3
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime, date
import os
from cat import *

class CateringApp(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.title('CateringWare')
        self.wm_iconbitmap('.\\img\\icon.ico')
        w = self.winfo_screenwidth()
        h = self.winfo_screenheight()
        if w <= 800:
            FONT = ('Bodoni MT Black', '11')
            MEDIUM_FONT = ('Bodoni MT Black', '9')
            MINI_FONT = ('Baskerville Old Face', '9')
            self.minsize(int(w * 0.8), int(h * 0.8))
            print("\n\n800\n\n")
            
        elif w <= 1280:
            FONT = ('Bodoni MT Black', '13')
            MEDIUM_FONT = ('Bodoni MT Black', '11')
            MINI_FONT = ('Baskerville Old Face', '11')
            self.minsize(int(w * 0.8), int(h * 0.8))
            print("\n\n1280\n\n")
            
        else:
            print("\n\nMAIOR\n\n")
            self.minsize(int(w * 0.75), int(h * 0.75))
            
        self.geometry('{w}x{h}+{wp}+{hp}'.format(w = int(self.winfo_screenwidth() * 0.8), h = int(self.winfo_screenheight() * 0.8), wp = int(self.winfo_screenwidth() * 0.1), hp = int(self.winfo_screenheight() * 0.1)))

        #FRAME MENU
        self.menu_frame = CateringPageMenuFrame(self)
        self.menu_frame.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)

        #FRAME CINZA
        self.bg_frame = tk.Frame(self, background = CINZA)
        self.bg_frame.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight = 1)

        #BINDS BUTOES MENU
        self.menu_frame.menu_button.button.bind('<ButtonRelease-1>', self.setSetsSubMenu)
        self.menu_frame.products_button.button.bind('<ButtonRelease-1>', self.setProductsPage)
        self.menu_frame.workers_button.button.bind('<ButtonRelease-1>', self.setWorkersPage)
        self.menu_frame.service_button.button.bind('<ButtonRelease-1>', self.setServicePage)
        self.menu_frame.eira_button.button.bind('<ButtonRelease-1>', self.setHomePage)
        
        self.page_frame = CateringHomePage(self)
        self.page_frame.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight = 1)
        
    def updateMenuBar(self):
        try:
            self.page_frame.destroy()
        except:
            pass

    def setProductsPage(self, event):
        self.updateMenuBar()
        self.menu_frame.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)
        self.page_frame = CateringProductPage(self)
        self.page_frame.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight = 1)

    def setWorkersPage(self, event):
        self.updateMenuBar()
        self.menu_frame.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)
        self.page_frame = CateringWorkerPage(self)
        self.page_frame.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight = 1)
        
    def setSetsSubMenu(self, event):
        self.updateMenuBar()
        self.menu_frame.place(relx = 0, rely = 0, relwidth = 0.125, relheight = 1)
        self.page_frame = CateringPageSetsMenu(self)
        self.page_frame.place(relx = 0.125, rely = 0, relwidth = 0.125, relheight = 1)
        self.page_frame.menu_button.button.bind('<ButtonRelease-1>', self.setMenuPage)
        self.page_frame.bar_button.button.bind('<ButtonRelease-1>', self.setBarPage)
        self.page_frame.desserts_button.button.bind('<ButtonRelease-1>', self.setDessertsPage)
        self.page_frame.appetizers_button.button.bind('<ButtonRelease-1>', self.setAppetizersPage)

    def setServicePage(self, event):
        self.updateMenuBar()
        self.menu_frame.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)
        self.page_frame = CateringServicePage(self)
        self.page_frame.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight = 1)

    def setMenuPage(self, event):
        self.updateMenuBar()
        self.menu_frame.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)
        self.page_frame = CateringMenuPage(self)
        self.page_frame.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight = 1)
    
    def setBarPage(self, event):
        self.updateMenuBar()
        self.menu_frame.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)
        self.page_frame = CateringBarPage(self)
        self.page_frame.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight = 1)
        
    def setDessertsPage(self, event):
        self.updateMenuBar()
        self.menu_frame.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)
        self.page_frame = CateringDessertsPage(self)
        self.page_frame.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight = 1)
    
    def setAppetizersPage(self, event):
        self.updateMenuBar()
        self.menu_frame.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)
        self.page_frame = CateringAppetizersPage(self)
        self.page_frame.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight = 1)

    def setHomePage(self, event):
        self.updateMenuBar()
        self.menu_frame.place(relx = 0, rely = 0, relwidth = 0.25, relheight = 1)
        self.page_frame = CateringHomePage(self)
        self.page_frame.place(relx = 0.25, rely = 0, relwidth = 0.75, relheight = 1)

app = CateringApp()
app.mainloop()



