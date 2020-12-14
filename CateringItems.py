#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 02:32:42 2019

@author: L.A.B
"""
class CateringItems:
    def __init__(self, name):
        self.name = name
        self.items = {self.name : dict()}       
        
    def add(self, item, value = 1):
        if issubclass(type(item), CateringProduct) or issubclass(type(item), CateringWorker):
            self.items[self.name][item.name] = item
        elif issubclass(type(item), CateringItems):
            self.items[self.name][item.name] = item.items[item.name]
        else:
            self.items[self.name][item] = value
    def rem(self, item):
        if item in self.items[self.name].keys():
            self.items[self.name].pop(item)
        if isinstance(item, CateringItems):
            if item in self.items[self.name].keys():
                self.items[self.name].pop(item.name)

    def get(self, name = '', full = 0):
        if name:
            try:
                return self.items[self.name][name]
            except NameError:
                print("Objecto não existe em {n}".format(n = self.name))
        if full:
            return self.items
        else:
            return self.items[self.name]