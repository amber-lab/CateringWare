#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date

exec(open('C:\\Users\\L.A.B\\Desktop\\CateringCalculator\\CateringErrors.py','r', encoding = 'utf-8').read())
exec(open('C:\\Users\\L.A.B\\Desktop\\CateringCalculator\\CateringDBManager.py','r', encoding = 'utf-8').read())
exec(open('C:\\Users\\L.A.B\\Desktop\\CateringCalculator\\CateringItems.py','r', encoding = 'utf-8').read())
exec(open('C:\\Users\\L.A.B\\Desktop\\CateringCalculator\\CateringProduct.py','r', encoding = 'utf-8').read())
exec(open('C:\\Users\\L.A.B\\Desktop\\CateringCalculator\\CateringSet.py','r', encoding = 'utf-8').read())
exec(open('C:\\Users\\L.A.B\\Desktop\\CateringCalculator\\CateringWorker.py','r', encoding = 'utf-8').read())
exec(open('C:\\Users\\L.A.B\\Desktop\\CateringCalculator\\CateringService.py','r', encoding = 'utf-8').read())
exec(open('C:\\Users\\L.A.B\\Desktop\\CateringCalculator\\HTMLWriter.py','r', encoding = 'utf-8').read())

#PRODUCTS

print("\nCriar Produtos\n\n")

carne = CateringProduct('Vitela Assada', tipe = 'carne', cost = 3, price = 5)
carne.save()
peixe = CateringProduct('Bacalhau Assado', tipe = 'peixe', cost = 3, price = 5)
peixe.save()
sopa = CateringProduct('Sopa Legumes', tipe = 'sopa', cost = 1, price = 2)
sopa.save()
r_carne = CateringProduct('Rissois Carne', tipe = 'entrada', cost = 0.1, price = 0.5)
r_carne.save()
r_camarao = CateringProduct('Rissois Camarão', tipe = 'entrada', cost = 0.1, price = 0.5)
r_camarao.save()
salada = CateringProduct('Salada Fria', tipe = 'entrada', cost = 4, price = 5, uni = 1)
salada.save()
pudim_f = CateringProduct('Pudim Flam', tipe = 'sobremesa', cost = 0.1, price = 0.5, uni = 1)
pudim_f.save()
pudim_c = CateringProduct('Pudim Caseiro', tipe = 'sobremesa', cost = 1, price = 5)
pudim_c.save()
whiskey = CateringProduct('Whiskey Velho', tipe = 'bebida', cost = 10, price = 15, liter = 0.75, white = 1)
whiskey.save()
coca = CateringProduct('Coca-Cola', tipe = 'bebida', cost = 2, price = 2.1, liter = 2)
coca.save()
agua = CateringProduct('Água Natural', tipe = 'bebida', cost = 0.2, price = 0.3, liter = 1.5)
agua.save()
ice = CateringProduct('Ice-Tea', tipe = 'bebida', cost = 1.5, price = 1.6)
ice.save()

print("\nProdutos Criados\n\n")
print("\nApagar Produtos\n\n")
# del carne, peixe, sopa, r_carne, r_camarao, salada, pudim_f, pudim_c, whiskey, coca, agua, ice
print("\nProdutos Apagados\n\n")
print("\nCarregar Produtos\n\n")
carne = CateringProduct.load('Vitela Assada')
peixe = CateringProduct.load('Bacalhau Assado')
sopa = CateringProduct.load('Sopa Legumes')
r_carne = CateringProduct.load('Rissois Carne')
r_camarao = CateringProduct.load('Rissois Camarão')
salada = CateringProduct.load('Salada Fria')
pudim_f = CateringProduct.load('Pudim Flam')
pudim_c = CateringProduct.load('Pudim Caseiro')
whiskey = CateringProduct.load('Whiskey Velho')
coca = CateringProduct.load('Coca-Cola')
agua = CateringProduct.load('Água Natural')
ice = CateringProduct.load('Ice-Tea')
print("\nEditar Produtos\n\n")
ice.liter = 1.5
ice.save(overwrite = True)
agua.cost = 0.25
agua.save(overwrite = True)
print("\nProdutos Editados\n\n")

#WORKERS

print("\nCriar Trabalhadores\n\n")

leo = CateringWorker('Leonardo Bernardino', tipe = 'geral', cost = 6)
leo.save()
eira = CateringWorker('Nuno Eira', tipe = 'geral', cost = 0)
eira.save()
chico = CateringWorker('Francisco Sousa', tipe = 'geral', cost = 7)
chico.save()
sao = CateringWorker('Conceição Pires', tipe = 'cozinha', cost = 5)
sao.save()
raul = CateringWorker('Raul Ramos', tipe = 'cargas', cost = 5)
raul.save()
rosa = CateringWorker('Rosa Ambrósio', tipe = 'limpeza', cost = 5)
rosa.save()

print("\nTrabalhadores Criados\n\n")
print("\nApagar Trabalhadores\n\n")
del leo, eira
print("\nTrabalhadores Criados\n\n")
leo = CateringWorker.load('Leonardo Bernardino')
eira = CateringWorker.load('Nuno Eira')
print("\nEditar Trabalhadores\n\n")
eira.cost = 1
eira.save(overwrite = 1)
print("\nTrabalhadores Editados\n\n")

#SETS

print("\nCria Sets\n\n")
bar = CateringBar('Bar Ouro')
bar.setNumber(100)
bar.setObjects([whiskey, coca, agua])
bar.save()

course = CateringCourseMenu('Menu Ouro')
course.setNumber(100)
course.setObjects([carne, peixe, sopa, agua, coca])
course.save()

desserts = CateringDessertsMenu('Sobremesas Ouro')
desserts.setNumber(100)
desserts.setObjects([pudim_c, pudim_f])
desserts.save()


#NOME DA EQUIPA DEVE SER PARECIDO AO NOME DO SERVIÇO
team = CateringTeam('Equipa Serviço João')
team.setObjects([eira, leo, chico, sao, raul, rosa])
team.save()

print('\nSets Criados\n\n')
print('\nApagar Set\n\n')
del course
print('\nSet Removido\n\n')
print('\nCarregar Sets\n\n')
course = CateringCourseMenu.load('Menu Ouro')
print('\nEditar Sets\n\n')
course.setObjects(ice)
course.save(overwrite=True)
print('\nSet Editado\n\n')
print('\nAlterar Horas de Equipa\n\n')
team.addTeamHours(10)
team.addWorkerHours('Leonardo Bernardino', 5)
team.save(overwrite=True)
print('\nEquipa Alterada\n\n')
print(team.getWorkersHours())
print(team.getTotal())

print('\nCriar Serviço')
service = CateringService('Serviço João', 100)
service.setTableType('redonda')
service.date = str(date.today())
service.cups_n = 2
service.status = 'aberto'
service.extra_tables = 7
service.distance = 15
service.trips = 10
service.site = 'Valpaços'
service.setSets(course)
service.setSets(bar)
service.setSets(desserts)
service.setSets(team)
service.save()
service.getAssemblyPage()
service.getExtraProductsPage()
service.getTotalPage()



