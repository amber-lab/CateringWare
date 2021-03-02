# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Mon Mar  9 15:31:58 2020

@author: L.A.B
"""

class CateringDessertsPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, background = CINZA)
        
        self.photo = ImageTk.PhotoImage(BG_VERDE)
        
        self.main_frame = CateringPageScrollBarFrame(self, height = 1100, background = CINZA)
        self.main_frame.place(x = 0, y = 0, relwidth = 1, relheight = 1)

        title_bar = CateringPageTitleLabel(self.main_frame.interior, 'Gestão de Ementas de Sobremesas', self.photo)
        title_bar.place(relx = 0.05, y = 50, relwidth = 0.9, height = 60)
        
        new_separator = CateringPageTitleLabel(self.main_frame.interior, 'Criar Novo Ementa de Sobremesas', self.photo)
        new_separator.place(relx = 0.1, y = 130, relwidth = 0.8, height = 30)
        
        self.name_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome da Ementa de Sobremesas', self.photo, default_text = 'Inserir Nome')
        self.name_entry.place(relx = 0.15, y = 180, relwidth = 0.7, height = 30)
        
        bar_prod_label = CateringPageTitleLabel(self.main_frame.interior, 'Sobremesas da Ementa', self.photo)
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

        manager_separator = CateringPageTitleLabel(self.main_frame.interior, 'Gerir Ementa de Sobremesas', self.photo)
        manager_separator.place(relx = 0.1, y = 670, relwidth = 0.8, height = 30)
        
        self.manager_entry = CateringPageLabeledEntry(self.main_frame.interior, 'Nome da Ementa Sobremesas', self.photo, on_default = False)
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
            self.setStatus('Impossível Gravar Ementa, dados em falta!')
            return False
        prod_list = list(self.dess_prod_uni_listbox.listbox.get(0, 'end'))
        prod_list.extend(list(self.dess_prod_div_listbox.listbox.get(0, 'end')))
        print("\n\n" + str(prod_list) + "\n\n")
        if not name:
            self.setStatus('Impossível Gravar Ementa, dados em falta!')
            return False
        print(name)
        try:
            self.obj = CateringDessertsEmenta(name)
            for product in prod_list:
                self.obj.setObjects(CateringProduct.load(product))
        except CateringExistingObject:
            self.setStatus('Já existe Ementa com esse nome!')
            
            self.obj = CateringSet.load(name)
            
            out_prod_list = list(self.obj.products.get().values())
            
            for product in out_prod_list:
                if product.name not in prod_list:
                    self.obj.delObjects(product.name)
                    print("\n\n\nRemovido Product " + product.name + "\n\n\n")
            
            for product in prod_list:
                self.obj.setObjects(CateringProduct.load(product))
            
            self.popup = CateringPagePopUpMensage(self, mensage = "Ementa já existe\nAlterar informação?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)            
            
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            self.popup.button_yes.bind('<ButtonRelease-1>', self.overwrite)
            
            self.manager_entry.setEntryValue(name)
        else:
            try:
                self.obj.save()
            except sqlite3.OperationalError:
                self.setStatus('Impossível Gravar Ementa, dados em falta!')
            else:
                self.setStatus('Ementa Gravado Com Sucesso')
            
    def overwrite(self, event):
        try:
            self.obj.save(overwrite = True)
        except sqlite3.OperationalError:
            self.popup.destroy()
            self.setStatus('Impossível Atualizar Ementa, dados em falta!')
        else:
            self.popup.destroy()
            self.setStatus('Ementa Atualizado com Sucesso!')
    
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
            self.setStatus('Não foram encontrados Ementas com esse nome!')
        else:
            self.scrollframe = CateringPageScrollBarList(self.main_frame.interior, 'Ementas Carregados', self.photo, VERDE, destroyButton = True)
            for row in data:
                self.scrollframe.listbox.insert('end', row[1])
            self.scrollframe.place(relx = 0.25, y = 770, relwidth = 0.50, height = 150)
            self.scrollframe.listbox.bind('<Double-Button-1>', self.setData)
            self.setStatus('Lista de Ementas carregada com sucesso!')
    
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
        self.setStatus('Ementa Carregado com sucesso!')
    
    def deleteDesserts(self, event):
        self.subFramesDestroy()
        name = self.manager_entry.get()
        try:
            self.obj = CateringSet.load(name)
        except CateringObjectNotFound:
            self.setStatus('Impossível Remover, Ementa não encontrado!')
        else:
            self.popup = CateringPagePopUpMensage(self, mensage = "Remover Ementa?")
            self.popup.place(relx = 0.25, rely = 0.60, relwidth = 0.50, relheight = 0.2)
            
            self.popup.button_yes.bind('<ButtonRelease-1>', self.confirmed_delete)
            self.popup.button_no.bind('<ButtonRelease-1>', self.eventDestroy)
            
    def confirmed_delete(self, event):
        self.popup.destroy()
        self.obj.delete()
        self.setStatus('Ementa removido com sucesso!')
    
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        