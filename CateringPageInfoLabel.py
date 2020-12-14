# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Wed Mar 11 10:39:38 2020

@author: L.A.B
"""

FONT = ('Bodoni MT Black', '20')

class CateringPageInfoLabel(tk.Frame):
    def __init__(self, master, text, color, default_text = '', font = FONT):
        super().__init__(master, background = color, borderwidth = 5)
        
        self.title_label = tk.Label(self, text = text, background = color, justify = 'center', font = font)
        self.title_label.place(relx = 0, rely = 0, relwidth = 0.5, relheight = 1)
        
        self.info_label = tk.Label(self, text = default_text, font = font)
        self.info_label.place(relx = 0.5, rely = 0, relwidth = 0.5, relheight = 1)
        
    def setInfo(self, text):
        self.info_label.config(text = text)
        
    def get(self):
        return self.info_label.cget('text')