#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 02:29:53 2019

@author: L.A.B
"""
class CateringWorker:
    def __init__(self, name, tipe = 'geral', cost = 1 ,inloadf = 0):
        self.name = str(name)
        self.type = str(tipe)
        self.cost = float(cost)
        self.hours = 0

        try:
            CateringDBManager.load(CateringDBManager.db_info['workers'], name)
        except CateringObjectNotFound:
            return
        else:
            if inloadf:
                return
            else:
                raise CateringExistingObject
                
    def addHours(self, hours):
        self.hours += hours
        
    def getTotalCost(self):
        total = self.hours * self.cost
        return total            

    def getData(self):
        self.data = (self.id, self.name, self.cost, self.type)
        return self.data

    def save(self, overwrite = False):
        if not hasattr(self, 'id'):
            self.id = CateringDBManager.getMaxID('WORKERS')
        try:
            CateringDBManager.load(CateringDBManager.db_info['workers'], self.name)
        except CateringObjectNotFound:
            CateringDBManager.save(CateringDBManager.db_info['workers'], self.getData())
            print("Worker {n} Guardado!".format(n = self.name))
            return True
        else:
            if overwrite:
                CateringDBManager.update(CateringDBManager.db_info['workers'], self.getData())
                print("Worker {n} Atualizado!".format(n = self.name))
                return True
            else:
                raise CateringExistingObject
        
    def load(name, like = False):
        try:
            data = CateringDBManager.load(CateringDBManager.db_info['workers'], name, like = like)
        except CateringObjectNotFound:
            raise CateringObjectNotFound
        else:
            if like:
                return data
            else:
                obj = CateringWorker(data[1], cost = data[2], tipe = data[3], inloadf = 1)
                obj.id = data[0]
                print("Worker {n} Carregado!".format(n = name))
                return(obj)
        
    def delete(self):
        CateringDBManager.delete(CateringDBManager.db_info['workers'], self.getData())
        print("Worker {n} Removido!".format(n = self.name))
        return True
