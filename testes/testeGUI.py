# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Created on Wed Feb 19 14:32:53 2020

@author: L.A.B
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

exec(open('C:/Users/L.A.B/Desktop/CateringCalculator/APP_FRONTEND/CateringPage.py','r', encoding = 'utf-8').read())
exec(open('C:/Users/L.A.B/Desktop/CateringCalculator/APP_FRONTEND/CateringPageTitleLabel.py','r', encoding = 'utf-8').read())
exec(open('C:/Users/L.A.B/Desktop/CateringCalculator/APP_FRONTEND/CateringPageInputWidget.py','r', encoding = 'utf-8').read())
exec(open('C:/Users/L.A.B/Desktop/CateringCalculator/APP_FRONTEND/CateringPageMenuButton.py','r', encoding = 'utf-8').read())
exec(open('C:/Users/L.A.B/Desktop/CateringCalculator/APP_FRONTEND/CateringPageScrollBarFrame.py','r', encoding = 'utf-8').read())
exec(open('C:/Users/L.A.B/Desktop/CateringCalculator/APP_FRONTEND/CateringPagePopUpMensage.py','r', encoding = 'utf-8').read())
exec(open('C:/Users/L.A.B/Desktop/CateringCalculator/APP_FRONTEND/CateringPageMenuFrame.py','r', encoding = 'utf-8').read())


FONT = ('Bodoni MT Black', '18')
MINI_FONT = ('Baskerville Old Face', '14')

CINZA = '#757575'
VERMELHO = '#C00000'
AZUL = '#0070ff'
VERDE = '#2b9d00'
AMARELO = '#ea9d00'

BG_CINZA = Image.open('BG_CINZA_HD.png')
BG_VERMELHO = Image.open('BG_VERMELHO_HD.png')
BG_AZUL = Image.open('BG_AZUL_HD.png')
BG_VERDE = Image.open('BG_VERDE_HD.png')
BG_AMARELO = Image.open('BG_AMARELO_HD.png')

app = tk.Tk()

frame = tk.Frame(app)
frame.place(relheight = 1, relwidth = 1)

page = CateringPage(frame)

title_l = CateringPageTitleLabel(page, 'TitleLabel', BG_VERMELHO)

input_w1 = CateringPageInputWidget(page, 'InputWidget1', BG_AZUL)
input_w2 = CateringPageInputWidget(page, 'InputWidget2', BG_AZUL)

page.addWidget(title_l)
page.addWidget(input_w1)
page.showWidgets()
page.pack()

app.mainloop()
