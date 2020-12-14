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


#OBJETOS

worker = CateringWorker('Leonardo', 5)
worker.save()

worker1 = CateringWorker('Nuno Eira', 0)
worker1.save()

worker2 = CateringWorker('Chico Sousa', 7)
worker2.save()

carne = CateringProduct('Vitela Assada', 'carne', 2, 3)
carne.save()

peixe = CateringProduct('Bacalhau com Broa', 'peixe', 3, 4)
peixe.save()

sopa = CateringProduct('Sopa Legumes', 'sopa', 0.25, 1.25)
sopa.save()

sobremesa_u = CateringProduct('Pudim unitário', 'sobremesa', 0.3, 0.5, uni = 1)
sobremesa_u.save()

sobremesa = CateringProduct('Pudim', 'sobremesa', 2, 3)
sobremesa.save()

entrada = CateringProduct('Rissois', 'entrada', 0.3, 0.4, uni = 1)
entrada.save()

agua = CateringProduct('Água Natural', 'bebida', 0.25, 0.35, liter = 1.5)
agua.save()

coca = CateringProduct('Coca Cola', 'bebida', 2, 2.1, liter = 2)
coca.save()

ice = CateringProduct('Ice Tea', 'bebida', 1.4, 1.5, liter = 1.5)
ice.save()

joy = CateringProduct('Joy', 'bebida', 1.2, 1.3, liter = 1.5)
joy.save()

whiskey = CateringProduct('Whiskey Velho', 'bebida', 15, 16, liter = 0.75, white = 1)
whiskey.save()

rum = CateringProduct('Rum', 'bebida', 7, 8, liter = 1.0, white = 1)
rum.save()

#SETS
print("\nMenu\n")
menu_c = CateringMenu('Casamento')
menu_c.setNumber(100)
menu_c.setObjects([carne, peixe, sopa, agua, joy, coca, ice])
menu_c.save()
print("\nTotal\n")
print(menu_c.getTotal())
print("\nItems\n")
print(menu_c.getItems())
print("\nProdutos\n")
print(menu_c.getObjects())

print("\nSobremesas\n")
menu_s = CateringExtraMenu('Sobremesas')
menu_s.setNumber(100)
menu_s.setObjects([sobremesa, sobremesa_u])
menu_s.save()
print("\nTotal\n")
print(menu_s.getTotal())
print("\nItems\n")
print(menu_s.getItems())
print("\nProdutos\n")
print(menu_s.getObjects())

print("\nEntradas\n")
menu_e = CateringExtraMenu('Entradas')
menu_e.setNumber(100)
menu_e.setObjects(entrada)
menu_e.save()
print("\nTotal\n")
print(menu_e.getTotal())
print("\nItems\n")
print(menu_e.getItems())
print("\nProdutos\n")
print(menu_e.getObjects())

print("\nMontagem\n")
assem = CateringAssembly('Montagem Casamento')
assem.setNumber(100)
assem.setTable('redonda')
assem.save()
assem.getItems()
assem.getTotal()
print("\nTotal\n")
print(assem.getTotal())
print("\nItems\n")
print(assem.getItems())
print("\nProdutos\n")
print(assem.getObjects())

print("\nBar\n")
bar = CateringBar('Bar Casamento')
bar.setNumber(100)
bar.setObjects([coca, ice, joy, rum, whiskey])
bar.save()
print("\nTotal\n")
print(bar.getTotal())
print("\nItems\n")
print(bar.getItems())
print("\nProdutos\n")
print(bar.getObjects())

print("\nEquipa\n")
team = CateringTeam('Equipa Casamento')
team.setObjects([worker, worker1, worker2])
team.addWorkerHours('Leonardo', 10)
team.addWorkerHours('Nuno Eira', 10)
team.addWorkerHours('Chico Sousa', 10)
team.save()
print("\nTotal\n")
print(team.getTotal())
print("\nItems\n")
print(team.getItems())
print("\nProdutos\n")
print(team.getObjects())

service = CateringService('Casamento', 100)
service.setObjects([menu_c, menu_s, bar, team, menu_e])
service.setObjects(assem, table = 'retangular')

print("Executado")
