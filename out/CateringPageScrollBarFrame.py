# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:35:54 2019

@author: L.A.B
"""

#LABEL FRAME COM LISTBOX E SCROLLBAR
class CateringPageScrollBarFrame(tk.LabelFrame):
    def __init__(self, master, text, color):
        tk.LabelFrame.__init__(self, master, text = text, font = FONT, bg = color)
        
        scrollbar = tk.Scrollbar(self, orient = 'vertical', bg = color)
        self.listbox = tk.Listbox(self, yscrollcommand = scrollbar.set, selectforeground = 'black', selectbackground = color, font = MINI_FONT)
        scrollbar.config(command=self.listbox.yview)
        
        self.listbox.pack(side = 'left', fill = 'both', expand = True)
        scrollbar.pack(side = 'right', fill = 'y')