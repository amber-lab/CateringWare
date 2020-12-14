# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:35:54 2019

@author: L.A.B
"""

#LABEL FRAME COM LISTBOX E SCROLLBAR
class CateringPageScrollBarList(tk.Frame):
    def __init__(self, master, name, photo, color, destroyButton = False):
        super().__init__(master, borderwidth = 5, background = color)
        
        title = CateringPageTitleLabel(self, name, photo = photo, font = MEDIUM_FONT)
        
        
        if destroyButton:
            x_button = tk.Button(self, text = 'X', background = 'red')
            x_button.place(relx = 0.95, rely = 0, relwidth = 0.05, relheight = 0.2)
            x_button.bind('<ButtonRelease-1>', self.selfDestruction)
            title.place(relx = 0, rely = 0, relwidth = 0.95, relheight = 0.2)
        else:
            title.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.2)
        scrollbar = tk.Scrollbar(self, orient = 'vertical', background = color)
        
        self.listbox = tk.Listbox(self, yscrollcommand = scrollbar.set, selectforeground = 'black', selectbackground = color, font = MINI_FONT)
        
        scrollbar.config(command=self.listbox.yview)
        
        self.listbox.place(relx = 0, rely = 0.2, relwidth = 0.95, relheight = 0.8)
        scrollbar.place(relx = 0.95, rely = 0.2, relwidth = 0.05, relheight = 0.8)
        
    def selfDestruction(self, event):
        self.destroy()