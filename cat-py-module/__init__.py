# -*- coding: utf-8 -*-
#!/usr/bin/env python

import tkinter as tk
import sqlite3
from tkinter import ttk
from PIL import Image, ImageTk
from datetime import datetime, date
import os

FONT = ('Baskerville Old Face', '16')
MEDIUM_FONT = ('Baskerville Old Face', '15')
MINI_FONT = ('Baskerville Old Face', '13')

CINZA = '#a9a9a9'
CINZA_ESCURO = '#878787'
VERMELHO = '#C00000'
AZUL = '#3193ca'
VERDE = '#2b9d00'
AMARELO = '#ea9d00'

BG_CINZA = Image.open('img\\cinza.png')
BG_VERMELHO = Image.open('img\\vermelho.png')
BG_AZUL = Image.open('img\\azul.png')
BG_VERDE = Image.open('img\\verde.png')
BG_AMARELO = Image.open('img\\amarelo.png')

class CateringAppetizersPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background = CINZA)
        
        self.photo = ImageTk.PhotoImage(BG_VERDE)
        
        self.main_frame = CateringPageScrollBarFrame(self, height = 1100, background = CINZA)
        self.main_frame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        title_bar = CateringPageTitleLabel(self.main_frame.interior, 'Gestão de Menus de Entradas', self.photo)
        title_bar.place(relx = 0.05, y = 50, relwidth = 0.9, height = 60)
        
        new_separator = CateringPageTitleLabel(self.main_frame.interior, 'Criar Novo Menu de Entradas', self.photo)
        new_separator.place(relx = 0.1, y = 130, relwidth = 0.8, height = 30)
        
        self.name_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome do Menu de Entradas', self.photo, default_text = 'Inserir Nome')
        self.name_entry.place(relx = 0.15, y = 180, relwidth = 0.7, height = 30)
        
        bar_prod_label = CateringPageTitleLabel(self.main_frame.interior, 'Entradas do Menu', self.photo)
        bar_prod_label.place(relx = 0.1, y = 230, relwidth = 0.8, height = 30)
        
        self.apt_prod_uni_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Entradas Unitárias', self.photo,  VERDE)
        self.apt_prod_uni_listbox.place(relx = 0.1, y = 280, relwidth = 0.3, height = 150)
        self.apt_prod_uni_listbox.listbox.bind('<Double-Button-1>', self.delFromAppetizers)
        
        clear_listbox_button = tk.Button(self.main_frame.interior, text = 'Limpar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        clear_listbox_button.bind('<ButtonRelease-1>', self.clearListbox)
        clear_listbox_button.place(relx = 0.45, y = 330, relwidth = 0.1, height = 50)
        
        self.apt_prod_div_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Entradas Divisiveis', self.photo,  VERDE)
        self.apt_prod_div_listbox.place(relx = 0.6, y = 280, relwidth = 0.3, height = 150)
        self.apt_prod_div_listbox.listbox.bind('<Double-Button-1>', self.delFromAppetizers)
        
        drinks_separator = CateringPageTitleLabel(self.main_frame.interior, 'Adicionar Entradas', self.photo)
        drinks_separator.place(relx = 0.1, y = 450, relwidth = 0.8, height = 30)
        
        self.uni_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Entradas Unitárias', self.photo, VERDE)
        self.uni_listbox.place(relx = 0.10, y = 500, relwidth = 0.35, height = 150)
        self.uni_listbox.listbox.bind('<Double-Button-1>', self.setToAppetizers)

        data = []
        for data_row in CateringDBManager.load(CateringDBManager.db_info['products'], 'entrada', where_column = 'TYPE', operator = "AND UNI = 'Unitário'"):
                data.append(data_row[1])
        for item in data:
            self.uni_listbox.listbox.insert('end', item)
        
        self.div_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Entradas Divisiveis', self.photo, VERDE)
        self.div_listbox.place(relx = 0.55, y = 500, relwidth = 0.35, height = 150)
        self.div_listbox.listbox.bind('<Double-Button-1>', self.setToAppetizers)
        
        data = []
        for data_row in CateringDBManager.load(CateringDBManager.db_info['products'], 'entrada', where_column = 'TYPE', operator = "AND UNI = 'Divisível'"):
                data.append(data_row[1])
        for item in data:
            self.div_listbox.listbox.insert('end', item)

        manager_separator = CateringPageTitleLabel(self.main_frame.interior, 'Gerir Menu Entradas', self.photo)
        manager_separator.place(relx = 0.1, y = 670, relwidth = 0.8, height = 30)
        
        self.manager_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome do Menu Entradas', self.photo, on_default = False)
        self.manager_entry.place(relx = 0.25, y = 720, relwidth = 0.5, height = 30)
        
        self.save_b = tk.Button(self.main_frame.interior, text = 'Gravar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.save_b.photo = self.photo
        self.save_b.bind('<ButtonRelease-1>', self.saveAppetizers)
        self.save_b.place(relx = 0.10, y = 980, relwidth = 0.20, height = 60)

        self.load_b = tk.Button(self.main_frame.interior, text = 'Carregar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.load_b.photo = self.photo
        self.load_b.bind('<ButtonRelease-1>', self.loadAppetizers)
        self.load_b.place(relx = 0.40, y = 980, relwidth = 0.20, height = 60)

        self.delete_b = tk.Button(self.main_frame.interior, text = 'Apagar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.delete_b.photo = self.photo
        self.delete_b.bind('<ButtonRelease-1>', self.deleteAppetizers)
        self.delete_b.place(relx = 0.70, y = 980, relwidth = 0.20, height = 60)
        
        self.status_bar = tk.Label(self, image = self.photo, compound = 'center', font = FONT, relief = 'sunken')
        self.status_bar.photo = self.photo
        self.status_bar.place(relx = 0, rely = 0.95, relwidth = 1, relheight = 0.05)
        
        self.after(500, self.c_update)
        
    def setToAppetizers(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        try:
            if value and 'list4' in str(widget):
                self.apt_prod_div_listbox.listbox.insert('end', value)
            else:
                self.apt_prod_uni_listbox.listbox.insert('end', value)
        except:pass
        
    def delFromAppetizers(self, event):
        widget = event.widget
        value = widget.curselection()
        try:
            widget.delete(value)
        except:pass
    
    def clearListbox(self, event):
        self.apt_prod_uni_listbox.listbox.delete(0, 'end')
        self.apt_prod_div_listbox.listbox.delete(0, 'end')
        
    def saveAppetizers(self, event):
        self.subFramesDestroy()
        try:
            name = self.name_entry.get()
        except CateringDefaultValue:
            self.setStatus('Impossível gravar Menu, dados em falta!')
            return False
        prod_list = list(self.apt_prod_uni_listbox.listbox.get(0, 'end'))
        prod_list.extend(list(self.apt_prod_div_listbox.listbox.get(0, 'end')))
        print("\n\n" + str(prod_list) + "\n\n")
        if not name:
            self.setStatus('Impossível gravar Menu, dados em falta!')
            return False
        print(name)
        try:
            self.obj = CateringAppetizersMenu(name)
            for product in prod_list:
                self.obj.setObjects(CateringProduct.load(product))
        except CateringExistingObject:
            self.setStatus('Já existe Menu com esse nome!')
            
            self.obj = CateringSet.load(name)
            
            out_prod_list = list(self.obj.products.get().values())
            
            for product in out_prod_list:
                if product.name not in prod_list:
                    self.obj.delObjects(product.name)
                    print("\n\n\nRemovido Product " + product.name + "\n\n\n")
            
            for product in prod_list:
                self.obj.setObjects(CateringProduct.load(product))
            
            self.popup = CateringPagePopUpMensage(self, mensage = "Menu já existe\nAlterar Informações?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)            
            
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            self.popup.button_yes.bind('<ButtonRelease-1>', self.overwrite)
            
            self.manager_entry.setEntryValue(name)
        else:
            try:
                self.obj.save()
            except sqlite3.OperationalError:
                self.setStatus('Impossível Gravar Menu, dados em falta!')
            else:
                self.setStatus('Menu Gravado Com Sucesso')
            
    def overwrite(self, event):
        try:
            self.obj.save(overwrite = True)
        except sqlite3.OperationalError:
            self.popup.destroy()
            self.setStatus('Impossível gravar Menu, dados em falta!')
        else:
            self.popup.destroy()
            self.setStatus('Menu Atualizado com Sucesso')
    
    def subFramesDestroy(self):
        try:
            self.popup.destroy()
        except AttributeError:
            pass
        try:
            self.scrollframe.destroy()
        except AttributeError:
            pass
    
    def eventDestroy(self, event):
        self.subFramesDestroy()

    def loadAppetizers(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            data = CateringSet.load(name, like = True, operator = "AND TYPE = 'appetizers'")
        except CateringObjectNotFound:
            self.setStatus('Não foram encontrados Menus com esse nome!')
        else:
            self.scrollframe = CateringPageScrollBarList(self.main_frame.interior, 'Menus Carregados', self.photo, VERDE, destroyButton = True)
            for row in data:
                self.scrollframe.listbox.insert('end', row[1])
            self.scrollframe.place(relx = 0.25, y = 770, relwidth = 0.50, height = 150)
            self.scrollframe.listbox.bind('<Double-Button-1>', self.setData)
            self.setStatus('Lista de Menus carregados com sucesso!')
    
    def setData(self, event):
        self.clearListbox(event)
        name = self.scrollframe.listbox.get(self.scrollframe.listbox.curselection())
        obj = CateringSet.load(name)
        self.name_entry.setEntryValue(name)
        for prod in obj.products.get().values():
            if prod.uni == 'Unitário':
                self.apt_prod_uni_listbox.listbox.insert('end', prod.name)
            else:
                self.apt_prod_div_listbox.listbox.insert('end', prod.name)
        self.manager_entry.setEntryValue(name)
        self.scrollframe.destroy()
        self.setStatus('Menu Carregado com sucesso')
    
    def deleteAppetizers(self, event):
        self.subFramesDestroy()
        try:
            name = self.manager_entry.get()
        except CateringDefaultValue:
            self.setStatus('Impossivel Remover Menu, dados em falta!')
        try:
            self.obj = CateringSet.load(name)
        except CateringObjectNotFound:
            self.setStatus('Impossivel Remover, Menu não encontrado!')
        else:
            self.popup = CateringPagePopUpMensage(self, mensage = "Remover Menu?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)
            
            self.popup.button_yes.bind('<ButtonRelease-1>', self.confirmed_delete)
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            
    def confirmed_delete(self, event):
        self.popup.destroy()
        self.obj.delete()
        self.setStatus('Menu Removido com sucesso!')
    
    def c_update(self):
        try:
            if self.counter:
                self.counter -= 1
            else:
                self.setStatus('')
                
        except AttributeError:
            pass
        self.after(500, self.c_update)
    
    def setStatus(self, mensage):
        self.status_bar.config(text = mensage)
        self.counter = 5
		
class CateringBarPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background = CINZA)
        
        self.photo = ImageTk.PhotoImage(BG_VERDE)
        
        self.main_frame = CateringPageScrollBarFrame(self, height = 1100, background = CINZA)
        self.main_frame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        title_bar = CateringPageTitleLabel(self.main_frame.interior, 'Gestão de Bars', self.photo)
        title_bar.place(relx = 0.05, y = 50, relwidth = 0.9, height = 60)
        
        new_separator = CateringPageTitleLabel(self.main_frame.interior, 'Criar Novo Bar', self.photo)
        new_separator.place(relx = 0.1, y = 130, relwidth = 0.8, height = 30)
        
        self.name_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome Bar', self.photo, default_text = 'Inserir Nome Bar')
        self.name_entry.place(relx = 0.15, y = 180, relwidth = 0.7, height = 30)
        
        bar_prod_label = CateringPageTitleLabel(self.main_frame.interior, 'Bebidas do Bar', self.photo)
        bar_prod_label.place(relx = 0.1, y = 230, relwidth = 0.8, height = 30)
        
        self.bar_prod_drinks_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Sumos / Água / Vinhos', self.photo,  VERDE)
        self.bar_prod_drinks_listbox.place(relx = 0.1, y = 280, relwidth = 0.3, height = 150)
        self.bar_prod_drinks_listbox.listbox.bind('<Double-Button-1>', self.delFromBar)
        
        clear_listbox_button = tk.Button(self.main_frame.interior, text = 'Limpar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        clear_listbox_button.bind('<ButtonRelease-1>', self.clearListbox)
        clear_listbox_button.place(relx = 0.45, y = 330, relwidth = 0.1, height = 50)
        
        self.bar_prod_white_drinks_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Bebidas Brancas', self.photo,  VERDE)
        self.bar_prod_white_drinks_listbox.place(relx = 0.6, y = 280, relwidth = 0.3, height = 150)
        self.bar_prod_white_drinks_listbox.listbox.bind('<Double-Button-1>', self.delFromBar)
        
        drinks_separator = CateringPageTitleLabel(self.main_frame.interior, 'Adicionar Bebidas', self.photo)
        drinks_separator.place(relx = 0.1, y = 450, relwidth = 0.8, height = 30)
        
        self.drinks_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Sumos / Água / Vinhos', self.photo, VERDE)
        self.drinks_listbox.place(relx = 0.10, y = 500, relwidth = 0.35, height = 150)
        self.drinks_listbox.listbox.bind('<Double-Button-1>', self.setToBar)

        data = []
        for data_row in CateringDBManager.load(CateringDBManager.db_info['products'], 'bebida', where_column = 'TYPE', operator = 'AND WHITE = 0'):
                data.append(data_row[1])
        for item in data:
            self.drinks_listbox.listbox.insert('end', item)
        
        self.white_drinks_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Bebidas Brancas', self.photo, VERDE)
        self.white_drinks_listbox.place(relx = 0.55, y = 500, relwidth = 0.35, height = 150)
        self.white_drinks_listbox.listbox.bind('<Double-Button-1>', self.setToBar)
        
        data = []
        for data_row in CateringDBManager.load(CateringDBManager.db_info['products'], 'bebida', where_column = 'TYPE', operator = 'AND WHITE = 1'):
                data.append(data_row[1])
        for item in data:
            self.white_drinks_listbox.listbox.insert('end', item)

        manager_separator = CateringPageTitleLabel(self.main_frame.interior, 'Gerir Bar', self.photo)
        manager_separator.place(relx = 0.1, y = 670, relwidth = 0.8, height = 30)
        
        self.manager_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome do Bar', self.photo, on_default = False)
        self.manager_entry.place(relx = 0.25, y = 720, relwidth = 0.5, height = 30)
        
        self.save_b = tk.Button(self.main_frame.interior, text = 'Gravar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.save_b.photo = self.photo
        self.save_b.bind('<ButtonRelease-1>', self.saveBar)
        self.save_b.place(relx = 0.10, y = 980, relwidth = 0.20, height = 60)

        self.load_b = tk.Button(self.main_frame.interior, text = 'Carregar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.load_b.photo = self.photo
        self.load_b.bind('<ButtonRelease-1>', self.loadBar)
        self.load_b.place(relx = 0.40, y = 980, relwidth = 0.20, height = 60)

        self.delete_b = tk.Button(self.main_frame.interior, text = 'Apagar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.delete_b.photo = self.photo
        self.delete_b.bind('<ButtonRelease-1>', self.deleteBar)
        self.delete_b.place(relx = 0.70, y = 980, relwidth = 0.20, height = 60)
        
        self.status_bar = tk.Label(self, image = self.photo, compound = 'center', font = FONT, relief = 'sunken')
        self.status_bar.photo = self.photo
        self.status_bar.place(relx = 0, rely = 0.95, relwidth = 1, relheight = 0.05)
        
        self.after(500, self.c_update)
        
    def setToBar(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        try:
            if value and 'list4' in str(widget):
                self.bar_prod_white_drinks_listbox.listbox.insert('end', value)
            else:
                self.bar_prod_drinks_listbox.listbox.insert('end', value)
        except:pass
        
    def delFromBar(self, event):
        widget = event.widget
        value = widget.curselection()
        try:
            widget.delete(value)
        except:pass
    
    def clearListbox(self, event):
        self.bar_prod_drinks_listbox.listbox.delete(0, 'end')
        self.bar_prod_white_drinks_listbox.listbox.delete(0, 'end')
        
    def saveBar(self, event):
        self.subFramesDestroy()
        try:
            name = self.name_entry.get()
        except CateringDefaultValue:
            self.setStatus('Impossível Gravar Bar, dados em falta!')
            return False
        prod_list = list(self.bar_prod_drinks_listbox.listbox.get(0, 'end'))
        prod_list.extend(list(self.bar_prod_white_drinks_listbox.listbox.get(0, 'end')))
        print("\n\n" + str(prod_list) + "\n\n")
        if not name:
            self.setStatus('Impossível Gravar Bar, dados em falta!')
            return False
        print(name)
        try:
            self.obj = CateringBar(name)
            for product in prod_list:
                self.obj.setObjects(CateringProduct.load(product))
        except CateringExistingObject:
            self.setStatus('Já existe Bar com esse nome!')
            
            self.obj = CateringSet.load(name)
            
            out_prod_list = list(self.obj.products.get().values())
            
            for product in out_prod_list:
                if product.name not in prod_list:
                    self.obj.delObjects(product.name)
                    print("\n\n\nRemovido Product " + product.name + "\n\n\n")
            
            for product in prod_list:
                self.obj.setObjects(CateringProduct.load(product))
            
            self.popup = CateringPagePopUpMensage(self, mensage = "Bar já existe\nAlterar informação?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)            
            
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            self.popup.button_yes.bind('<ButtonRelease-1>', self.overwrite)
            
            self.manager_entry.setEntryValue(name)
        else:
            try:
                self.obj.save()
            except sqlite3.OperationalError:
                self.setStatus('Impossível Gravar Bar, dados em falta')
            else:
                self.setStatus('Bar Gravado Com Sucesso')
            
    def overwrite(self, event):
        try:
            self.obj.save(overwrite = True)
        except sqlite3.OperationalError:
            self.popup.destroy()
            self.setStatus('Impossível Atualizar Menu, dados em falta')
        else:
            self.popup.destroy()
            self.setStatus('Produto Atualizado com Sucesso')
    
    def subFramesDestroy(self):
        try:
            self.popup.destroy()
        except AttributeError:
            pass
        try:
            self.scrollframe.destroy()
        except AttributeError:
            pass
    
    def eventDestroy(self, event):
        self.subFramesDestroy()

    def loadBar(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            data = CateringSet.load(name, like = True, operator = "AND TYPE = 'bar'")
        except CateringObjectNotFound:
            self.setStatus('Não foram encontrados bars com esse nome!')
        else:
            self.scrollframe = CateringPageScrollBarList(self.main_frame.interior, 'Bars Carregados', self.photo, VERDE, destroyButton = True)
            for row in data:
                self.scrollframe.listbox.insert('end', row[1])
            self.scrollframe.place(relx = 0.25, y = 770, relwidth = 0.50, height = 150)
            self.scrollframe.listbox.bind('<Double-Button-1>', self.setData)
            self.setStatus('Lista de Bars carregados com sucesso!')
    
    def setData(self, event):
        self.clearListbox(event)
        name = self.scrollframe.listbox.get(self.scrollframe.listbox.curselection())
        obj = CateringSet.load(name)
        self.name_entry.setEntryValue(name)
        for prod in obj.products.get().values():
            if prod.white:
                self.bar_prod_white_drinks_listbox.listbox.insert('end', prod.name)
            else:
                self.bar_prod_drinks_listbox.listbox.insert('end', prod.name)
        self.manager_entry.setEntryValue(name)
        self.scrollframe.destroy()
        self.setStatus('Bar Carregado com sucesso!')
    
    def deleteBar(self, event):
        self.subFramesDestroy()
        try:
            name = self.name_entry.get()
        except CateringDefaultValue:
            self.setStatus('Impossivel Remover Bar, dados em falta!')
            return False
        try:
            self.obj = CateringSet.load(name)
        except CateringObjectNotFound:
            self.setStatus('Impossivel Remover, Bar não encontrado!')
        else:
            self.popup = CateringPagePopUpMensage(self, mensage = "Remover Produto?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)
            
            self.popup.button_yes.bind('<ButtonRelease-1>', self.confirmed_delete)
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            
    def confirmed_delete(self, event):
        self.popup.destroy()
        self.obj.delete()
        self.setStatus('Bar removido com sucesso!')
    
    def c_update(self):
        try:
            if self.counter:
                self.counter -= 1
            else:
                self.setStatus('')
                
        except AttributeError:
            pass
        self.after(500, self.c_update)
    
    def setStatus(self, mensage):
        self.status_bar.config(text = mensage)
        self.counter = 5
		
class CateringDBManager():
    def save(db_info, data):
        conn = sqlite3.connect('CateringDB.db')
        query = "INSERT INTO {t} ({c}) VALUES {v}".format(t = db_info['table'], c = ', '.join(db_info['columns']), v = data)
        print(query)
        conn.execute(query)
        conn.commit()
        conn.close()
        return True
        
    def load(db_info, name, like = False, id_list = False, where_column = '', operator = ''):
        conn = sqlite3.connect('CateringDB.db')
        query = ''
        if like and where_column:
            query = "SELECT {c} FROM {t} WHERE {wc} LIKE '{n}%'".format(c = ', '.join(db_info['columns']), t = db_info['table'], n = name, wc = where_column)
        elif like:
            query = "SELECT {c} FROM {t} WHERE NAME LIKE '{n}%'".format(c = ', '.join(db_info['columns']), t = db_info['table'], n = name)
        elif where_column:
            query = "SELECT {c} FROM {t} WHERE {wc} = '{n}'".format(c = ', '.join(db_info['columns']), t = db_info['table'], n = name, wc = where_column)
        elif isinstance(name, int):
            query = "SELECT {c} FROM {t} WHERE ID = {n}".format(c = ', '.join(db_info['columns']), t = db_info['table'], n = name)
        elif isinstance(name, str):
            query = "SELECT {c} FROM {t} WHERE NAME = '{n}'".format(c = ', '.join(db_info['columns']), t = db_info['table'], n = name)
        if operator:
            query += " {}".format(operator)
        print(query)
        cursor = conn.execute(query)
        if like or where_column or id_list:
            data = cursor.fetchall()
        else:
            data = cursor.fetchone()
        conn.commit()
        conn.close()
        if data:
            return data
        else:
            raise CateringObjectNotFound

    def delete(db_info, data, operator = ''):
        conn = sqlite3.connect('CateringDB.db')
        query = "DELETE FROM {t} WHERE ID = {i}".format(t = db_info['table'], i = data[0])
        if operator:
            query += ' {}'.format(operator)
        print(query)
        conn.execute(query)
        conn.commit()
        conn.close()
        return True
        
    def update(db_info, data, operator = ''):
        conn = sqlite3.connect('CateringDB.db')
        data_str = ''
        for n in range(len(db_info['columns']) - 1):
            if data_str:
                data_str += ', '
            if isinstance(data[n+1], str):
                data_str += db_info['columns'][n+1] + " = '" + str(data[n+1]) + "'"
            else:
                data_str += db_info['columns'][n+1] + ' = ' + str(data[n+1])
        query = "UPDATE {t} SET {d} WHERE ID = {i}".format(t = db_info['table'], d = data_str, i = data[0])
        if operator:
            query += ' {}'.format(operator)
        print(query)
        conn.execute(query)
        conn.commit()
        conn.close()
        return True
        
    def getMaxID(table):
        conn = sqlite3.connect('CateringDB.db')
        query = "SELECT MAX(ID) FROM {t}".format(t = table)
        cursor = conn.execute(query)
        maxID = cursor.fetchone()[0]
        if maxID:
            return maxID + 1
        else:
            return 1
    
CateringDBManager.db_info = {'products' : {'table' : 'PRODUCTS', 'columns' : ('ID', 'NAME', 'TYPE', 'COST', 'PRICE', 'LITER', 'WHITE', 'UNI', 'UNI_N')},
                            'sets' : {'table' : 'SETS', 'columns' : ('ID', 'NAME', 'TYPE')},
                            'setsproducts' : {'table' : 'SETSPRODUCTS', 'columns' : ('ID', 'PRODUCTID', 'HOURS')},
                            'workers' : {'table' : 'WORKERS' , 'columns' : ('ID', 'NAME', 'COST', 'TYPE')},
                            'services' : {'table' : 'SERVICES', 'columns' : ('ID', 'NAME', 'DATE', 'NUMBER', 'STATUS', 'CUPS', 'TABLES_TYPE', 'EXTRA_TABLES', 'TRIPS', 'DISTANCE', 'SITE', 'MENU', 'BAR', 'APPETIZERS', 'DESSERTS', 'TEAM', 'APT_L', 'DST_L')}}

class CateringDessertsPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background = CINZA)
        
        self.photo = ImageTk.PhotoImage(BG_VERDE)
        
        self.main_frame = CateringPageScrollBarFrame(self, height = 1100, background = CINZA)
        self.main_frame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        title_bar = CateringPageTitleLabel(self.main_frame.interior, 'Gestão de Menus de Sobremesas', self.photo)
        title_bar.place(relx = 0.05, y = 50, relwidth = 0.9, height = 60)
        
        new_separator = CateringPageTitleLabel(self.main_frame.interior, 'Criar Novo Menu de Sobremesas', self.photo)
        new_separator.place(relx = 0.1, y = 130, relwidth = 0.8, height = 30)
        
        self.name_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome do Menu de Sobremesas', self.photo, default_text = 'Inserir Nome')
        self.name_entry.place(relx = 0.15, y = 180, relwidth = 0.7, height = 30)
        
        bar_prod_label = CateringPageTitleLabel(self.main_frame.interior, 'Sobremesas do Menu', self.photo)
        bar_prod_label.place(relx = 0.1, y = 230, relwidth = 0.8, height = 30)
        
        self.dess_prod_uni_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Sobremesas Unitárias', self.photo,  VERDE)
        self.dess_prod_uni_listbox.place(relx = 0.1, y = 280, relwidth = 0.3, height = 150)
        self.dess_prod_uni_listbox.listbox.bind('<Double-Button-1>', self.delFromDesserts)
        
        clear_listbox_button = tk.Button(self.main_frame.interior, text = 'Limpar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        clear_listbox_button.bind('<ButtonRelease-1>', self.clearListbox)
        clear_listbox_button.place(relx = 0.45, y = 330, relwidth = 0.1, height = 50)
        
        self.dess_prod_div_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Sobremesas Divisiveis', self.photo,  VERDE)
        self.dess_prod_div_listbox.place(relx = 0.6, y = 280, relwidth = 0.3, height = 150)
        self.dess_prod_div_listbox.listbox.bind('<Double-Button-1>', self.delFromDesserts)
        
        drinks_separator = CateringPageTitleLabel(self.main_frame.interior, 'Adicionar Sobremesas', self.photo)
        drinks_separator.place(relx = 0.1, y = 450, relwidth = 0.8, height = 30)
        
        self.uni_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Sobremesas Unitárias', self.photo, VERDE)
        self.uni_listbox.place(relx = 0.10, y = 500, relwidth = 0.35, height = 150)
        self.uni_listbox.listbox.bind('<Double-Button-1>', self.setToDesserts)

        data = []
        for data_row in CateringDBManager.load(CateringDBManager.db_info['products'], 'sobremesa', where_column = 'TYPE', operator = "AND UNI = 'Unitário'"):
                data.append(data_row[1])
        for item in data:
            self.uni_listbox.listbox.insert('end', item)
        
        self.div_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Sobremesas Divisiveis', self.photo, VERDE)
        self.div_listbox.place(relx = 0.55, y = 500, relwidth = 0.35, height = 150)
        self.div_listbox.listbox.bind('<Double-Button-1>', self.setToDesserts)
        
        data = []
        for data_row in CateringDBManager.load(CateringDBManager.db_info['products'], 'sobremesa', where_column = 'TYPE', operator = "AND UNI = 'Divisível'"):
                data.append(data_row[1])
        for item in data:
            self.div_listbox.listbox.insert('end', item)

        manager_separator = CateringPageTitleLabel(self.main_frame.interior, 'Gerir Menu Sobremesas', self.photo)
        manager_separator.place(relx = 0.1, y = 670, relwidth = 0.8, height = 30)
        
        self.manager_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome do Menu Sobremesas', self.photo, on_default = False)
        self.manager_entry.place(relx = 0.25, y = 720, relwidth = 0.5, height = 30)
        
        self.save_b = tk.Button(self.main_frame.interior, text = 'Gravar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.save_b.photo = self.photo
        self.save_b.bind('<ButtonRelease-1>', self.saveDesserts)
        self.save_b.place(relx = 0.10, y = 980, relwidth = 0.20, height = 60)

        self.load_b = tk.Button(self.main_frame.interior, text = 'Carregar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.load_b.photo = self.photo
        self.load_b.bind('<ButtonRelease-1>', self.loadDesserts)
        self.load_b.place(relx = 0.40, y = 980, relwidth = 0.20, height = 60)

        self.delete_b = tk.Button(self.main_frame.interior, text = 'Apagar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.delete_b.photo = self.photo
        self.delete_b.bind('<ButtonRelease-1>', self.deleteDesserts)
        self.delete_b.place(relx = 0.70, y = 980, relwidth = 0.20, height = 60)
        
        self.status_bar = tk.Label(self, image = self.photo, compound = 'center', font = FONT, relief = 'sunken')
        self.status_bar.photo = self.photo
        self.status_bar.place(relx = 0, rely = 0.95, relwidth = 1, relheight = 0.05)
        
        self.after(500, self.c_update)
        
    def setToDesserts(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        try:
            if value and 'list4' in str(widget):
                self.dess_prod_div_listbox.listbox.insert('end', value)
            else:
                self.dess_prod_uni_listbox.listbox.insert('end', value)
        except:pass
        
    def delFromDesserts(self, event):
        widget = event.widget
        value = widget.curselection()
        try:
            widget.delete(value)
        except:pass
    
    def clearListbox(self, event):
        self.dess_prod_uni_listbox.listbox.delete(0, 'end')
        self.dess_prod_div_listbox.listbox.delete(0, 'end')
        
    def saveDesserts(self, event):
        self.subFramesDestroy()
        try:
            name = self.name_entry.get()
        except CateringDefaultValue:
            self.setStatus('Impossível Gravar Menu, dados em falta!')
            return False
        prod_list = list(self.dess_prod_uni_listbox.listbox.get(0, 'end'))
        prod_list.extend(list(self.dess_prod_div_listbox.listbox.get(0, 'end')))
        print("\n\n" + str(prod_list) + "\n\n")
        if not name:
            self.setStatus('Impossível Gravar Menu, dados em falta!')
            return False
        print(name)
        try:
            self.obj = CateringDessertsMenu(name)
            for product in prod_list:
                self.obj.setObjects(CateringProduct.load(product))
        except CateringExistingObject:
            self.setStatus('Já existe Menu com esse nome!')
            
            self.obj = CateringSet.load(name)
            
            out_prod_list = list(self.obj.products.get().values())
            
            for product in out_prod_list:
                if product.name not in prod_list:
                    self.obj.delObjects(product.name)
                    print("\n\n\nRemovido Product " + product.name + "\n\n\n")
            
            for product in prod_list:
                self.obj.setObjects(CateringProduct.load(product))
            
            self.popup = CateringPagePopUpMensage(self, mensage = "Menu já existe\nAlterar informação?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)            
            
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            self.popup.button_yes.bind('<ButtonRelease-1>', self.overwrite)
            
            self.manager_entry.setEntryValue(name)
        else:
            try:
                self.obj.save()
            except sqlite3.OperationalError:
                self.setStatus('Impossível Gravar Menu, dados em falta!')
            else:
                self.setStatus('Menu Gravado Com Sucesso')
            
    def overwrite(self, event):
        try:
            self.obj.save(overwrite = True)
        except sqlite3.OperationalError:
            self.popup.destroy()
            self.setStatus('Impossível Atualizar Menu, dados em falta!')
        else:
            self.popup.destroy()
            self.setStatus('Menu Atualizado com Sucesso!')
    
    def subFramesDestroy(self):
        try:
            self.popup.destroy()
        except AttributeError:
            pass
        try:
            self.scrollframe.destroy()
        except AttributeError:
            pass
    
    def eventDestroy(self, event):
        self.subFramesDestroy()

    def loadDesserts(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            data = CateringSet.load(name, like = True, operator = "AND TYPE = 'desserts'")
        except CateringObjectNotFound:
            self.setStatus('Não foram encontrados Menus com esse nome!')
        else:
            self.scrollframe = CateringPageScrollBarList(self.main_frame.interior, 'Menus Carregados', self.photo, VERDE, destroyButton = True)
            for row in data:
                self.scrollframe.listbox.insert('end', row[1])
            self.scrollframe.place(relx = 0.25, y = 770, relwidth = 0.50, height = 150)
            self.scrollframe.listbox.bind('<Double-Button-1>', self.setData)
            self.setStatus('Lista de Menus carregada com sucesso!')
    
    def setData(self, event):
        self.clearListbox(event)
        name = self.scrollframe.listbox.get(self.scrollframe.listbox.curselection())
        obj = CateringSet.load(name)
        self.name_entry.setEntryValue(name)
        for prod in obj.products.get().values():
            if prod.uni == 'Unitário':
                self.dess_prod_uni_listbox.listbox.insert('end', prod.name)
            else:
                self.dess_prod_div_listbox.listbox.insert('end', prod.name)
        self.manager_entry.setEntryValue(name)
        self.scrollframe.destroy()
        self.setStatus('Menu Carregado com sucesso!')
    
    def deleteDesserts(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            self.obj = CateringSet.load(name)
        except CateringObjectNotFound:
            self.setStatus('Impossível Remover, Menu não encontrado!')
        else:
            self.popup = CateringPagePopUpMensage(self, mensage = "Remover Menu?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)
            
            self.popup.button_yes.bind('<ButtonRelease-1>', self.confirmed_delete)
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            
    def confirmed_delete(self, event):
        self.popup.destroy()
        self.obj.delete()
        self.setStatus('Menu removido com sucesso!')
    
    def c_update(self):
        try:
            if self.counter:
                self.counter -= 1
            else:
                self.setStatus('')
                
        except AttributeError:
            pass
        self.after(500, self.c_update)
    
    def setStatus(self, mensage):
        self.status_bar.config(text = mensage)
        self.counter = 5

class CateringExistingObject(Exception):
    pass

class CateringObjectNotFound(Exception):
    pass

class CateringDateError(Exception):
    pass

class CateringDefaultValue(Exception):
    pass

class CateringCupsNumberError(Exception):
    pass

class CateringHomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.photo = ImageTk.PhotoImage(BG_CINZA)
        
        self.img = Image.open('img\\home.png')
        self.img_copy = self.img.copy()
        
        self.bg_photo = ImageTk.PhotoImage(self.img)
        
        self.background = tk.Label(self, image = self.bg_photo)
        self.background.photo = self.bg_photo
        self.background.bind('<Configure>', self.imageResize)
        self.background.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)
        
        title = CateringPageTitleLabel(self, 'CateringWare Tasca da Rosa', self.photo)
        title.place(relx = 0.05, y = 50, relwidth = 0.9, height = 60)
        services_separator = CateringPageTitleLabel(self, 'Proximos Serviços', self.photo)
        services_separator.place(relx = 0.1, y = 130, relwidth = 0.8, height = 30)
        
        try:
            today_date = str(date.today())
            data = CateringService.load('', like = True, operator = "AND DATE > {} AND STATUS = 'aberto'".format(today_date))
            dates = []
            for row in data:
                data = row[2]
                if data not in dates:
                    dates.append(row[2])
            dates = sorted(dates, key = lambda d: tuple(map(int, d.split('-'))))
            dates = dates[:5]
            objs = []
            for dat in dates:
                data = CateringDBManager.load(CateringDBManager.db_info['services'], name = dat, where_column = 'DATE')
                if isinstance(data, list):
                    for dat in data:
                        objs.append((dat[1], dat[2], dat[10]))
                else:
                    obj.append(data[1], data[2], data[10])
            y = 180
            if objs:
                for obj in objs:
                    info = CateringPageInfoLabel(self, obj[0], CINZA_ESCURO, default_text = str(obj[1] + " / " + obj[2]), font = MEDIUM_FONT)
                    info.place(relx = 0.15, y = y, relwidth = 0.7, height = 30)
                    y += 50
        except CateringObjectNotFound:
            label = tk.Label(self, text = 'Proximos serviços serão apresentados aqui.', background = CINZA_ESCURO, font = MEDIUM_FONT)
            label.place(relx = 0.15, y = 180, relwidth = 0.7, height = 100)
            
    def imageResize(self, event):
        width = event.width
        height = event.height
        
        self.img = self.img_copy.resize((width, height), Image.ANTIALIAS)
        
        self.bg_photo = ImageTk.PhotoImage(self.img)
        self.background.config(image = self.bg_photo)


class CateringItems:
    def __init__(self, name):
        self.name = name
        self.items = {self.name : dict()}       
        
    def add(self, item, value = 1):
        if issubclass(type(item), CateringProduct) or issubclass(type(item), CateringWorker):
            self.items[self.name][item.name] = item
        elif issubclass(type(item), CateringItems):
            self.items[self.name][item.name] = item.items[item.name]
        else:
            self.items[self.name][item] = value
    def rem(self, item):
        if item in self.items[self.name].keys():
            self.items[self.name].pop(item)
        if isinstance(item, CateringItems):
            if item in self.items[self.name].keys():
                self.items[self.name].pop(item.name)

    def get(self, name = '', full = 0):
        if name:
            try:
                return self.items[self.name][name]
            except NameError:
                print("Objecto não existe em {n}".format(n = self.name))
        if full:
            return self.items
        else:
            return self.items[self.name]

class CateringMenuPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, background = CINZA)
        
        self.photo = ImageTk.PhotoImage(BG_VERDE)

        self.main_frame = CateringPageScrollBarFrame(self, height = 1300, background = CINZA)
        self.main_frame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        title_bar = CateringPageTitleLabel(self.main_frame.interior, 'Gestão de Menus', self.photo)
        title_bar.place(relx = 0.05, y = 50, relwidth = 0.9, height = 60)
        
        new_separator = CateringPageTitleLabel(self.main_frame.interior, 'Criar Novo Menu', self.photo)
        new_separator.place(relx = 0.1, y = 130, relwidth = 0.8, height = 30)
        
        self.name_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome Menu', self.photo, default_text = 'Inserir Nome Menu')
        self.name_entry.place(relx = 0.15, y = 180, relwidth = 0.7, height = 30)
        
        menu_prod_label = CateringPageTitleLabel(self.main_frame.interior, 'Produtos do Menu', self.photo)
        menu_prod_label.place(relx = 0.1, y = 230, relwidth = 0.8, height = 30)
        
        self.menu_prod_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Pratos do Menu', self.photo,  VERDE)
        self.menu_prod_listbox.place(relx = 0.1, y = 280, relwidth = 0.3, height = 150)
        self.menu_prod_listbox.listbox.bind('<Double-Button-1>', self.delFromMenu)
        
        clear_listbox_button = tk.Button(self.main_frame.interior, text = 'Limpar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        clear_listbox_button.bind('<ButtonRelease-1>', self.clearListbox)
        clear_listbox_button.place(relx = 0.45, y = 330, relwidth = 0.1, height = 50)
        
        self.menu_drinks_prod_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Bebidas do Menu', self.photo,  VERDE)
        self.menu_drinks_prod_listbox.place(relx = 0.6, y = 280, relwidth = 0.3, height = 150)
        self.menu_drinks_prod_listbox.listbox.bind('<Double-Button-1>', self.delFromMenu)
        
        dishes_separator = CateringPageTitleLabel(self.main_frame.interior, 'Adicionar Pratos', self.photo)
        dishes_separator.place(relx = 0.1, y = 450, relwidth = 0.8, height = 30)
        
        self.menu_soup_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Pratos de Sopa', self.photo, VERDE)
        self.menu_soup_listbox.place(relx = 0.10, y = 500, relwidth = 0.25, height = 150)
        self.menu_soup_listbox.listbox.bind('<Double-Button-1>', self.setToMenu)
        
        data = []
        for data_row in CateringDBManager.load(CateringDBManager.db_info['products'], 'sopa', where_column = 'TYPE'):
                data.append(data_row[1])
        for item in data:
            self.menu_soup_listbox.listbox.insert('end', item)
        
        self.menu_meat_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Pratos de Carne', self.photo, VERDE)
        self.menu_meat_listbox.place(relx = 0.375, y = 500, relwidth = 0.25, height = 150)
        self.menu_meat_listbox.listbox.bind('<Double-Button-1>', self.setToMenu)
        
        data = []
        for data_row in CateringDBManager.load(CateringDBManager.db_info['products'], 'carne', where_column = 'TYPE'):
                data.append(data_row[1])
        for item in data:
            self.menu_meat_listbox.listbox.insert('end', item)
        
        self.menu_fish_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Pratos de Peixe', self.photo, VERDE)
        self.menu_fish_listbox.place(relx = 0.65, y = 500, relwidth = 0.25, height = 150)
        self.menu_fish_listbox.listbox.bind('<Double-Button-1>', self.setToMenu)
        
        data = []
        for data_row in CateringDBManager.load(CateringDBManager.db_info['products'], 'peixe', where_column = 'TYPE'):
                data.append(data_row[1])
        for item in data:
            self.menu_fish_listbox.listbox.insert('end', item)

        drinks_separator = CateringPageTitleLabel(self.main_frame.interior, 'Adicionar Bebidas', self.photo)
        drinks_separator.place(relx = 0.1, y = 670, relwidth = 0.8, height = 30)
        
        self.menu_drinks_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Bebidas', self.photo, VERDE)
        self.menu_drinks_listbox.place(relx = 0.25, y = 720, relwidth = 0.5, height = 150)
        self.menu_drinks_listbox.listbox.bind('<Double-Button-1>', self.setToMenu)

        data = []
        for item in CateringDBManager.load(CateringDBManager.db_info['products'], 'bebida', where_column = 'TYPE', operator = 'AND WHITE = 0'):
            data.append(item[1])
        for item in data:
            self.menu_drinks_listbox.listbox.insert('end', item)
 
        manager_separator = CateringPageTitleLabel(self.main_frame.interior, 'Gerir Menu', self.photo)
        manager_separator.place(relx = 0.1, y = 890, relwidth = 0.8, height = 30)
        
        self.manager_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome do Menu', self.photo, on_default = False)
        self.manager_entry.place(relx = 0.25, y = 940, relwidth = 0.5, height = 30)
        
        self.save_b = tk.Button(self.main_frame.interior, text = 'Gravar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.save_b.photo = self.photo
        self.save_b.bind('<ButtonRelease-1>', self.saveMenu)
        self.save_b.place(relx = 0.10, y = 1180, relwidth = 0.20, height = 60)

        self.load_b = tk.Button(self.main_frame.interior, text = 'Carregar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.load_b.photo = self.photo
        self.load_b.bind('<ButtonRelease-1>', self.loadMenu)
        self.load_b.place(relx = 0.40, y = 1180, relwidth = 0.20, height = 60)

        self.delete_b = tk.Button(self.main_frame.interior, text = 'Apagar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.delete_b.photo = self.photo
        self.delete_b.bind('<ButtonRelease-1>', self.deleteMenu)
        self.delete_b.place(relx = 0.70, y = 1180, relwidth = 0.20, height = 60)
        
        self.status_bar = tk.Label(self, image = self.photo, compound = 'center', font = FONT, relief = 'sunken')
        self.status_bar.photo = self.photo
        self.status_bar.place(relx = 0, rely = 0.95, relwidth = 1, relheight = 0.05)
        
        self.after(500, self.c_update)
        
    def setToMenu(self, event):
        widget = event.widget
        selection = widget.curselection()[0]
        value = widget.get(selection)
        try:
            if value and 'list6' in str(widget):
                self.menu_drinks_prod_listbox.listbox.insert('end', value)
            else:
                self.menu_prod_listbox.listbox.insert('end', value)
        except:pass
        
    def delFromMenu(self, event):
        widget = event.widget
        value = widget.curselection()
        try:
            if value and 'list2' in str(widget):
                self.menu_drinks_prod_listbox.listbox.delete(value)
            else:
                self.menu_prod_listbox.listbox.delete(value)
        except:pass
    
    def clearListbox(self, event):
        self.menu_drinks_prod_listbox.listbox.delete(0, 'end')
        self.menu_prod_listbox.listbox.delete(0, 'end')
        
    def saveMenu(self, event):
        self.subFramesDestroy()
        try:
            name = self.name_entry.get()
        except CateringDefaultValue:
            self.setStatus('Impossível Gravar Menu, dados em falta!')
            return False
        prod_list = list(self.menu_prod_listbox.listbox.get(0, 'end'))
        prod_list.extend(list(self.menu_drinks_prod_listbox.listbox.get(0, 'end')))
        print("\n\n" + str(prod_list) + "\n\n")
        if not name:
            self.setStatus('Impossível Gravar Menu, dados em falta!')
            return False
        print(name)
        try:
            self.obj = CateringCourseMenu(name)
            for product in prod_list:
                self.obj.setObjects(CateringProduct.load(product))
        except CateringExistingObject:
            self.setStatus('Já existe Menu com esse nome!')
            self.obj = CateringCourseMenu.load(name)
            out_prod_list = list(self.obj.products.get().values())
            for product in out_prod_list:
                if product.name not in prod_list:
                    self.obj.delObjects(product.name)
                    print("\n\n\nRemovido Product " + product.name + "\n\n\n")
            for product in prod_list:
                self.obj.setObjects(CateringProduct.load(product))
            self.popup = CateringPagePopUpMensage(self, mensage = "Menu já existe\nAlterar informação?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)            
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            self.popup.button_yes.bind('<ButtonRelease-1>', self.overwrite)
            self.manager_entry.setEntryValue(name)
        else:
            try:
                self.obj.save()
            except sqlite3.OperationalError:
                self.setStatus('Impossível Gravar Menu, dados em falta!')
            else:
                self.setStatus('Menu Gravado Com Sucesso!')
            
    def overwrite(self, event):
        try:
            self.obj.save(overwrite = True)
        except sqlite3.OperationalError:
            self.popup.destroy()
            self.setStatus('Impossível Atualizar Menu, dados em falta!')
        else:
            self.popup.destroy()
            self.setStatus('Menu Atualizado com Sucesso')
    
    def subFramesDestroy(self):
        try:
            self.popup.destroy()
        except AttributeError:
            pass
        try:
            self.scrollframe.destroy()
        except AttributeError:
            pass
    
    def eventDestroy(self, event):
        self.subFramesDestroy()

    def loadMenu(self, event):
        self.clearListbox(event)
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            data = CateringSet.load(name, like = True, operator = "AND TYPE = 'course'")
        except CateringObjectNotFound:
            self.setStatus('Não foram encontrados Menus com esse nome!')
        else:
            self.scrollframe = CateringPageScrollBarList(self.main_frame.interior, 'Menus Carregados', self.photo, VERDE, destroyButton = True)
            for row in data:
                self.scrollframe.listbox.insert('end', row[1])
            self.scrollframe.place(relx = 0.25, y = 1000, relwidth = 0.50, height = 150)
            self.scrollframe.listbox.bind('<Double-Button-1>', self.setData)
            self.setStatus('Lista de Menus carregada com sucesso')
    
    def setData(self, event):
        name = self.scrollframe.listbox.get('active')
        obj = CateringSet.load(name)
        self.name_entry.setEntryValue(name)
        for prod in obj.products.get().values():
            if prod.type == 'bebida':
                self.menu_drinks_prod_listbox.listbox.insert('end', prod.name)
            else:
                self.menu_prod_listbox.listbox.insert('end', prod.name)
        self.manager_entry.setEntryValue(name)
        self.scrollframe.destroy()
        self.setStatus('Menu Carregado com sucesso')
    
    def deleteMenu(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            self.obj = CateringSet.load(name)
        except CateringObjectNotFound:
            self.setStatus('Impossível Remover, Menu não encontrado!')
        else:
            self.popup = CateringPagePopUpMensage(self, mensage = "Remover Produto?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)
            
            self.popup.button_yes.bind('<ButtonRelease-1>', self.confirmed_delete)
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            
    def confirmed_delete(self, event):
        self.popup.destroy()
        self.obj.delete()
        self.setStatus('Menu removido com sucesso!')
    
    def c_update(self):
        try:
            if self.counter:
                self.counter -= 1
            else:
                self.setStatus('')
                
        except AttributeError:
            pass
        self.after(500, self.c_update)
    
    def setStatus(self, mensage):
        self.status_bar.config(text = mensage)
        self.counter = 5



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

class CateringPageLabeledDateEntry(tk.Frame):
    def __init__(self, master, text, photo):
        tk.Frame.__init__(self, master, background = CINZA)
        
        date = datetime.now()
        
        self.photo = photo
        self.label = tk.Label(self, text = text, image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        self.label.photo = self.photo
        self.label.place(relx = 0, rely = 0, relwidth = 0.6, relheight = 1)
        
        self.day_entry_var = tk.StringVar()
        self.month_entry_var = tk.StringVar()
        self.year_entry_var = tk.StringVar()
        
        self.day_entry = tk.Entry(self, textvariable = self.day_entry_var, font = MINI_FONT, justify = 'center')
        self.day_entry.insert(0, date.day)
        self.month_entry = tk.Entry(self, textvariable = self.month_entry_var, font = MINI_FONT, justify = 'center')
        self.month_entry.insert(0, date.month)
        self.year_entry = tk.Entry(self, textvariable = self.year_entry_var, font = MINI_FONT, justify = 'center')
        self.year_entry.insert(0, date.year)
        
        self.d_label = tk.Label(self, text = 'D', image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        self.m_label = tk.Label(self, text = 'M', image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        self.y_label = tk.Label(self, text = 'A', image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        
        self.d_label.place(relx = 0.65, rely = 0, relwidth = 0.05, relheight = 1)
        self.day_entry.place(relx = 0.70, rely = 0, relwidth = 0.05, relheight = 1)
        
        self.m_label.place(relx = 0.75, rely = 0, relwidth = 0.05, relheight = 1)
        self.month_entry.place(relx = 0.80, rely = 0, relwidth = 0.05, relheight = 1)
        
        self.y_label.place(relx = 0.85, rely = 0, relwidth = 0.05, relheight = 1)
        self.year_entry.place(relx = 0.90, rely = 0, relwidth = 0.10, relheight = 1)
        
    def get(self):
        d = int(self.day_entry_var.get())
        m = int(self.month_entry_var.get())
        y = int(self.year_entry_var.get())
        try:
            entry_date = date(y, m, d)
            if entry_date == date.today() or entry_date < date.today():
                raise CateringDateError
        except ValueError:
            raise CateringDateError
        else:
            return str(entry_date)
    
    def setEntryValue(self, value):
        n = 0
        for entry in [self.year_entry, self.month_entry, self.day_entry]:
            entry.delete(0, 'end')
            entry.insert(0, value.split('-')[n])
            n += 1

class CateringPageLabeledEntry(tk.Frame):
    def __init__(self, master, text, photo, extra_label = str(), default_text = str(), on_default = True):
        tk.Frame.__init__(self, master, background = CINZA)
        self.on_default = on_default
        self.photo = photo
        self.label = tk.Label(self, text = text, image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        self.label.photo = self.photo
        self.label.place(relx = 0, rely = 0, relwidth = 0.6, relheight = 1)
        self.entry_v = tk.StringVar()
        self.entry = tk.Entry(self, textvariable = self.entry_v, font = MINI_FONT)
        self.entry.insert(0, default_text)
        self.entry.bind('<Button-1>', self.onClick)
        self.default = default_text
        if extra_label:
            self.entry.place(relx = 0.65, rely = 0, relwidth = 0.25, relheight = 1)
            self.extra_label = tk.Label(self, text = extra_label, image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
            self.extra_label.place(relx = 0.90, rely = 0, relwidth = 0.1, relheight = 1)
        else:
            self.entry.place(relx = 0.65, rely = 0, relwidth = 0.35, relheight = 1)
        
    def get(self):
        value = self.entry_v.get()
        float_val = value.split(',')
        if isinstance(float_val, list) and len(float_val) == 2:
            float_val = str('.').join(float_val)
            try:
                float_val = float(float_val)
            except ValueError:
                pass
            else:
                value = float_val
        if self.on_default:
            if value == self.default or value == str():
                raise CateringDefaultValue
            else:
                return value
        else:
            return value
    
    def onClick(self, event):
        if self.entry_v.get() == self.default and self.on_default:
            event.widget.delete(0, 'end')
    
    def setEntryValue(self, value):
        self.entry.delete(0, 'end')
        self.entry.insert(0, value)

class CateringPageMenuButton(tk.Frame):
    def __init__(self, master, image, text):
        tk.Frame.__init__(self, master)
        self.bg_img = ImageTk.PhotoImage(image)
        self.button = tk.Button(self, image = self.bg_img, text = text, font = FONT, compound = 'center')
        self.button.photo = self.bg_img
        self.button.pack()

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
        
class CateringPageScrollBarFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)            
        
        vscrollbar = tk.Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill = 'y', side = 'right', expand = False)
        canvas = tk.Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set)
        canvas.pack(side = 'left', fill = 'both', expand = 'True')
        vscrollbar.config(command=canvas.yview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.interior = tk.Frame(canvas, **kwargs)
        interior_id = canvas.create_window((0, 0), window=self.interior, anchor='nw')
        
        def _configure_interior(event):
            canvas.config(scrollregion=canvas.bbox('all'))
            canvas.config(height = self.interior.winfo_reqheight(), width = self.interior.winfo_reqwidth())
            if self.interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=self.interior.winfo_reqwidth(), height = self.interior.winfo_reqheight())
        
        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
                
        canvas.bind('<Configure>', _configure_canvas)

        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/60)), 'units')
            except:pass
        self.interior.bind("<MouseWheel>", _on_mousewheel)

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

class CateringPageTable(tk.Frame):
    def __init__(self, master, photo, color, headers, **kwargs):
        # HEADERS = LISTA DE NOMES
        super().__init__(master, borderwidth = 5, background = color, **kwargs)
        self.color = color
        self.headers = headers
        self.widgets = {}
        
        self.scrollbar = tk.Scrollbar(self, orient = 'vertical', background = color, command = self.moveLists)
        self.scrollbar.place(relx = 0.95, rely = 0.3, relwidth = 0.05, relheight = 0.7)
        
        x = 0
        w = 0.95 / len(self.headers)
        
        for header in self.headers:
            title = CateringPageTitleLabel(self, header, photo, MEDIUM_FONT)
            title.place(relx = x, rely = 0, relwidth = w, relheight = 0.3)
            listbox = tk.Listbox(self, yscrollcommand = self.scrollbar.set, selectforeground = 'black', selectbackground = color, font = MINI_FONT, selectmode = 'multiple')
            listbox.bind('<MouseWheel>', self.onMouseWheel)
            listbox.bind('<ButtonRelease-1>', self.onClick)
            listbox.bind('<ButtonRelease-3>', self.delValues)
            listbox.place(relx = x , rely = 0.3, relwidth = w, relheight = 0.7)
            self.widgets[header] = listbox
            x += w
        
    def setValues(self, values):
        # values = dict
        for item, value in values.items():
            self.widgets[item].insert('end', value)
    
    def moveLists(self, *args):
        for widget in self.widgets.values():
            widget.yview(*args)

    def onMouseWheel(self, event):
        for widget in self.widgets.values():
            widget.yview_scroll(int(-1 * event.delta / 60), "units")
        return "break"

    def onClick(self, event):
        widget = event.widget
        try:
            selection = widget.curselection()
        except:
            pass
        else:
            for widget in self.widgets.values():
                for item in range(widget.size()):
                    widget.itemconfig(item, background = 'white')
            for widget in self.widgets.values():
                for value in selection:
                    widget.itemconfig(value, background = self.color)
    
    def delValues(self, event):
        widget = event.widget
        try:
            selection = widget.curselection()
        except:
            pass
        else:
            for widget in self.widgets.values():
                widget.delete(selection)


class CateringPageTitleLabel(tk.Frame):
    def __init__(self, master, title, photo, font = FONT):
        tk.Frame.__init__(self, master)
        self.label = tk.Label(self, text = title, image = photo, compound = 'center', font = font, relief = 'raised')
        self.label.photo = photo
        self.label.pack()

class CateringProduct:
    def __init__(self, name, tipe = '', cost = 0, price = 0, liter = 0, white = 0, uni = 0, uni_n = 0, inloadf = 0):
        self.name = str(name)
        self.type = str(tipe)
        self.cost = float(cost)
        self.price = float(price)
        self.liter = float(liter)
        self.white = int(white)
        self.uni = str(uni)
        self.uni_n = int(uni_n)
        
        try:
            CateringDBManager.load(CateringDBManager.db_info['products'], name = name)
        except CateringObjectNotFound:
            return
        else:
            if inloadf:
                return
            else:
                raise CateringExistingObject

    def save(self, overwrite = False):
        if not hasattr(self, 'id'):
            self.id = CateringDBManager.getMaxID('PRODUCTS')
        try:
            CateringDBManager.load(CateringDBManager.db_info['products'], self.name)
        except CateringObjectNotFound:
            CateringDBManager.save(CateringDBManager.db_info['products'], self.getData())
            print("Produto {n} Guardado!".format(n = self.name))
            return True
        else:
            if overwrite:
                CateringDBManager.update(CateringDBManager.db_info['products'], self.getData())
                print("Produto {n} Atualizado!".format(n = self.name))
                return True
            else:
                raise CateringExistingObject
        
    def load(name, like = False):
        try:
            data = CateringDBManager.load(CateringDBManager.db_info['products'], name = name, like = like)
            print(data)
        except CateringObjectNotFound:
            raise CateringObjectNotFound
        else:
            if like:
                return data
            else:
                print(data)
                obj = CateringProduct(data[1], tipe = data[2], cost = data[3], price = data[4], liter = data[5], white = data[6], uni = data[7], uni_n = data[8], inloadf = 1)
                obj.id = data[0]
                print("Produto {n} Carregado!".format(n = name))
                return(obj)
        
    def delete(self):
        CateringDBManager.delete(CateringDBManager.db_info['products'], self.getData())
        print("Produto {n} Removido!".format(n = self.name))
        return True
    
    def getData(self):
        data = (self.id, self.name, self.type, self.cost, self.price, self.liter, self.white, self.uni, self.uni_n)
        return data
    
    def getItems():
        return CateringProduct.items[self.type]
    
CateringProduct.items = {'carne' : ['prato refeição', 'garfo carne', 'faca carne'],
                         'peixe' : ['prato refeição', 'garfo peixe', 'faca peixe'],
                         'sopa' : ['prato sopa', 'colher sopa'],
                         'entrada' : ['prato pequeno', 'garfo pequeno', 'faca pequena', 'colher pequena'],
                         'sobremesa' : ['prato pequeno', 'garfo pequeno', 'faca pequena', 'colher pequena'],
                         'bebida' : ['copos de água', 'copos de vinho', 'copos de bar']}

class CateringProductPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, background = CINZA)

        self.photo = ImageTk.PhotoImage(BG_AMARELO)

        title_bar = CateringPageTitleLabel(self, 'Gestão de Produtos', self.photo)
        title_bar.place(relx = 0.05, rely = 0.05, relwidth = 0.9, height = 60)
        
        new_separator = CateringPageTitleLabel(self, 'Criar Novo Produto', self.photo)
        new_separator.place(relx = 0.10, rely = 0.15, relwidth = 0.8, height = 30)

        self.name_entry = CateringPageLabeledEntry(self, 'Nome do Produto', self.photo, default_text = 'Inserir Nome')
        self.name_entry.place(relx = 0.15, rely = 0.20, relwidth = 0.7, height = 30)

        self.cost_entry = CateringPageLabeledEntry(self, 'Custo do Produto', self.photo, extra_label = '€')
        self.cost_entry.place(relx = 0.15, rely = 0.25, relwidth = 0.7, height = 30)
        
        self.price_entry = CateringPageLabeledEntry(self, 'Preço do Produto', self.photo, extra_label = '€')
        self.price_entry.place(relx = 0.15, rely = 0.30, relwidth = 0.7, height = 30)
        
        self.type_entry = CateringPageLabeledComboBox(self, 'Tipo de Produto', ['carne', 'peixe', 'sopa', 'bebida', 'entrada', 'sobremesa'], self.photo)
        self.type_entry.place(relx = 0.15, rely = 0.35, relwidth = 0.7, height = 30)
        
        manager_separator = CateringPageTitleLabel(self, 'Gerir Produto', self.photo)
        manager_separator.place(relx = 0.10, rely = 0.50, relwidth = 0.8, height = 30)
        
        self.manager_entry = CateringPageLabeledEntry(self, 'Nome do Produto', self.photo, on_default = False)
        self.manager_entry.place(relx = 0.15, rely = 0.55, relwidth = 0.7, height = 30)

#        BUTOES
        self.save_b = tk.Button(self, text = 'Gravar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.save_b.photo = self.photo
        self.save_b.place(relx = 0.10, rely = 0.85, relwidth = 0.20, height = 60)

        self.load_b = tk.Button(self, text = 'Carregar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.load_b.photo = self.photo
        self.load_b.place(relx = 0.40, rely = 0.85, relwidth = 0.20, height = 60)

        self.delete_b = tk.Button(self, text = 'Apagar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.delete_b.photo = self.photo
        self.delete_b.place(relx = 0.70, rely = 0.85, relwidth = 0.20, height = 60)
        
        #STATUS BAR
        self.status_bar = tk.Label(self, image = self.photo, compound = 'center', font = FONT, relief = 'sunken')
        self.status_bar.photo = self.photo
        self.status_bar.place(relx = 0, rely = 0.95, relwidth = 1, relheight = 0.05)

        self.save_b.bind('<ButtonRelease-1>', self.saveProduct)
        self.load_b.bind('<ButtonRelease-1>', self.loadProduct)
        self.delete_b.bind('<ButtonRelease-1>', self.deleteProduct)
        
        self.after(500, self.c_update)
        
    def show_sub_page_drinks(self):
        try:
            self.uni_entry.destroy()
            self.uni_n_entry.destroy()
        except AttributeError:
            pass
        self.liter_entry = CateringPageLabeledEntry(self, 'Litros por Unidade', self.photo, extra_label = 'L')
        self.liter_entry.place(relx = 0.15, rely = 0.40, relwidth = 0.7, height = 25)

        self.white_v = tk.IntVar()
        self.white_entry = tk.Checkbutton(self, text = 'Bebida Branca', variable = self.white_v, font = MINI_FONT, relief = 'raised')
        self.white_entry.place(relx = 0.15 + (70 * 0.0065), rely = 0.45, relwidth = 70 * 0.0035, height = 25)

#    MOSTRAR SUBMENU DE SOBREMESAS/ENTRADAS
    def show_sub_page_uni(self):
        try:
            self.liter_entry.destroy()
            self.white_entry.destroy()
        except AttributeError:
            pass
        self.uni_entry = CateringPageLabeledComboBox(self, 'Característica do produto', ['Unitário', 'Divisível'], self.photo)
        self.uni_entry.place(relx = 0.15, rely = 0.40, relwidth = 0.7, height = 25)
        self.uni_n_entry = CateringPageLabeledEntry(self, 'Numero médio de divisões possiveis', self.photo)
        self.uni_n_entry.place(relx = 0.15, rely = 0.45, relwidth = 0.7, height = 25)
    
        
#    COSTUME UPDATE PARA FUNÇÃO AFTER
    def c_update(self):
        tipe = self.type_entry.get()
        if tipe == 'bebida':
#            CONDIÇÃO PARA NAO ATUALIZAR O MESMO
            try:
                boolean_v = self.white_entry.winfo_ismapped()
            except:
                self.show_sub_page_drinks()
            else:
                if not boolean_v:
                    self.show_sub_page_drinks()

        elif tipe == 'entrada' or tipe == 'sobremesa':
#            CONDIÇÃO PARA NAO ATUALIZAR O MESMO
            try:
                boolean_v = self.uni_entry.winfo_ismapped()
            except:
                self.show_sub_page_uni()
            else:
                if not boolean_v:
                    self.show_sub_page_uni()
                else:
                    if self.uni_entry.get() == 'Unitário':
                        self.uni_n_entry.setEntryValue(1)
                        self.uni_n_entry.entry.config(state = 'disabled')
                    else:
                        self.uni_n_entry.entry.config(state = 'normal')
        else:
            try:
                self.uni_entry.destroy()
                self.uni_n_entry.destroy()
            except:
                pass
            try:
                self.liter_entry.destroy()
                self.white_entry.destroy()
            except:
                pass
        #CONTADOR DA BARRA DE STATS
        try:
            if self.counter:
                self.counter -= 1
            else:
                self.setStatus('')
                
        except AttributeError:
            pass
        self.after(500, self.c_update)

#    FUNÇAO GRAVAR PRODUTOS
    def saveProduct(self, event):
        self.subFramesDestroy()
        try:
            items_l = {'name' : self.name_entry.get(),
                       'cost' : self.cost_entry.get(),
                       'price' : self.price_entry.get(),
                       'type' : self.type_entry.get()}
            tipe = items_l['type']
            if tipe == 'bebida':
                items_l['white'] = self.white_v.get()
                items_l['liter'] = self.liter_entry.get()
            elif tipe == 'entrada' or tipe == 'sobremesa':
                items_l['uni'] = self.uni_entry.get()
                items_l['uni_n'] = self.uni_n_entry.get()
        except CateringDefaultValue:
            self.setStatus('Impossível Gravar Produto, dados em falta!')
            return False
        try:
            self.obj = CateringProduct(items_l['name'], tipe = items_l['type'], cost = items_l['cost'], price = items_l['price'])
        except CateringExistingObject:
            self.setStatus('Já existe produto com esse nome!')
            
            self.obj = CateringProduct.load(items_l['name'])
            self.obj.type = items_l['type']
            self.obj.cost = items_l['cost']
            self.obj.price = items_l['price']
            
            if tipe == 'bebida':
                self.obj.liter = items_l['liter']
                self.obj.white = items_l['white']
            elif tipe == 'entrada' or tipe == 'sobremesa':
                self.obj.uni = items_l['uni']
                self.obj.uni_n = items_l['uni_n']
            
            self.popup = CateringPagePopUpMensage(self, mensage = "Produto já existe\nAlterar informação?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)
            
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            self.popup.button_yes.bind('<ButtonRelease-1>', self.overwrite)
            self.manager_entry.setEntryValue(self.obj.name)
        except ValueError:
            self.setStatus('Impossível Gravar Produto, dados em falta!')
        else: 
            if tipe == 'bebida':
                self.obj.liter = items_l['liter']
                self.obj.white = items_l['white']
            elif tipe == 'entrada' or tipe == 'sobremesa':
                self.obj.uni = items_l['uni']
                self.obj.uni_n = items_l['uni_n']
            try:
                if self.obj.name != '':
                    self.obj.save()
                else:
                    self.setStatus('Impossível Gravar Produto, dados em falta!')
                    return
            except sqlite3.OperationalError:
                self.setStatus('Impossível Gravar Produto, dados em falta!')
            else:
                self.setStatus('Produto Gravado com Sucesso!')
                self.manager_entry.setEntryValue(self.obj.name)
                
    def overwrite(self, event):
        try:
            self.obj.save(overwrite = True)
        except sqlite3.OperationalError:
            self.popup.destroy()
            self.setStatus('Impossível Atualizar Produto, dados em falta!')
        else:
            self.popup.destroy()
            self.setStatus('Produto Atualizado com Sucesso!')
    
    def loadProduct(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            data = CateringProduct.load(name, like = True)
        except CateringObjectNotFound:
            self.setStatus('Não foram encontrados produtos com esse nome!')
        else:
            self.scrollframe = CateringPageScrollBarList(self, 'Produtos Carregados', self.photo, AMARELO, destroyButton = True)
            for row in data:
                self.scrollframe.listbox.insert('end', row[1])
            self.scrollframe.place(relx = 0.25, rely = 0.60, relwidth = 0.5, relheight = 0.2)
            self.scrollframe.listbox.bind('<Double-Button-1>', self.setData)
            self.setStatus('Lista de produtos carregada com sucesso!')
            
    def setData(self, event):
        name = self.scrollframe.listbox.get(self.scrollframe.listbox.curselection())
        data = CateringProduct.load(name)
   
        data =  {'name' : data.name, 'type' : data.type, 'cost' : data.cost, 'price' : data.price, 'white' : data.white, 'liter' : data.liter, 'uni' : data.uni, 'uni_n' : data.uni_n}
        widgets = {'name' : self.name_entry, 'type' : self.type_entry, 'cost' : self.cost_entry, 'price' : self.price_entry}
        
        print(data)
        
        if data['type'] == 'bebida':
            self.show_sub_page_drinks()
            try:
                widgets['white'] = self.white_entry
                widgets['liter'] = self.liter_entry
            except AttributeError:
                pass
        if data['type'] == 'sobremesa' or data['type'] == 'entrada':
            self.show_sub_page_uni()
            try:
                widgets['uni'] = self.uni_entry
                widgets['uni_n'] = self.uni_n_entry
            except AttributeError:
                pass

        for key, value in widgets.items():
            if type(value) == CateringPageLabeledEntry or type(value) == CateringPageLabeledComboBox:
                value.setEntryValue(data[key])
            if isinstance(value, tk.Checkbutton) and data[key]:
                value.select()
        self.manager_entry.setEntryValue(data['name'])
        self.scrollframe.destroy()
        self.setStatus('Produtos Carregados com Sucesso!')
    
    def subFramesDestroy(self):
        try:
            self.popup.destroy()
        except AttributeError:
            pass
        try:
            self.scrollframe.destroy()
        except AttributeError:
            pass
    
    def eventDestroy(self, event):
        self.subFramesDestroy()
    
    def deleteProduct(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            self.obj = CateringProduct.load(name)
        except CateringObjectNotFound:
            self.setStatus('Impossível Remover, Produto não encontrado!')
        else:
            self.popup = CateringPagePopUpMensage(self, mensage = "Remover Produto?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)
            
            self.popup.button_yes.bind('<ButtonRelease-1>', self.confirmed_delete)
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            
    def confirmed_delete(self, event):
        self.popup.destroy()
        self.obj.delete()
        self.setStatus('Produto Removido com sucesso!')
    
    def setStatus(self, mensage):
        self.status_bar.config(text = mensage)
        self.counter = 5

class CateringService():
    def __init__(self, name, number, inloadf = 0):
        self.sets = {'menu' : 0, 'bar' : 0, 'appetizers' : 0, 'desserts' : 0, 'team' : 0}
        self.name = name
        self.number = number
        self.distance = 0
        self.trips = 0
        self.items = CateringItems(self.name + ' Items')
        self.date = date
        self.cups_n = 0
        self.status = 'aberto'
        self.extra_tables = 0
        self.site = ''
        self.apt_l = 1
        self.dst_l = 1
        try:
            CateringDBManager.load(CateringDBManager.db_info['services'], name)
        except CateringObjectNotFound:
            return
        else:
            if inloadf:
                return
            else:
                raise CateringExistingObject
                
    def setSets(self, sets):
        if isinstance(sets, CateringCourseMenu):
            sets.setNumber(self.number)
            self.sets['menu'] = sets
        elif isinstance(sets, CateringBar):
            sets.setNumber(self.number)
            self.sets['bar'] = sets
        elif isinstance(sets, CateringAppetizersMenu):
            sets.setNumber(self.number)
            self.sets['appetizers'] = sets
        elif isinstance(sets, CateringDessertsMenu):
            sets.setNumber(self.number)
            self.sets['desserts'] = sets
        elif isinstance(sets, CateringTeam):
            self.sets['team'] = sets
        else:
            print("Insira class CateringSet")
    
    def getDistanceCost(self):
        cost = (((self.distance * self.trips) / 16) * 1.60)
        return cost
          
    def getTotal(self):
        self.total = {'cost' : 0, 'price' : 0}
        for sets in self.sets.values():
            if sets:
                self.total['cost'] += sets.getTotal()['cost']
                self.total['price'] += sets.getTotal()['price']
        self.total['cost'] += self.getDistanceCost()
        return self.total
        
    def setTableType(self, tabletype):
        self.tabletype = tabletype
        if tabletype == 'redonda':
            self.table_n = 10
        elif tabletype == 'retangular':
            self.table_n = 8
        else:
            print('Essa mesa não existe')

    def getAssemblyItems(self):
        items = CateringItems('Items Montagem')
        tables = int((self.number / self.table_n) + 4)
        items.add('mesas {t}'.format(t = self.tabletype), value = round(tables))
        items.add('mesas de apoio', value = self.extra_tables)
        if self.tabletype == 'redonda':
            items.add('cavaletes', value = int((tables * 3) + (self.extra_tables * 2)))
            items.add('toalhas redondas', value = tables)
            items.add('toalhas retangulares', value = self.extra_tables)
        elif self.tabletype == 'retangular':
            items.add('cavaletes', value = int((tables * 2) + (self.extra_tables * 2)))
            items.add('toalhas retangulares', value = self.extra_tables + tables)
        items.add('cadeiras', value = round(self.number * 1.1))
        items.add('centros mesa', value = tables)
        return items

    def getItems(self):
        self.tools = CateringItems(self.name + ' Ferramentas')
        self.products_n = CateringItems(self.name + ' Produtos')
        for sets in self.sets.values():
            if sets:
                if sets.type == 'appetizers':
                    sets.getItems(level = self.apt_l)
                    if hasattr(sets, 'tools'):
                        self.tools.add(sets.tools)
                    if hasattr(sets, 'products_n'):
                        self.products_n.add(sets.products_n)
                elif sets.type == 'desserts':
                    sets.getItems(level = self.dst_l)
                    if hasattr(sets, 'tools'):
                        self.tools.add(sets.tools)
                    if hasattr(sets, 'products_n'):
                        self.products_n.add(sets.products_n)
                else:
                    sets.getItems()
                    if hasattr(sets, 'tools'):
                        self.tools.add(sets.tools)
                    if hasattr(sets, 'products_n'):
                        self.products_n.add(sets.products_n)
                    
        self.tools.add(self.getAssemblyItems())
        return self.tools, self.products_n
    
    def getData(self):
        id_list = list()
        for sets in ['menu', 'bar', 'appetizers', 'desserts', 'team']:
            if self.sets[sets]:
                id_list.append(self.sets[sets].id)
            else:
                id_list.append(0)
        return(self.id, self.name, self.date, self.number, self.status, self.cups_n, self.tabletype, self.extra_tables, self.trips, self.distance, self.site, id_list[0], id_list[1], id_list[2], id_list[3], id_list[4], self.apt_l, self.dst_l)
    
    def save(self, overwrite = False):
        if not hasattr(self, 'id'):
            self.id = CateringDBManager.getMaxID('SERVICES')
        try:
            CateringDBManager.load(CateringDBManager.db_info['services'], self.name)
        except CateringObjectNotFound:
            CateringDBManager.save(CateringDBManager.db_info['services'], self.getData())
            print("Serviço {n} Guardado!".format(n = self.name))
            return True
        else:
            if overwrite:
                CateringDBManager.update(CateringDBManager.db_info['services'], self.getData())
                print("Serviços {n} Atualizado!".format(n = self.name))
                return True
            else:
                raise CateringExistingObject
        
    def load(name, like = False, id_list = False, where_column = '', operator = ''):
        try:
            data = CateringDBManager.load(CateringDBManager.db_info['services'], name = name, like = like, id_list = id_list, where_column = where_column, operator = operator)
            print(data)
        except CateringObjectNotFound:
            raise CateringObjectNotFound
        else:
            if like:
                return data
            else:
                obj = CateringService(data[1], data[3], inloadf = 1)
                obj.id = data[0]
                obj.date = data[2]
                obj.status = data[4]
                obj.cups_n = data[5]
                tipo = data[6]
                obj.setTableType(tipo)
                obj.extra_tables = data[7]
                obj.trips = data[8]
                obj.distance = data[9]
                obj.site = data[10]
                obj.apt_l = data[16]
                obj.dst_l = data[17]
                sets_list = [data[11], data[12], data[13], data[14], data[15]]
                sets_type = [CateringCourseMenu, CateringBar, CateringAppetizersMenu, CateringDessertsMenu, CateringTeam]
                for sets in sets_list:
                    if sets:
                        set_obj = sets_type[sets_list.index(sets)].load(sets)
                        obj.setSets(set_obj)
                    else:
                        pass
                return(obj)

    def delete(self):
        CateringDBManager.delete(CateringDBManager.db_info['services'], self.getData())
        CateringDBManager.delete(CateringDBManager.db_info['sets'], (self.sets['team'].getData()))
        
    def getAssemblyPage(self):
        page = HTMLWriter(self.name, 'Cargas-Descargas')
        page_items = list()
        page_items.append(self.getAssemblyItems())
        
        if self.cups_n == 1:
            try:
                CateringProduct.items['bebida'].pop(CateringProduct.items['bebida'].index('copos de água'))
                CateringProduct.items['bebida'].pop(CateringProduct.items['bebida'].index('copos de vinho'))
            except ValueError:pass
            CateringProduct.items['bebida'].append('copos')
        elif self.cups_n == 2:
            if 'copos de água' and 'copos de vinho' not in CateringProduct.items['bebida']:
                CateringProduct.items['bebida'].append('copos de água')
                CateringProduct.items['bebida'].append('copos de vinho')
        elif self.cups_n == 3:
            if 'copos de água' and 'copos de vinho' not in CateringProduct.items['bebida']:
                CateringProduct.items['bebida'].append('copos de água')
                CateringProduct.items['bebida'].append('copos de vinho')
            CateringProduct.items['bebida'].append('copos de sumo')
        else:
            raise CateringCupsNumberError
        
        for sett in self.sets.values():
            if sett:
                if sett.type == 'team':
                    pass
                elif sett.type == 'course':
                    page_items.append(sett.getItems()['ferramentas'])
                    page_items.append(sett.getItems()['produtos'])
                elif sett.type == 'bar':
                    page_items.append(sett.getItems()['produtos'])
                elif sett.type == 'desserts':
                    page_items.append(sett.getItems(level = self.dst_l)['ferramentas'])
                elif sett.type == 'appetizers':
                    page_items.append(sett.getItems(level = self.apt_l)['ferramentas'])
        print("LENLENLEN\n" + str(len(page_items)) + "LENLENLEN")
        div_counter = int(len(page_items)) / 3
        loop_counter = 0
        page.openDiv()
        for items in page_items:
            if loop_counter >= div_counter:
                page.closeDiv()
                page.openDiv()
                loop_counter = 0
            page.addHeader('{n}'.format(n = items.name.capitalize()))
            for items_k, items_v in items.get().items():
                page.addParagraph('{k} = {v}'.format(k = items_k, v = items_v))
            loop_counter += 1
        page.closeDiv()
        page.close()
        
    def getExtraProductsPage(self):
        page = HTMLWriter(self.name, 'Sobremesas-Entradas')
        page_items = list()
        for sett in self.sets.values():
            if sett:
                if sett.type == 'appetizers':
                    page_items.append(sett.getItems(self.apt_l)['produtos'])
                elif sett.type == 'desserts':
                    page_items.append(sett.getItems(self.dst_l)['produtos'])
                
        div_counter = 2
        loop_counter = 1
        page.openDiv()
        for items in page_items:
            if loop_counter >= div_counter:
                page.closeDiv()
                page.openDiv()
            page.addHeader('{n}'.format(n = items.name.capitalize()))
            for items_k, items_v in items.get().items():
                page.addParagraph('{k} = {v}'.format(k = items_k, v = items_v))
            loop_counter += 1
        page.closeDiv()
        page.close()
    
    def getTotalPage(self):
        page = HTMLWriter(self.name, 'Total')
        total = {'cost' : 0, 'price' : 0, 'profit' : 0}
        page.openDiv()
        for sett in self.sets.values():
            if sett:
                if sett.type != 'team':
                    if sett.type == 'appetizers' or sett.type == 'desserts':
                        items = sett.getTotal(self.apt_l).items()
                    else:
                        items = sett.getTotal().items()
                    page.addHeader(sett.name)
                    for key, value in items:
                        if key == 'cost':
                            page.addParagraph('Custo = {v} €'.format(v = round(value, 2)))
                            total['cost'] += round(value, 2)
                        elif key == 'price':
                            page.addParagraph('Preço = {v} €'.format(v = round(value, 2)))
                            total['price'] += round(value, 2)
                        elif key == 'profit':
                            page.addParagraph('Lucro = {v} €'.format(v = round(value, 2)))
                            total['profit'] += round(value, 2)
                    # page.addBreakRow()        
        page.addHeader('Custo Médio de Logística')
        page.addParagraph('Distância do Local: {} km'.format(self.distance))
        page.addParagraph('Numero de Viagens: {}'.format(self.trips))
        page.addParagraph('Total Logística: {} €'.format(self.getDistanceCost()))
        total['cost'] += self.getDistanceCost()
        page.closeDiv()
        page.openDiv()
        page.addHeader(self.sets['team'].name)
        total['cost'] += self.sets['team'].getTotal()['cost']
        lista = self.sets['team'].getWorkersHours()
        f_list = list()
        for row in lista:
            f_list.append([str(row[0]), str(row[1]), str(row[2]) + ' €', str(row[3]) + ' €'])
        page.addTable(('Nome', 'Horas (h)', 'Custo (€)', 'Total (€)'), f_list)
        page.addParagraph('Custo = {} €'.format(self.sets['team'].getTotal()['cost']))
        total['profit'] = round(total['price'] - total['cost'], 2)
        page.addHeader('Total Serviço')
        page.addParagraph('Custo {}€'.format(total['cost']))
        page.addParagraph('Preço {}€'.format(total['price']))
        page.addParagraph('Lucro {}€'.format(total['profit']))
        page.closeDiv()
        page.close()

class CateringServicePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        
        self.photo = ImageTk.PhotoImage(BG_AZUL)
        
        self.obj = None
        
        self.main_frame = CateringPageScrollBarFrame(self, height = 3000, background = CINZA)
        self.main_frame.place(x = 0, y = 0, relwidth = 1, relheight = 1)
        
        title = CateringPageTitleLabel(self.main_frame.interior, 'Gestão de Serviços', self.photo)
        title.place(relx = 0.05, y = 50, relwidth = 0.9, height = 60)

        new_separator = CateringPageTitleLabel(self.main_frame.interior, 'Criar Novo Serviço', self.photo)
        new_separator.place(relx = 0.1, y = 130, relwidth = 0.8, height = 30)
        
        self.name_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome', self.photo, default_text = 'Inserir Nome de Serviço')
        self.name_entry.place(relx = 0.15, y = 180, relwidth = 0.7, height = 30)
        
        self.date_entry = CateringPageLabeledDateEntry(self.main_frame.interior, 'Data de Realização', self.photo)
        self.date_entry.place(relx = 0.15, y = 230, relwidth = 0.7, height = 30)
        
        self.number_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Numero de Pessoas', self.photo)
        self.number_entry.place(relx = 0.15, y = 280, relwidth = 0.7, height = 30)
        
        self.cups_number_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Numero de Copos por Pessoa', self.photo)
        self.cups_number_entry.place(relx = 0.15, y = 330, relwidth = 0.7, height = 30)
        
        self.status_entry = CateringPageLabeledComboBox(self.main_frame.interior, 'Estado do Serviço', ['aberto', 'fechado'], self.photo)
        self.status_entry.place(relx = 0.15, y = 380, relwidth = 0.7, height = 30)
        
        self.site_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Local do Serviço', self.photo, default_text = 'Valpaços', on_default = False)
        self.site_entry.place(relx = 0.15, y = 430, relwidth = 0.7, height = 30)
        
        self.distance_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Distância do Serviço', self.photo, extra_label = 'km', default_text = '15', on_default = False)
        self.distance_entry.place(relx = 0.15, y = 480, relwidth = 0.7, height = 30)
        
        self.trips_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Numero de viagens', self.photo, default_text = 0, on_default = False)
        self.trips_entry.place(relx = 0.15, y = 530, relwidth = 0.7, height = 30)
        
        course_separator = CateringPageTitleLabel(self.main_frame.interior, 'Adicionar Menu de Refeição', self.photo)
        course_separator.place(relx = 0.10, y = 580, relwidth = 0.8, height = 30)
        
        self.loaded_course_menus = CateringPageScrollBarList(self.main_frame.interior, 'Menus de Refeição Carregados', self.photo, AZUL)
        self.loaded_course_menus.listbox.name = 'course'
        self.loaded_course_menus.listbox.bind("<<ListboxSelect>>", self.getProducts)
        self.loaded_course_menus.listbox.bind("<ButtonRelease-3>", self.clearListbox)
        self.loaded_course_menus.place(relx = 0.10, y = 630, relwidth = 0.35, height = 150)
        try:
            data = CateringSet.load('course', where_column = 'TYPE')
            for item in data:
                self.loaded_course_menus.listbox.insert('end', item[1])
        except CateringObjectNotFound:
            pass
        
        self.course_menus_products = CateringPageScrollBarList(self.main_frame.interior, 'Produtos', self.photo, AZUL)
        self.course_menus_products.place(relx = 0.55, y = 630, relwidth = 0.35, height = 150)
                
        self.selected_menu = CateringPageInfoLabel(self.main_frame.interior, 'Menu Selecionado', AZUL, font = MEDIUM_FONT)
        self.selected_menu.place(relx = 0.15, y = 800, relwidth = 0.7, height = 30)
        
        bar_separator = CateringPageTitleLabel(self.main_frame.interior, 'Adicionar Bar', self.photo)
        bar_separator.place(relx = 0.10, y = 850, relwidth = 0.8, height = 30)
        
        self.loaded_bars = CateringPageScrollBarList(self.main_frame.interior, 'Bars Carregados', self.photo, AZUL)
        self.loaded_bars.listbox.name = 'bar'
        self.loaded_bars.listbox.bind("<<ListboxSelect>>", self.getProducts)
        self.loaded_bars.listbox.bind("<ButtonRelease-3>", self.clearListbox)
        self.loaded_bars.place(relx = 0.10, y = 900, relwidth = 0.35, height = 150)
        try:
            data = CateringSet.load('bar', where_column = 'TYPE')
            for item in data:
                self.loaded_bars.listbox.insert('end', item[1])
        except CateringObjectNotFound:
            pass
        self.bar_products = CateringPageScrollBarList(self.main_frame.interior, 'Produtos', self.photo, AZUL)
        self.bar_products.place(relx = 0.55, y = 900, relwidth = 0.35, height = 150)
        
        self.selected_bar = CateringPageInfoLabel(self.main_frame.interior, 'Bar Selecionado', AZUL, font = MEDIUM_FONT)
        self.selected_bar.place(relx = 0.15, y = 1070, relwidth = 0.7, height = 30)
        
        desserts_separator = CateringPageTitleLabel(self.main_frame.interior, 'Adicionar Menu de Sobremesas', self.photo)
        desserts_separator.place(relx = 0.10, y = 1120, relwidth = 0.8, height = 30)
        
        self.loaded_desserts = CateringPageScrollBarList(self.main_frame.interior, 'Menus de Sobremesas Carregadas', self.photo, AZUL)
        self.loaded_desserts.listbox.name = 'desserts'
        self.loaded_desserts.listbox.bind("<<ListboxSelect>>", self.getProducts)
        self.loaded_desserts.listbox.bind("<ButtonRelease-3>", self.clearListbox)
        self.loaded_desserts.place(relx = 0.10, y = 1170, relwidth = 0.35, height = 150)
        try:
            data = CateringSet.load('desserts', where_column = 'TYPE')
            for item in data:
                self.loaded_desserts.listbox.insert('end', item[1])
        except CateringObjectNotFound:
            pass
        self.desserts_products = CateringPageScrollBarList(self.main_frame.interior, 'Produtos', self.photo, AZUL)
        self.desserts_products.place(relx = 0.55, y = 1170, relwidth = 0.35, height = 150)

        self.selected_desserts = CateringPageInfoLabel(self.main_frame.interior, 'Menu de Sobremesas Selecionado', AZUL, font = MEDIUM_FONT)
        self.selected_desserts.place(relx = 0.15, y = 1340, relwidth = 0.7, height = 30)
        
        self.desserts_level = CateringPageLabeledComboBox(self.main_frame.interior, 'Nível de Quantidade', ['1', '2', '3'], self.photo)
        self.desserts_level.place(relx = 0.5, y = 1390, relwidth = 0.35, height = 30)
        
        appetizers_separator = CateringPageTitleLabel(self.main_frame.interior, 'Adicionar de Menu de Entradas', self.photo)
        appetizers_separator.place(relx = 0.10, y = 1440, relwidth = 0.8, height = 30)
        
        self.loaded_appetizers = CateringPageScrollBarList(self.main_frame.interior, 'Menus de Entradas Carregadas', self.photo, AZUL)
        self.loaded_appetizers.listbox.name = 'appetizers'
        self.loaded_appetizers.listbox.bind("<<ListboxSelect>>", self.getProducts)
        self.loaded_appetizers.listbox.bind("<ButtonRelease-3>", self.clearListbox)
        self.loaded_appetizers.place(relx = 0.10, y = 1490, relwidth = 0.35, height = 150)
        try:
            data = CateringSet.load('appetizers', where_column = 'TYPE')
            for item in data:
                self.loaded_appetizers.listbox.insert('end', item[1])
        except CateringObjectNotFound:
            pass
        
        self.appetizers_products = CateringPageScrollBarList(self.main_frame.interior, 'Produtos', self.photo, AZUL)
        self.appetizers_products.place(relx = 0.55, y = 1490, relwidth = 0.35, height = 150)
        
        self.selected_appetizers = CateringPageInfoLabel(self.main_frame.interior, 'Menu de Entradas Selecionado', AZUL, font = MEDIUM_FONT)
        self.selected_appetizers.place(relx = 0.15, y = 1660, relwidth = 0.7, height = 30)
        
        self.appetizers_level = CateringPageLabeledComboBox(self.main_frame.interior, 'Nível de Quantidade', ['1', '2', '3'], self.photo)
        self.appetizers_level.place(relx = 0.5, y = 1710, relwidth = 0.35, height = 30)
        
        team_separator = CateringPageTitleLabel(self.main_frame.interior, 'Gestão de Equipa', self.photo)
        team_separator.place(relx = 0.10, y = 1760, relwidth = 0.8, height = 30)
        
        self.loaded_workers = CateringPageScrollBarList(self.main_frame.interior, 'Adicionar Trabalhadores', self.photo, AZUL)
        self.loaded_workers.place(relx = 0.25, y = 1810, relwidth = 0.5, height = 150)
        self.loaded_workers.listbox.bind('<Double-Button-1>', self.setToTable)
        
        data = CateringWorker.load('', like = True)
        for item in data:
            self.loaded_workers.listbox.insert('end', item[1])
        
        table_separator = CateringPageTitleLabel(self.main_frame.interior, 'Tabela de Trabalhadores do Serviço', self.photo)
        table_separator.place(relx = 0.2, y = 1980, relwidth = 0.6, height = 30)
        
        self.workers_table = CateringPageTable(self.main_frame.interior, self.photo, AZUL, ['Nome Trabalhador', 'Horas de Serviço'])
        self.workers_table.place(relx = 0.2, y = 2030, relwidth = 0.6, height = 200)
        
        self.hours_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Numero de horas', self.photo, default_text = 'Numero de horas')
        self.hours_entry.place(relx = 0.2, y = 2250, relwidth = 0.4, height = 30)
        
        self.add_button = tk.Button(self.main_frame.interior, text = 'Adicionar', image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        self.add_button.photo = self.photo
        self.add_button.place(relx = 0.615, y = 2250, relwidth = 0.15, height = 30)
        self.add_button.bind('<ButtonRelease-1>', self.addHours)
        
        assembly_separator = CateringPageTitleLabel(self.main_frame.interior, 'Material de Montagem', self.photo)
        assembly_separator.place(relx = 0.10, y = 2300, relwidth = 0.8, height = 30)
        
        self.table_type_entry = CateringPageLabeledComboBox(self.main_frame.interior, 'Tipo de mesa', ['redonda', 'retangular'], self.photo)
        self.table_type_entry.place(relx = 0.2, y = 2350, relwidth = 0.6, height = 30)
        
        self.table_n_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Numero de mesas extra', self.photo)
        self.table_n_entry.place(relx = 0.2, y = 2400, relwidth = 0.6, height = 30)

        results_separator = CateringPageTitleLabel(self.main_frame.interior, 'Resultados Finais', self.photo)
        results_separator.place(relx = 0.1, y = 2450, relwidth = 0.8, height = 30)
        
        self.assembly_b = tk.Button(self.main_frame.interior, text = 'Montagem', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.assembly_b.photo = self.photo
        self.assembly_b.bind('<ButtonRelease-1>', self.getAssemblyPage)
        self.assembly_b.place(relx = 0.10, y = 2500, relwidth = 0.20, height = 60)

        self.values_b = tk.Button(self.main_frame.interior, text = 'Valores', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.values_b.photo = self.photo
        self.values_b.bind('<ButtonRelease-1>', self.getTotalPage)
        self.values_b.place(relx = 0.40, y = 2500, relwidth = 0.20, height = 60)

        self.products_b = tk.Button(self.main_frame.interior, text = 'Produtos', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.products_b.photo = self.photo
        self.products_b.bind('<ButtonRelease-1>', self.getExtraProductsPage)
        self.products_b.place(relx = 0.70, y = 2500, relwidth = 0.20, height = 60)
    
        manager_separator = CateringPageTitleLabel(self.main_frame.interior, 'Gerir Serviço', self.photo)
        manager_separator.place(relx = 0.1, y = 2580, relwidth = 0.8, height = 30)
        
        self.manager_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome do Serviço', self.photo, on_default = False)
        self.manager_entry.place(relx = 0.25, y = 2630, relwidth = 0.5, height = 30)
        
        self.save_b = tk.Button(self.main_frame.interior, text = 'Gravar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.save_b.photo = self.photo
        self.save_b.bind('<ButtonRelease-1>', self.save)
        self.save_b.place(relx = 0.10, y = 2850, relwidth = 0.20, height = 60)

        self.load_b = tk.Button(self.main_frame.interior, text = 'Carregar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.load_b.photo = self.photo
        self.load_b.bind('<ButtonRelease-1>', self.load)
        self.load_b.place(relx = 0.40, y = 2850, relwidth = 0.20, height = 60)

        self.delete_b = tk.Button(self.main_frame.interior, text = 'Apagar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.delete_b.photo = self.photo
        self.delete_b.bind('<ButtonRelease-1>', self.delete)
        self.delete_b.place(relx = 0.70, y = 2850, relwidth = 0.20, height = 60)

        self.obj_bar = CateringPageInfoLabel(self, 'Objeto em Uso:', AZUL, default_text = 'Nenhum', font = FONT)
        self.obj_bar.place(relx = 0, rely = 0, relwidth = 1, height = 30)
    
        self.status_bar = tk.Label(self, image = self.photo, compound = 'center', font = FONT, relief = 'sunken')
        self.status_bar.photo = self.photo
        self.status_bar.place(relx = 0, rely = 0.95, relwidth = 1, relheight = 0.05)

        self.after(500, self.c_update)
    
    def c_update(self):
        try:
            if self.counter:
                self.counter -= 1
            else:
                self.setStatus('')
        except AttributeError:
            pass
        self.after(500, self.c_update)
    
    def addHours(self, event):
        hours = int(self.hours_entry.get())
        for widget in self.workers_table.widgets.values():
            selections = widget.curselection()
            if selections:
                for selection in selections:
                    print(selection)
                    last_hours = int(self.workers_table.widgets['Horas de Serviço'].get(selection))
                    print(last_hours + hours)
                    self.workers_table.widgets['Horas de Serviço'].delete(selection)
                    self.workers_table.widgets['Horas de Serviço'].insert(selection, last_hours + hours)

    def setToTable(self, event):
        widget = event.widget
        value = widget.get('active')
        self.workers_table.setValues({'Nome Trabalhador' : value, 'Horas de Serviço' : 0})
    
    def getProducts(self, event):
        widget = event.widget
        try:
            selection = widget.curselection()[0]
            value = widget.get(selection)
        except IndexError:
            pass
        else:
            self.clearListbox(event)
            obj = CateringSet.load(value)
            for product in obj.products.get().keys():
                if widget.name == 'course':
                    self.course_menus_products.listbox.insert('end', product)
                    self.selected_menu.setInfo(value)
                elif widget.name == 'bar':
                    self.bar_products.listbox.insert('end', product)
                    self.selected_bar.setInfo(value)
                elif widget.name == 'desserts':
                    self.desserts_products.listbox.insert('end', product)
                    self.selected_desserts.setInfo(value)
                elif widget.name == 'appetizers':
                    self.appetizers_products.listbox.insert('end', product)
                    self.selected_appetizers.setInfo(value)
            widget.itemconfig(selection, background = AZUL)
            
    def clearListbox(self, event):
        widget = event.widget
        name = widget.name
        for item in range(widget.size()):
            widget.itemconfig(item, background = 'white')
        if name == 'course':
            self.course_menus_products.listbox.delete(0, 'end')
            self.selected_menu.setInfo('')
        elif name == 'bar':
            self.bar_products.listbox.delete(0, 'end')
            self.selected_bar.setInfo('')
        elif name == 'desserts':
            self.desserts_products.listbox.delete(0, 'end')
            self.selected_desserts.setInfo('')
        elif name == 'appetizers':
            self.appetizers_products.listbox.delete(0, 'end')
            self.selected_appetizers.setInfo('')
        widget.selection_clear(0, 'end')
        
    def getAssemblyPage(self, event):
        if isinstance(self.obj, CateringService):
            try:
                self.obj.getAssemblyPage()
                self.setStatus('Página de Montagem gerada com Sucesso!')
            except CateringCupsNumberError:
                self.setStatus('Numero de Copos não suportado')
                return
        else:
            self.setStatus('Nenhum Objeto em uso. Crie um novo ou carregue objeto existente!')
        
    def getTotalPage(self, event):
        if isinstance(self.obj, CateringService):
            self.obj.getTotalPage()
            self.setStatus('Página de Valores gerada com Sucesso!')
        else:
            self.setStatus('Nenhum Objeto em uso. Crie um novo ou carregue objeto existente!')
    
    def getExtraProductsPage(self, event):
        if isinstance(self.obj, CateringService):
            self.obj.getExtraProductsPage()
            self.setStatus('Página de Produtos gerada com Sucesso!')
        else:
            self.setStatus('Nenhum Objeto em uso. Crie um novo ou carregue objeto existente!')
        
    def save(self, event):
        try:
            name = self.name_entry.get().strip()
            date = self.date_entry.get()
            number = self.number_entry.get()
            cups = self.cups_number_entry.get()
            status = self.status_entry.get()
            site = self.site_entry.get()
            distance = self.distance_entry.get()
            trips = self.trips_entry.get()
            table_type = self.table_type_entry.get()
            extra_table = self.table_n_entry.get()
            menu = self.selected_menu.get()
            bar = self.selected_bar.get()
            desserts = self.selected_desserts.get()
            appetizers = self.selected_appetizers.get()
            appetizers_level = self.appetizers_level.get()
            desserts_level = self.appetizers_level.get()
            workers_list = list()
            for worker in self.workers_table.widgets['Nome Trabalhador'].get(0, 'end'):
                workers_list.append(worker)
            workers_hours = list()
            for hours in self.workers_table.widgets['Horas de Serviço'].get(0, 'end'):
                workers_hours.append(hours)
        except CateringDefaultValue:
            self.setStatus('Impossível Guardar Serviço, dados em falta')
            return False
        except CateringDateError:
            self.setStatus('Impossível Guardar Serviço, Data de inválida')
        else:
            try:
                self.obj = CateringService(name, number)
            except CateringExistingObject:
                self.obj = CateringService.load(name)
                team = CateringTeam.load('Equipa ' + self.obj.name)
                team.products = CateringItems('Products ' + team.name)
                for worker in workers_list:
                    team.setObjects(CateringWorker.load(worker))
                    team.addWorkerHours(worker, workers_hours[workers_list.index(worker)])
                team.save(overwrite = True)
                self.obj.number = int(number)
                self.obj.date = date
                self.obj.cups_n = int(cups)
                self.obj.status = status
                self.obj.setTableType(table_type)
                self.obj.extra_tables = int(extra_table)
                self.obj.site = site
                self.obj.distance = int(distance)
                self.obj.trips = int(trips)
                self.obj.sets = {'menu' : 0, 'bar' : 0, 'appetizers' : 0, 'desserts' : 0, 'team' : 0}
                self.obj.setSets(team)
                self.obj.apt_l = int(appetizers_level)
                self.obj.dst_l = int(desserts_level)
                for item in [menu, bar, desserts, appetizers]:
                    if item:
                        self.obj.setSets(CateringSet.load(item))
                    else:
                        pass
                self.popup = CateringPagePopUpMensage(self, mensage = "Serviço já existe\nAlterar informação?")
                self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)            
                self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
                self.popup.button_yes.bind('<ButtonRelease-1>', self.overwrite)
            else:
                team = CateringTeam('Equipa ' + self.obj.name)
                for worker in workers_list:
                    team.setObjects(CateringWorker.load(worker))
                    team.addWorkerHours(worker, workers_hours[workers_list.index(worker)])
                team.save()
                self.obj.setSets(team)
                self.obj.number = int(number)
                self.obj.date = date
                self.obj.cups_n = int(cups)
                self.obj.status = status
                self.obj.setTableType(table_type)
                self.obj.extra_tables = int(extra_table)
                self.obj.site = site
                self.obj.distance = int(distance)
                self.obj.trips = int(trips)
                self.obj.apt_l = int(appetizers_level)
                self.obj.dst_l = int(desserts_level)
                for item in [menu, bar, desserts, appetizers]:
                    if item:
                        self.obj.setSets(CateringSet.load(item))
                    else:
                        pass
                self.obj.save()
                self.setObjBar(self.obj.name)
                self.manager_entry.setEntryValue(self.obj.name)
                self.setStatus('Serviço Guardado Com Sucesso')
                
    def load(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            data = CateringService.load(name, like = True)
        except CateringObjectNotFound:
            self.setStatus('Não foram encontrados Serviços com esse nome!')
        else:
            self.loaded_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Serviços Carregados', self.photo, AZUL, destroyButton = True)
            for row in data:
                self.loaded_listbox.listbox.insert('end', row[1])
            self.loaded_listbox.place(relx = 0.25, y = 2680, relwidth = 0.50, height = 150)
            self.loaded_listbox.listbox.bind('<Double-Button-1>', self.setData)
            self.setStatus('Lista de Serviços carregada com sucesso')

    def setData(self, event):
        name = event.widget.get('active')
        print('\n\n' + name + '\n\n')
        self.obj = CateringService.load(name)
        # INSERIR DADOS DE ENTRYS
        data_entry = [(self.name_entry, self.obj.name),
                      (self.date_entry, self.obj.date),
                      (self.number_entry, self.obj.number),
                      (self.cups_number_entry, self.obj.cups_n),
                      (self.status_entry, self.obj.status),
                      (self.site_entry, self.obj.site),
                      (self.distance_entry, self.obj.distance),
                      (self.trips_entry, self.obj.trips),
                      (self.table_type_entry, self.obj.tabletype),
                      (self.table_n_entry, self.obj.extra_tables),
                      (self.appetizers_level, self.obj.apt_l),
                      (self.desserts_level, self.obj.dst_l)]
        for data in data_entry:
            data[0].setEntryValue(data[1])
        
        # INSERIR DADOS LISTBOX
        sets_objs = list()
        widgets = [(self.loaded_course_menus, self.course_menus_products, self.selected_menu),
                   (self.loaded_bars, self.bar_products, self.selected_bar),
                   (self.loaded_appetizers, self.appetizers_products, self.selected_appetizers),
                   (self.loaded_desserts, self.desserts_products, self.selected_desserts)]
        for item in list(self.obj.sets.values())[:4]:
            if item:
                sets_objs.append(item)
            else:
                sets_objs.append(0)
        n = 0
        for sett in sets_objs:
            listbox_w = widgets[n][0].listbox
            listbox_prod = widgets[n][1].listbox
            selected_name = widgets[n][2]
            listbox_prod.delete(0, 'end')
            if sett:
                # RESET LISTBOX ITEM CONFIG
                for item in range(listbox_w.size()):
                    listbox_w.itemconfig(item, background = 'white')
                listbox_w.itemconfig(listbox_w.get(0, 'end').index(sett.name), background = AZUL)
                listbox_w.see(listbox_w.get(0, 'end').index(sett.name))
                for item in sett.getObjects().keys():
                    listbox_prod.insert('end', item)
                selected_name.setInfo(sett.name)
            else:
                pass
            n += 1
        
        self.workers_table.widgets['Nome Trabalhador'].delete(0, 'end')
        self.workers_table.widgets['Horas de Serviço'].delete(0, 'end')
        
        for data_row in self.obj.sets['team'].getWorkersHours():
            print(data_row)
            self.workers_table.widgets['Nome Trabalhador'].insert('end', data_row[0])
            self.workers_table.widgets['Horas de Serviço'].insert('end', data_row[1])
        self.manager_entry.setEntryValue(self.obj.name)
        self.loaded_listbox.destroy()
        self.setObjBar(self.obj.name)
        self.setStatus('Serviço Carregado com Sucesso!')

    def delete(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            self.obj = CateringService.load(name)
        except CateringObjectNotFound:
            self.setStatus('Impossível Remover, Serviço não encontrado!')
        else:
            self.popup = CateringPagePopUpMensage(self, mensage = "Remover Produto?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)
            
            self.popup.button_yes.bind('<ButtonRelease-1>', self.confirmed_delete)
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            
    def confirmed_delete(self, event):
        self.popup.destroy()
        self.obj.delete()
        self.setStatus('Serviço Removido Com Sucesso!')
        self.obj = None
        self.setObjBar('Nenhum')


    def overwrite(self, event):
        try:
            self.obj.save(overwrite = True)
        except sqlite3.OperationalError:
            self.popup.destroy()
            self.setStatus('Impossível Atualizar Serviço, dados em falta!')
        else:
            self.popup.destroy()
            self.setStatus('Serviço Atualizado com Sucesso')                 
        
    def subFramesDestroy(self):
        try:
            self.popup.destroy()
        except AttributeError:
            pass
        try:
            self.loaded_listbox.destroy()
        except AttributeError:
            pass
    
    def eventDestroy(self, event):
        self.subFramesDestroy()
        
    def setStatus(self, mensage):
        self.status_bar.config(text = mensage)
        self.counter = 3
        
    def setObjBar(self, mensage):
        self.obj_bar.setInfo(mensage)

class CateringSet():
    def __init__(self, name, inloadf = 0):
        raise Exception('Impossivel instanciar esta class')

    def getItems(self):
        tools = CateringItems('Ferramentas ' + self.name)
        products_n = CateringItems('Produtos ' + self.name)
        types = []
        for pro in self.products.get().values():
            if pro.type == 'bebida':
#                coeficiente de multiplicação de bebida
                if not pro.white:
                    literpp = 0.5
                else:
                    literpp = 0.1
                botle_n = (self.number * literpp) / pro.liter
                products_n.add(pro.name, value = int(botle_n))
                pass
            types.append(pro.type)
        types = set(types)

        for typ in types:
            if typ == 'bebida':
                for item in CateringProduct.items[typ]:
                    if self.type == 'bar':
                        if item == 'copo de bar':
                            tools.add(item, value = int(self.number * 1.25))
                        else:
                            continue
                    if self.type == 'course':
                        if item != 'copo de bar':
                            tools.add(item, value = int(self.number * 1.1))
                        else:
                            continue
            else:   
                for item in CateringProduct.items[typ]:
                    tools.add(item, value = int(self.number * 1.1))
        return {'ferramentas' : tools, 'produtos' : products_n}

    def setObjects(self, product):
        if isinstance(product, list):
            for p in product:
                self.setObjects(p)
        elif isinstance(product, CateringProduct) and self.__class__.__name__ != 'CateringTeam':
            self.products.add(product)
        else:
            print('Insira objetos de classe CateringProduct')

    def setNumber(self, number):
        self.number = number

    def getObjects(self, name = ''):
        if name:
            return self.products.get(name = name)
        else:
            return self.products.get()

    def delObjects(self, product):
        if isinstance(product, list):
            for p in product:
                self.delProduct(p)
        else:
            if product in self.products.get().keys():
                self.products.rem(product)
            else:
                print("Produto nao existe neste menu")

    def getTotal(self):
        self.total = {'cost' : 0, 'price' : 0, 'profit' : 0}
        for product in self.products.get().values():
            if product.type != 'bebida':
                self.total['cost'] += round(product.cost * self.number, 2)
                self.total['price'] += round(product.price * self.number, 2)
                self.total['profit'] += round(float(product.price * self.number) - float(product.cost * self.number), 2)
            else:
                if not product.white:
                    literpp = 0.5
                else:
                    literpp = 0.1
                botle_n = int((self.number * literpp) / product.liter)
                self.total['cost'] += round(product.cost * botle_n, 2)
                self.total['price'] += round(product.price * botle_n, 2)
                self.total['profit'] += round(float(product.price * botle_n) - float(product.cost * botle_n), 2)
        return self.total

    def getData(self):
        return (self.id, self.name, self.type)

    def save(self, overwrite = False):
        if not hasattr(self, 'id'):
            self.id = CateringDBManager.getMaxID('SETS')
        try:
            CateringDBManager.load(CateringDBManager.db_info['sets'], self.name)
        except CateringObjectNotFound:
            CateringDBManager.save(CateringDBManager.db_info['sets'], self.getData())
            for pro in self.products.get().values():
                if isinstance(pro, CateringWorker):
                    hrs = pro.hours
                else:
                    hrs = 0
                CateringDBManager.save(CateringDBManager.db_info['setsproducts'], (self.id, pro.id, hrs))
            return True
        else:
            if overwrite:
                CateringDBManager.update(CateringDBManager.db_info['sets'], self.getData())                
                id_list = []
                for pro in self.products.get().values():
                    id_list.append(pro.id)
                p_data = CateringDBManager.load(CateringDBManager.db_info['setsproducts'], self.id, id_list = True)
                pid_data = []
                out_pid_data = []
                for data in p_data:
                    if data[1] in id_list:
                        pid_data.append(data[1])
                    else:
                        out_pid_data.append(data[1])
                for pro in self.products.get().values():
                    if isinstance(pro, CateringWorker):
                        hrs = pro.hours
                    else:
                        hrs = 0
                    if pro.id in pid_data:
                        CateringDBManager.update(CateringDBManager.db_info['setsproducts'], (self.id, pro.id, hrs), operator = 'AND PRODUCTID = {i}'.format(i = pro.id))
                    else:
                        CateringDBManager.save(CateringDBManager.db_info['setsproducts'], (self.id, pro.id, hrs))
                for ids in out_pid_data:
                    CateringDBManager.delete(CateringDBManager.db_info['setsproducts'], (self.id, pro.id, hrs), operator = 'AND PRODUCTID = {i}'.format(i = ids))
                return True
            else:
                raise CateringExistingObject

    def load(name, like = False, where_column = '', operator = ''):
        try:
            m_data = CateringDBManager.load(CateringDBManager.db_info['sets'], name = name, like = like, where_column = where_column, operator = operator)
            if like or where_column:
                return m_data
            tipe = m_data[2]
            if tipe == 'bar':
                sets = CateringBar(m_data[1], inloadf = True)
            elif tipe == 'course':
                sets = CateringCourseMenu(m_data[1], inloadf = True)
            elif tipe == 'desserts':
                sets = CateringDessertsMenu(m_data[1], inloadf = True)
            elif tipe == 'appetizers':
                sets = CateringAppetizersMenu(m_data[1], inloadf = True)
            elif tipe == 'team':
                sets = CateringTeam(m_data[1], inloadf = True)
            sets.id = m_data[0]
            try:
                products_id = CateringDBManager.load(CateringDBManager.db_info['setsproducts'], name = sets.id, id_list = True)
                for pro_id in products_id:
                    if tipe != 'team':
                        product = CateringProduct.load(pro_id[1])
                        sets.setObjects(product)
                    else:
                        product = CateringWorker.load(pro_id[1])
                        sets.setObjects(product)
                        sets.addWorkerHours(product.name, pro_id[2])
            except CateringObjectNotFound:
                pass
            return sets
        except CateringObjectNotFound:
            raise CateringObjectNotFound

    def delete(self):
        CateringDBManager.delete(CateringDBManager.db_info['sets'], self.getData())
        for pro in self.products.get().values():
            CateringDBManager.delete(CateringDBManager.db_info['setsproducts'], self.getData(), operator = 'AND PRODUCTID = {i}'.format(i = pro.id))
        print("Removido com Sucesso!")

class CateringBar(CateringSet):
    def __init__(self, name, inloadf = 0):
        self.number = 1
        self.name = name
        self.type = 'bar'
        self.products = CateringItems('Products ' + self.name)
        try:
            CateringDBManager.load(CateringDBManager.db_info['sets'], name)
        except CateringObjectNotFound:
            return
        else:
            if inloadf:
                return
            else:
                raise CateringExistingObject

class CateringCourseMenu(CateringSet):
    def __init__(self, name, inloadf = 0):
        self.name = name
        self.number = 1
        self.type = 'course'
        self.products = CateringItems('Products ' + self.name)
        try:
            CateringDBManager.load(CateringDBManager.db_info['sets'], name)
        except CateringObjectNotFound:
            return
        else:
            if inloadf:
                return
            else:
                raise CateringExistingObject

class CateringExtraMenu(CateringSet):
    def __init__(self, name, inloadf = 0):
        raise Exception('Impossivel instanciar esta class')

    def getItems(self, level = 2):
        tools = CateringItems('Ferramentas ' + self.name)
        products_items = CateringItems('Produtos ' + self.name)
        n_items = self.number * (level + 1)
        products_n = round(n_items / 2)
        uni_n = 0
        not_uni_n = 0
         
        for item in self.products.get().values():
            if item.uni == 'Unitário':
                uni_n += 1
            else:
                not_uni_n += 1
        
        for item in CateringProduct.items['sobremesa']:
            tools.add(item, value = round(self.number * 1.25))
        
        uni_prod_n = products_n / uni_n
        not_uni_prod_n = products_n / not_uni_n
        
        div_n = 0
        
        for prod in self.products.get().values():
            if prod.uni == 'Unitário':
                n = round((uni_prod_n))
                products_items.add(prod.name, value = n)
            else:
                n = round((not_uni_prod_n / prod.uni_n)+0.55)
                products_items.add(prod.name, value = n)
                div_n += n
        
        div_n = round(div_n / 2)
        tools.add('Espatulas', value = div_n)
        tools.add('Pinças', value = div_n)
        tools.add('Colheres de Self-Service', value = div_n)
                
        return {'ferramentas' : tools, 'produtos' : products_items}

    def getTotal(self, level = 2):
        self.getItems()
        total = {'cost' : 0, 'price' : 0, 'profit' : 0}
        for keys, values in self.getItems(level)['produtos'].get().items():
            total['cost'] += round(values * self.products.get(keys).cost, 2)
            total['price'] += round(values * self.products.get(keys).price, 2)
            total['profit'] += round(float(values * self.products.get(keys).price) - float(values * self.products.get(keys).cost), 2)
        return total

class CateringDessertsMenu(CateringExtraMenu):
    def __init__(self, name, inloadf = 0):
        self.name = name
        self.number = 1
        self.type = 'desserts'
        self.products = CateringItems('Produtos ' + self.name)
        try:
            CateringDBManager.load(CateringDBManager.db_info['sets'], name)
        except CateringObjectNotFound:
            return
        else:
            if inloadf:
                return
            else:
                raise CateringExistingObject
                
class CateringAppetizersMenu(CateringExtraMenu):
    def __init__(self, name, inloadf = 0):
        self.name = name
        self.number = 1
        self.type = 'appetizers'
        self.products = CateringItems('Produtos ' + self.name)
        try:
            CateringDBManager.load(CateringDBManager.db_info['sets'], name)
        except CateringObjectNotFound:
            return
        else:
            if inloadf:
                return
            else:
                raise CateringExistingObject

class CateringTeam(CateringSet):
    def __init__(self, name, inloadf = 0):
        self.name = name
        self.type = 'team'
        self.products = CateringItems('Products ' + self.name)
        try:
            CateringDBManager.load(CateringDBManager.db_info['sets'], name)
        except CateringObjectNotFound:
            return
        else:
            if inloadf:
                return
            else:
                raise CateringExistingObject

    def getItems(self):
        pass

    def getTotal(self):
        self.total = {'cost' : 0}
        for product in self.products.get().values():
            self.total['cost'] += round(product.cost * product.hours, 2)
        return self.total

    def setNumber(self):
        pass

    def setObjects(self, product):
        if isinstance(product, list):
            for p in product:
                self.setObjects(p)
        elif isinstance(product, CateringWorker):
            self.products.add(product)
        else:
            print('Insira objetos de classe CateringWorkers')

    def addTeamHours(self, hours):
        for worker in self.getObjects().values():
            worker.addHours(hours)

    def addWorkerHours(self, worker, hours):
        try:
            if isinstance(hours, int):
                self.getObjects(name = worker).addHours(hours)
            else:
                print('Horas devem ser numeros inteiros')
        except KeyError:
            print('Não Existe Trabalhador')

    def getWorkersHours(self, worker = '', formated = False):
        if worker:
            preço = self.getObjects(name = worker).cost
            horas = self.getObjects(name = worker).hours
            nome = self.getObjects(name = worker).name
            return ([name, horas, cost, horas * cost])
        else:
            lista = []
            for worker in self.getObjects().values():
                lista.append([worker.name, worker.hours, worker.cost, worker.hours * worker.cost])
            return lista
class CateringWorker:
    def __init__(self, name, tipe = 'geral', cost = 1 ,inloadf = 0):
        self.name = str(name)
        self.type = str(tipe)
        self.cost = float(cost)
        self.hours = 0

        try:
            CateringDBManager.load(CateringDBManager.db_info['workers'], name)
        except CateringObjectNotFound:
            return
        else:
            if inloadf:
                return
            else:
                raise CateringExistingObject
                
    def addHours(self, hours):
        self.hours += hours
        
    def getTotalCost(self):
        total = self.hours * self.cost
        return total            

    def getData(self):
        self.data = (self.id, self.name, self.cost, self.type)
        return self.data

    def save(self, overwrite = False):
        if not hasattr(self, 'id'):
            self.id = CateringDBManager.getMaxID('WORKERS')
        try:
            CateringDBManager.load(CateringDBManager.db_info['workers'], self.name)
        except CateringObjectNotFound:
            CateringDBManager.save(CateringDBManager.db_info['workers'], self.getData())
            print("Worker {n} Guardado!".format(n = self.name))
            return True
        else:
            if overwrite:
                CateringDBManager.update(CateringDBManager.db_info['workers'], self.getData())
                print("Worker {n} Atualizado!".format(n = self.name))
                return True
            else:
                raise CateringExistingObject
        
    def load(name, like = False):
        try:
            data = CateringDBManager.load(CateringDBManager.db_info['workers'], name, like = like)
        except CateringObjectNotFound:
            raise CateringObjectNotFound
        else:
            if like:
                return data
            else:
                obj = CateringWorker(data[1], cost = data[2], tipe = data[3], inloadf = 1)
                obj.id = data[0]
                print("Worker {n} Carregado!".format(n = name))
                return(obj)
        
    def delete(self):
        CateringDBManager.delete(CateringDBManager.db_info['workers'], self.getData())
        print("Worker {n} Removido!".format(n = self.name))
        return True
class CateringWorkerPage(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master, background = CINZA)
        
        self.photo = ImageTk.PhotoImage(BG_VERMELHO)
        
        title_bar = CateringPageTitleLabel(self, 'Gestão de Trabalhador', self.photo)
        title_bar.place(relx = 0.05, rely = 0.05, relwidth = 0.9, height = 60)
        
        new_separator = CateringPageTitleLabel(self, 'Criar Novo Trabalhador', self.photo)
        new_separator.place(relx = 0.1, rely = 0.15, relwidth = 0.8, height = 30)
        
        self.name_entry = CateringPageLabeledEntry(self, 'Nome do Trabalhador', self.photo, default_text = 'Inserir Nome')
        self.name_entry.place(relx = 0.15, rely = 0.20, relwidth = 0.7, height = 30)

        self.cost_entry = CateringPageLabeledEntry(self, 'Custo do Trabalhador', self.photo, extra_label = '€')
        self.cost_entry.place(relx = 0.15, rely = 0.25, relwidth = 0.7, height = 30)

        self.type_entry = CateringPageLabeledComboBox(self, 'Tipo de Trabalhador', ['geral', 'servir', 'bar', 'limpezas', 'cozinha'], self.photo)
        self.type_entry.place(relx = 0.15, rely = 0.30, relwidth = 0.7, height = 30)
        
        manager_separator = CateringPageTitleLabel(self, 'Gerir Trabalhador', self.photo)
        manager_separator.place(relx = 0.1, rely = 0.50, relwidth = 0.8, height = 30)
        
        self.manager_entry = CateringPageLabeledEntry(self, 'Nome do Trabalhador', self.photo, on_default = False)
        self.manager_entry.place(relx = 0.15, rely = 0.55, relwidth = 0.7, height = 30)
        
#        BUTOES
        
        self.save_b = tk.Button(self, text = 'Gravar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.save_b.photo = self.photo
        self.save_b.place(relx = 0.10, rely = 0.85, relwidth = 0.20, height = 60)

        self.load_b = tk.Button(self, text = 'Carregar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.load_b.photo = self.photo
        self.load_b.place(relx = 0.40, rely = 0.85, relwidth = 0.20, height = 60)

        self.delete_b = tk.Button(self, text = 'Apagar', image = self.photo, compound = 'center', font = FONT, relief = 'raised')
        self.delete_b.photo = self.photo
        self.delete_b.place(relx = 0.70, rely = 0.85, relwidth = 0.20, height = 60)
        
        #STATUS BAR
        self.status_bar = tk.Label(self, image = self.photo, compound = 'center', font = FONT, relief = 'sunken')
        self.status_bar.photo = self.photo
        self.status_bar.place(relx = 0, rely = 0.95, relwidth = 1, relheight = 0.05)
        
        self.save_b.bind('<ButtonRelease-1>', self.saveWorker)
        self.load_b.bind('<ButtonRelease-1>', self.loadWorker)
        self.delete_b.bind('<ButtonRelease-1>', self.deleteWorker)
        
        self.after(500, self.c_update)
        
    def c_update(self):
        try:
            if self.counter:
                self.counter -= 1
            else:
                self.setStatus('')
        except AttributeError:
            pass
        self.after(500, self.c_update)

    def saveWorker(self, event):
        self.subFramesDestroy()
        try:
            items_l = {'name' : self.name_entry.get(),
                       'cost' : self.cost_entry.get(),
                       'type' : self.type_entry.get()}
        except CateringDefaultValue:
            self.setStatus('Impossível Gravar Trabalhador, dados em falta!')
            return False
        try:
            self.obj = CateringWorker(items_l['name'], tipe = items_l['type'], cost = items_l['cost'])
        except CateringExistingObject:
            self.setStatus('Já existe Trabalhador com esse nome!')
            
            self.obj = CateringWorker.load(items_l['name'])
            self.obj.type = items_l['type']
            self.obj.cost = items_l['cost']
            
            self.popup = CateringPagePopUpMensage(self, mensage = "Trabalhador já existe\nAlterar Informações?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)
            
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            self.popup.button_yes.bind('<ButtonRelease-1>', self.overwrite)
        except ValueError:
            self.setStatus('Impossível Gravar Trabalhador, dados em falta!')
        else: 
            try:
                self.obj.save()
            except sqlite3.OperationalError:
                self.setStatus('Impossível Gravar Trabalhador, dados em falta!')
            else:
                self.setStatus('Trabalhador Gravado com Sucesso!')
                self.manager_entry.setEntryValue(self.obj.name)
    
    def overwrite(self, event):
        try:
            self.obj.save(overwrite = True)
        except sqlite3.OperationalError:
            self.setStatus('Impossível Atualizar, dados em falta!')
            self.popup.destroy()
        else:
            self.popup.destroy()
            self.setStatus('Trabalhador Atualizado com Sucesso!')
        
    def loadWorker(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            data = CateringWorker.load(name, like = 1)
        except CateringObjectNotFound:
            self.setStatus('Não foram encontrados Trabalhadors com esse nome!')
        else:
            self.scrollframe = CateringPageScrollBarList(self, 'Trabalhadores Carregados!', self.photo, VERMELHO, destroyButton = True)
            for row in data:
                self.scrollframe.listbox.insert('end', row[1])
            self.scrollframe.place(relx = 0.25, rely = 0.60, relwidth = 0.5, relheight = 0.2)
            self.scrollframe.listbox.bind('<Double-Button-1>', self.setData)
            self.setStatus('Lista de Trabalhadors carregada com Sucesso!')

    def setData(self, event):
        name = self.scrollframe.listbox.get(self.scrollframe.listbox.curselection())
        data = CateringWorker.load(name)
   
        data =  {'name' : data.name, 'cost' : data.cost, 'type' : data.type}
        widgets = {'name' : self.name_entry, 'cost' : self.cost_entry, 'type' : self.type_entry}

        print(data)

        for key, value in widgets.items():
            if type(value) == CateringPageLabeledEntry or type(value) == CateringPageLabeledComboBox:
                value.setEntryValue(data[key])
        self.manager_entry.setEntryValue(data['name'])
        self.scrollframe.destroy()
        self.setStatus('Trabalhadores Carregados com Sucesso')

    def subFramesDestroy(self):
        try:
            self.popup.destroy()
        except AttributeError:
            pass
        try:
            self.scrollframe.destroy()
        except AttributeError:
            pass
        
    def eventDestroy(self, event):
        self.subFramesDestroy()
        
    def deleteWorker(self, event):
        self.subFramesDestroy()
        name = self.name_entry.get()
        try:
            self.obj = CateringWorker.load(name)
        except CateringObjectNotFound:
            self.setStatus('Impossível Remover, Trabalhador não encontrado')
        else:
            self.popup = CateringPagePopUpMensage(self, mensage = "Remover Trabalhador?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)
            
            self.popup.button_yes.bind('<ButtonRelease-1>', self.confirmed_delete)
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            
    def confirmed_delete(self, event):
        self.obj.delete()
        self.popup.destroy()
        self.setStatus('Trabalhador Removido Com Sucesso')
        
    def setStatus(self, mensage):
        self.status_bar.config(text = mensage)
        self.counter = 5

class HTMLWriter():
    def __init__(self, name, page_name):
        self.name = name
        username = os.environ['USERNAME']
        try:
            os.mkdir('C:\\Users\\{u}\\Desktop\\InventariosCatering'.format(u = username))
        except FileExistsError:pass
        try:
            os.mkdir('C:\\Users\\{u}\\Desktop\\InventariosCatering\\{n}'.format(n = self.name, u = username))
        except FileExistsError:pass
        self.file = open('C:\\Users\\{u}\\Desktop\\InventariosCatering\\{n}\\{pn}.htm'.format(n = self.name, pn = page_name, u = username), 'w+')
        self.file.write('<!DOCTYPE html>\n')
        self.file.write('<html>\n')
        self.file.write('<head>\n')
        self.file.write('<title>{t}</title>\n'.format(t = name))
        self.file.write('<style>\n')
        self.file.write('.clearfix::after {content: "";clear: both;display: table;}')
        self.file.write('.box {float:left;width:30.0%;padding:20px}')
        self.file.write('table {border-collapse: collapse;padding: 10px;}\n')
        self.file.write('table, th, td {border: 1px solid black;padding: 10px;}\n')
        self.file.write('h2 {color:grey;}\n')
        self.file.write('</style>\n')
        self.file.write('</head>\n')
        self.file.write('<body>\n')
        self.addHeader(str(self.name), h = 'h1')
        self.addHeader(str(page_name), h = 'h2')
        self.addBreakRow()
        self.file.write('<div class = "clearfix">\n')

    def openDiv(self):
        self.file.write('<div class = "box">\n')
        
    def closeDiv(self):
        self.file.write('</div>\n')
    
    def addHeader(self, text, h = 'h3'):
        self.file.write('<{h}>{t}</{h}>\n'.format(h = h, t = text))
        
    def addParagraph(self, text, p = 'p'):
        self.file.write('<{p}>{t}</{p}>\n'.format(p = p, t = text))

    def addBreakRow(self):
        self.file.write('<br>')

    def addTable(self, title, data):
        self.file.write('<table>\n')
        self.file.write('<tr>\n')
        for t in title:
            self.file.write('<th><b>{h}</b></th>\n'.format(h = t))
        self.file.write('</tr>\n')
        for tup in data:
            self.file.write('<tr>\n')
            for d in tup:
                self.file.write('<td>{d}</td>\n'.format(d = d))
            self.file.write('</tr>\n')
        self.file.write('</table>\n')

    def close(self):
        self.file.write('</div>\n')
        self.file.write('</body>')
        self.file.write('</html>')
        self.file.close()
        print('\nPÁGINA {n} CRIADA!\n'.format(n = self.name))