# -*- coding: utf-8 -*-
"""
Created on Fri Nov 22 18:38:52 2519

@author: L.A.B
"""

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
        