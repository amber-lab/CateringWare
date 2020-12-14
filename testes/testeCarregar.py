#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  2 02:43:56 2019

@author: L.A.B
"""
import sqlite3
exec(open('G:/Working Dir/CateringCalculator/CateringItems.py','r', encoding = 'utf-8').read())
exec(open('G:/Working Dir/CateringCalculator/CateringProduct.py','r', encoding = 'utf-8').read())
exec(open('G:/Working Dir/CateringCalculator/CateringSet.py','r', encoding = 'utf-8').read())
exec(open('G:/Working Dir/CateringCalculator/CateringWorker.py','r', encoding = 'utf-8').read())
exec(open('G:/Working Dir/CateringCalculator/CateringService.py','r', encoding = 'utf-8').read())

worker = CateringWorker.load('Nuno Eira')
#worker.save()

worker1 = CateringWorker.load('Chico Sousa')
#worker.save()

worker2 = CateringWorker.load('Leonardo')
#worker.save()

carne = CateringProduct.load('Vitela Assada')
#carne.price += 1
#carne.save()

peixe = CateringProduct.load('Bacalhau com Broa')
#peixe.price += 1
#peixe.save()

sopa = CateringProduct.load('Sopa Legumes')
#sopa.price += 0.1
#peixe.save()

sobremesa = CateringProduct.load('Pudim')
#sobremesa.price += 1
#peixe.save()

sobremesa_1 = CateringProduct.load('Pudim unitário')
#sobremesa_1.price += 0.1
#sobremesa.save()

entrada = CateringProduct.load('Rissois')
#entrada.price += 0.1

menu_c = CateringMenu.load('Casamento')
menu_c.setNumber(100)

#menu_a.setObjects(sopa)
#menu_a.setObjects(peixe)
#menu_a.setObjects(carne)
#menu_a.save()
#print(menu_a.getTotal())

menu_s = CateringMenu.load('Sobremesas')
menu_s.setNumber(100)

menu_e = CateringExtraMenu.load('Entradas')
menu_e.setNumber(100)

assem = CateringAssembly.load('Montagem Casamento')
assem.setNumber(100)
assem.setTable('retangular')
#print(assem.getTotal())

bar = CateringBar.load('Bar Casamento')
bar.setNumber(100)
#print(bar.getTotal())

team  = CateringTeam.load('Equipa Casamento')