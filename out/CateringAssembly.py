# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Sun Feb  2 16:10:03 2020

@author: L.A.B
"""

class CateringAssembly():
    def __init__(self, table, number = 1):
        self.number = number
        self.table = table
        if self.table == 'redonda':
            self.table_n = 10
        elif self.table == 'retangular':
            self.table_n = 8
        else:
            print('Essa mesa não existe')

    def getItems(self):
        self.items = CateringItems('Items Montagem')
        tables = round((self.number / self.table_n) + 3.5)
        self.items.add('mesas {t}'.format(t = self.table), value = tables)
        self.items.add('cavaletes', value = int(tables * 2))
        self.items.add('toalhas', value = tables)
        self.items.add('cadeiras', value = self.number * 1.1)
        self.items.add('centros mesa', value = tables)
        return self.items.get()

    def setNumber(self, number):
        if isinstance(number, int):
            self.number = number

    def getObjects(self):
        return

    def getTotal(self):
        return self.getItems()