#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:09:00 2019

@author: L.A.B
"""

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