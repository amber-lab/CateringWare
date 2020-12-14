#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Wed Nov 20 09:31:32 2019

@author: L.A.B
"""

#FRAME COM BUTAO E IMAGEM DE CATERINGMENUFRAME
class CateringPageMenuButton(tk.Frame):
    def __init__(self, master, image, text):
        tk.Frame.__init__(self, master)
        self.bg_img = ImageTk.PhotoImage(image)
        self.button = tk.Button(self, image = self.bg_img, text = text, font = FONT, compound = 'center')
        self.button.photo = self.bg_img
        self.button.pack()