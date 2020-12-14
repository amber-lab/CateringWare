#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 23:02:05 2019

@author: L.A.B
"""

class CateringBar():
    def __init__(self, name, inloadf = 0):
        conn = sqlite3.connect('CateringDB.db')
        query = "SELECT NAME FROM BAR WHERE NAME = '{n}';".format(n = name)
        cursor = conn.execute(query)
        if not inloadf:
            try:
                exists = cursor.fetchall()[0]
            except IndexError:
                self.name = name
                self.loaded = 1
            else:
                self.loaded = 0
                print('Ja existe bar com esse nome')
        if not hasattr(self, 'name'):
            self.name = name
        self.cost = 0
        self.price = 0
        self.drinks = CateringItems('Products ' + self.name)
        self.items = CateringItems('Items ' + self.name)
        conn.close()
    
    def getItems(self):
        self.items = CateringItems('Items ' + self.name)
        for product in self.getDrinks().values():
            self.items.add(product.items)
        print(self.items.get())
        
    def getDrinks(self, name = ''):
        if name:
            return self.drinks.get(name)
        else:
            return self.drinks.get()
        
    def setProduct(self, product):
        if isinstance(product, list):
            for p in product:
                self.setProduct(p)
        elif isinstance(product, CateringProduct) and product.type == 'bebida':
            self.drinks.add(product)
        else:
            print('Insira objetos de classe CateringRecipe')
    
    def getTotal(self):
        print("\n\nBar: {n}\n".format(n = self.name))
        for product in self.drinks.get().values():
            self.cost += product.cost
            self.price += product.price
            print('Produto: {n} | Custo: {c} | Preço: {p}\n'.format(n = product.name, c = product.cost, p = product.price))
        print("Total:\nBar: {n} | Custo: {c} | Preço: {p} | Lucro: {l}".format(n = self.name, c = self.cost, p = self.price, l = self.price - self.cost))
            
    
    def save(self):
        if self.loaded:
#        VERIFICAR SE EXISTE
            conn = sqlite3.connect('CateringDB.db')
            query = "SELECT NAME FROM BAR WHERE NAME = '{n}'".format(n = self.name)
            cursor = conn.execute(query)
            try:
                exists = cursor.fetchall()[0]
    #        SENAO EXISTIR:
            except IndexError:
    #            INSERIR BAR
                query = "INSERT INTO BAR(NAME) VALUES('{n}');".format(n = self.name)
                conn.execute(query)
                conn.commit()
    #            PROCURAR ID DE BAR
                query = "SELECT ID FROM BAR WHERE NAME = '{n}';".format(n = self.name)
                cursor = conn.execute(query)
                self.id = cursor.fetchone()[0]
                print("Criado Bar {n}".format(n = self.name))
    #                INSERIR PRODUTO 
                for product in self.getDrinks().values():
                    if hasattr(product, 'id'):
                        query = "INSERT INTO BARPRODUCTS(BAR_ID, PRODUCT_ID) VALUES({bi}, {pi});".format(bi = self.id, pi = product.id)
                        conn.execute(query)
                        conn.commit()
                        print("Inserido {pn} no Bar {bn}".format(pn = product.name, bn = self.name))
                    else:
                        print('Produto sem id, impossivel guardar')
                        
            else:
    #           SE EXISTIR
                write = input('Alterar?\t(1 \ 0)\nR:')
                if write:
    #                PROCURAR ID DE BAR
                    query = "SELECT ID FROM BAR WHERE NAME = '{n}';".format(n = self.name)
                    cursor = conn.execute(query)
                    self.id = cursor.fetchone()[0]
    #                ATUALIZAR NOME
                    query = "UPDATE BAR SET NAME = '{n}' WHERE ID = {i};".format(n = self.name, i = self.id)
                    conn.execute(query)
                    conn.commit()
                    print("Bar {n} atualizado".format(n = self.name))
#                    APAGAR REGISTOS ANTERIORES
                    query = "DELETE FROM BARPRODUCTS WHERE BAR_ID = {i};".format(i = self.id)
                    conn.execute(query)
                    conn.commit()
#                    ATUALIZAR PRODUTOS                    
                    for product in self.getDrinks().values():
                        if hasattr(product, 'id'):
                            query = "INSERT INTO BARPRODUCTS(BAR_ID, PRODUCT_ID) VALUES({bi}, {pi});".format(bi = self.id, pi = product.id)
                            conn.execute(query)
                            conn.commit()
                            print("Atualizado {pn} no Bar {bn}".format(pn = product.name, bn = self.name))
                        else:
                            print('Produto sem id, impossivel guardar')
                    conn.close()
                else:
                    pass
            
    def load(name):
        conn = sqlite3.connect('CateringDB.db')
        query = "SELECT ID FROM BAR WHERE NAME = '{n}'".format(n = name)
        cursor = conn.execute(query)
        try:
            bar_id = cursor.fetchone()[0]
        except IndexError:
            print("Bar {n} não encontrado".format(n = name))
        else:
            bar_obj = CateringBar(name, inloadf = 1)
            bar_obj.id = bar_id
            bar_obj.loaded = 1

            query = "SELECT PRODUCT_ID FROM BARPRODUCTS WHERE BAR_ID = {i};".format(i = bar_id)
            cursor = conn.execute(query)
            for product_id in cursor.fetchall():
                query = "SELECT NAME FROM BARPRODUCTS WHERE ID = {i};".format(i = product_id[0])
                product_cursor = conn.execute(query)
                data = product_cursor.fetchone()
                product_obj = CateringProduct.load(data[0])
                product_obj.loaded = 1
                bar_obj.setProduct(product_obj)
            print("Bar {n} carregado".format(n = name))
            return bar_obj

        conn.commit()
        conn.close()