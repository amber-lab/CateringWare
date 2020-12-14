  # -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 17:18:32 2019

@author: L.A.B
"""

class CateringPagePopUpMensage(tk.Frame):
    def __init__(self, master, mensage):
        tk.Frame.__init__(self, master)
        
        image = ImageTk.PhotoImage(BG_CINZA)
        
        msg_label = tk.Label(self, text = mensage, font = FONT, image = image, compound = 'center', relief = 'raised')
        msg_label.photo = image
        msg_label.place(relx = 0, rely = 0, relheight = 0.5, relwidth = 1)
        
        self.button_yes = tk.Button(self, text = 'Sim', font = FONT, image = image, compound = 'center')
        self.button_yes.photo = image
        self.button_yes.place(relx = 0, rely = 0.5, relheight = 0.5, relwidth = 0.5)
        
        self.button_no = tk.Button(self, text = 'Não', font = FONT, image = image, compound = 'center')
        self.button_no.photo = image
        self.button_no.place(relx = 0.5, rely = 0.5, relheight = 0.5, relwidth = 0.5)
        