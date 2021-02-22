# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Tue Mar 10 17:58:23 2020

@author: L.A.B
"""

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
            name = self.name_entry.get()
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
            self.loaded_listbox = CateringPageScrollBarList(self.main_frame.interior, 'Menus Carregados', self.photo, AZUL, destroyButton = True)
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
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        