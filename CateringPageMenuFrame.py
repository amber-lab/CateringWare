# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:34:24 2019

@author: L.A.B
"""

#FRAME DO MENU
class CateringPageMenuFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        #LABEL MENU
        self.eira_button = CateringPageMenuButton(self, image = BG_CINZA, text = 'Tasca da Rosa\n\nCateringWare')
        self.eira_button.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.2)

        self.service_button = CateringPageMenuButton(self, image = BG_AZUL, text = 'Serviços')
        self.service_button.place(relx = 0, rely = 0.2, relwidth = 1, relheight = 0.2)

        self.workers_button = CateringPageMenuButton(self, image = BG_VERMELHO, text = 'Pessoal')
        self.workers_button.place(relx = 0, rely = 0.4, relwidth = 1, relheight = 0.2)

        self.menu_button = CateringPageMenuButton(self, image = BG_VERDE, text = 'Menus')
        self.menu_button.place(relx = 0, rely = 0.6, relwidth = 1, relheight = 0.2)

        self.products_button = CateringPageMenuButton(self, image = BG_AMARELO, text = 'Produtos')
        self.products_button.place(relx = 0, rely = 0.8, relwidth = 1, relheight = 0.2)