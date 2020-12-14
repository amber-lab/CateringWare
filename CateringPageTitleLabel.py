# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Created on Wed Feb 19 14:17:05 2020

@author: L.A.B
"""
FONT = ('Baskerville Old Face', '18')

class CateringPageTitleLabel(tk.Frame):
    def __init__(self, master, title, photo, font = FONT):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, text = title, image = photo, compound = 'center', font = font, relief = 'raised')
        self.label.photo = photo
        self.label.pack()