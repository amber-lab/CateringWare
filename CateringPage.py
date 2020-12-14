#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:23:03 2019

@author: L.A.B
"""

#FRAME DE PRODUCTS
class CateringPage(tk.Frame):
    def __init__(self, master, background_hex = '#757575'):
        tk.Frame.__init__(self, master, background = background_hex)
        self.widgets = list()
#        self.after(500, self.c_update)

    def addWidget(self, widget):
        if type(widget) == type(tk) or type(widget) == type(ttk):
            self.widgets.append(widget)
        else:
            print("Inserir apenas widgets tkinter")

    def showWidgets(self):
        rely_n = 0.1
        for widget in self.widgets:
            if widget.__class__.__name__ == 'CateringPageTitleLabel':
                widget.place(relx = 0.1, rely = rely_n, relwidht = 0.8, relheight = 0.1)
                rely_n += 0.1
            elif widget.winfo() == 'Frame':
                widget.place(relx = 0.15, rely = rely_n, relwidth = 0.85, relheight = 0.05)

    
    def setStatus(self, mensage):
        self.status_bar = tk.Label(self, text = mensage, image = self.photo, compound = 'center', font = FONT, relief = 'sunken')
        self.status_bar.photo = self.photo
        self.status_bar.place(relx = 0, rely = 0.95, relwidth = 1, relheight = 0.05)
        self.counter = 10