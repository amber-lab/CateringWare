#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:23:03 2019

@author: L.A.B
"""

#FRAME DE PRODUCTS
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