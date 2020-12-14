#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 14:38:30 2019

@author: L.A.B
"""

class CateringMenu():
    def __init__(self, name, inloadf = 0):
        
        conn = sqlite3.connect('CateringDB.db')
        query = "SELECT NAME FROM MENU WHERE NAME = '{n}';".format(n = name)
        cursor = conn.execute(query)
        if not inloadf:
            try:
                exists = cursor.fetchall()[0]
            except IndexError:
                self.name = name
                self.loaded = 1
            else:
                self.loaded = 0
                print('Ja existe menu com esse nome')
        if not hasattr(self, 'name'):    
            self.name = name
        self.cost = 0
        self.price = 0
        self.products = CateringItems('Products ' + self.name)
        self.drinks = CateringItems('Drinks ' + self.name)
        self.items = CateringItems('Items ' + self.name)
        conn.close()
    
    def getItems(self):
        
        self.items = CateringItems('Items ' + self.name)
        for product in self.getProducts().values():
            self.items.add(product.items)
        print(self.items.get())
    
    def getProducts(self, name = ''):
        if name:
            return self.products.get(name)
        else:
            return self.products.get()
    
    def getDrinks(self, name = ''):
        if name:
            return self.drinks.get(name)
        else:
            return self.drinks.get()

    def setProduct(self, product):
        if isinstance(product, list):
            for p in product:
                self.setProduct(p)
        elif isinstance(product, CateringProduct) and (product.type == 'carne' or product.type == 'peixe' or product.type == 'sopa'):
            self.products.add(product)
        elif isinstance(product, CateringProduct) and product.type == 'bebida':
            self.drinks.add(product)
        else:
            print('Insira objetos de classe CateringRecipe')

    def getTotal(self):
        print("\n\nMenu: {n}\n".format(n = self.name))
        for product in self.products.get().values():
            self.cost += product.cost
            self.price += product.price
            print('Produto: {n} | Custo: {c} | Preço: {p}\n'.format(n = product.name, c = product.cost, p = product.price))
        print("Total:\nMenu: {n} | Custo: {c} | Preço: {p} | Lucro: {l}".format(n = self.name, c = self.cost, p = self.price, l = self.price - self.cost))
            
    
    def save(self):
        if self.loaded:
#        VERIFICAR SE EXISTE
            conn = sqlite3.connect('CateringDB.db')
            query = "SELECT NAME FROM MENU WHERE NAME = '{n}'".format(n = self.name)
            cursor = conn.execute(query)
            try:
                exists = cursor.fetchall()[0]
    #        SENAO EXISTIR:
            except IndexError:
    #            INSERIR MENU
                query = "INSERT INTO MENU(NAME) VALUES('{n}');".format(n = self.name)
                conn.execute(query)
                conn.commit()
    #            PROCURAR ID DE MENU
                query = "SELECT ID FROM MENU WHERE NAME = '{n}';".format(n = self.name)
                cursor = conn.execute(query)
                self.id = cursor.fetchone()[0]
                print("Criado Menu {n}".format(n = self.name))
    #                INSERIR PRODUTO 
                for product in self.getProducts().values():
                    if hasattr(product, 'id'):
                        query = "INSERT INTO MENUPRODUCTS(MENU_ID, PRODUCT_ID) VALUES({mi}, {pi});".format(mi = self.id, pi = product.id)
                        conn.execute(query)
                        conn.commit()
                        print("Inserido {pn} no menu {mn}".format(pn = product.name, mn = self.name))
                    else:
                        print('Produto sem id, impossivel guardar')
                        
                for drink in self.getDrinks().values():
                    if hasattr(drink, 'id'):
                        query = "INSERT INTO MENUPRODUCTS(MENU_ID, PRODUCT_ID) VALUES({mi}, {pi});".format(mi = self.id, pi = drink.id)
                        conn.execute(query)
                        conn.commit()
                        print("Inserido {dn} no menu {mn}".format(dn = drink.name, mn = self.name))
                    else:
                        print('Produto sem id, impossivel guardar')
            else:
    #           SE EXISTIR
                write = input('Alterar?\t(1 \ 0)\nR:')
                if write:
    #                PROCURAR ID DE MENU
                    query = "SELECT ID FROM MENU WHERE NAME = '{n}';".format(n = self.name)
                    cursor = conn.execute(query)
                    self.id = cursor.fetchone()[0]
    #                ATUALIZAR NOME
                    query = "UPDATE MENU SET NAME = '{n}' WHERE ID = {i};".format(n = self.name, i = self.id)
                    conn.execute(query)
                    conn.commit()
                    print("Menu {n} atualizado".format(n = self.name))
#                    APAGAR REGISTOS ANTERIORES
                    query = "DELETE FROM MENUPRODUCTS WHERE MENU_ID = {i};".format(i = self.id)
                    conn.execute(query)
                    conn.commit()
#                    ATUALIZAR PRODUTOS                    
                    for product in self.getProducts().values():
                        if hasattr(product, 'id'):
                            query = "INSERT INTO MENUPRODUCTS(MENU_ID, PRODUCT_ID) VALUES({mi}, {pi});".format(mi = self.id, pi = product.id)
                            conn.execute(query)
                            conn.commit()
                            print("Atualizado {pn} no menu {mn}".format(pn = product.name, mn = self.name))
                        else:
                            print('Produto sem id, impossivel guardar')
                    for drink in self.getDrinks().values():
                        if hasattr(drink, 'id'):
                            query = "INSERT INTO MENUPRODUCTS(MENU_ID, PRODUCT_ID) VALUES({mi}, {pi});".format(mi = self.id, pi = drink.id)
                            conn.execute(query)
                            conn.commit()
                            print("Atualizado Produto {pn} no menu {mn}".format(pn = drink.name, mn = self.name))
                        else:
                            print('Produto sem id, impossivel guardar')
                    conn.close()
                else:
                    pass
            
    def load(name):
        conn = sqlite3.connect('CateringDB.db')
        query = "SELECT ID FROM MENU WHERE NAME = '{n}'".format(n = name)
        cursor = conn.execute(query)
        try:
            menu_id = cursor.fetchone()[0]
        except IndexError:
            print("Menu {n} não encontrado".format(n = name))
        else:
            menu_obj = CateringMenu(name, inloadf = 1)
            menu_obj.id = menu_id
            menu_obj.loaded = 1

            query = "SELECT PRODUCT_ID FROM MENUPRODUCTS WHERE MENU_ID = {i};".format(i = menu_id)
            cursor = conn.execute(query)
            for product_id in cursor.fetchall():
                query = "SELECT NAME FROM PRODUCTS WHERE ID = {i};".format(i = product_id[0])
                product_cursor = conn.execute(query)
                data = product_cursor.fetchone()
                product_obj = CateringProduct.load(data[0])
                product_obj.loaded = 1
                menu_obj.setProduct(product_obj)
                
            print("Menu {n} carregado".format(n = name))
            return menu_obj

        conn.commit()
        conn.close()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            