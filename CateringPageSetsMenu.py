# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 20:30:52 2020

@author: L.A.B
"""

class CateringPageSetsMenu(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, bg = CINZA)

        self.menu_button = CateringPageMenuButton(self, image = BG_VERDE, text = 'Refeição')
        self.menu_button.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.25)

        self.bar_button = CateringPageMenuButton(self, image = BG_VERDE, text = 'Bar')
        self.bar_button.place(relx = 0, rely = 0.25, relwidth = 1, relheight = 0.25)

        self.desserts_button = CateringPageMenuButton(self, image = BG_VERDE, text = 'Sobremesas')
        self.desserts_button.place(relx = 0, rely = 0.5, relwidth = 1, relheight = 0.25)

        self.appetizers_button = CateringPageMenuButton(self, image = BG_VERDE, text = 'Entradas')
        self.appetizers_button.place(relx = 0, rely = 0.75, relwidth = 1, relheight = 0.25)