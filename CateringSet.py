# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Mon Sep 30 01:30:29 2019

@author: L.A.B
"""

class CateringSet():
    def __init__(self, name, inloadf = 0):
        raise Exception('Impossivel instanciar esta class')

    def getItems(self):
        tools = CateringItems('Ferramentas ' + self.name)
        products_n = CateringItems('Produtos ' + self.name)
        drinks_n = CateringItems('Bebidas' + self.name)

        types = []
        for pro in self.products.get().values():
            if pro.type == 'bebida':
#                coeficiente de multiplicação de bebida
                if not pro.white:
                    literpp = 0.5
                else:
                    literpp = 0.1
                botle_n = (self.number * literpp) / pro.liter
                drinks_n.add(pro.name, value = int(botle_n))
                pass
            if pro.type in ['carne', 'sopa', 'peixe']:
                products_n.add(pro.name, value = self.number)
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
        return {'ferramentas' : tools, 'produtos' : products_n, 'bebidas' : products_n}

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
            



































