# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 08:54:50 2020

@author: L.A.B
"""

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
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    