#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 02:31:24 2019

@author: L.A.B
"""
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
    
#    INCOMPLETA !!!!! FALTAM CUSTOS        
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

            
        
    


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
                