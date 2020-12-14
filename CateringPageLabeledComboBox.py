# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 14:50:08 2020

@author: L.A.B
"""

class CateringPageLabeledComboBox(tk.Frame):
    def __init__(self, master, text, lista, photo):
        tk.Frame.__init__(self, master, background = CINZA)
        self.photo = photo
        self.label = tk.Label(self, text = text, image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        self.label.photo = self.photo
        self.label.place(relx = 0, rely = 0, relwidth = 0.6, relheight = 1)
        self.entry_v = tk.StringVar()
        self.entry = ttk.Combobox(self, textvariable = self.entry_v, values = lista, state = 'readonly', font = MINI_FONT)
        self.entry.set(lista[0])
        self.entry.place(relx = 0.65, rely = 0, relwidth = 0.35, relheight = 1)

    def get(self):
        return(self.entry_v.get())
    
    def setEntryValue(self, value):
        self.entry.set(value)