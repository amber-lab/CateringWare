# -*- coding: utf-8 -*-
#!/usr/bin/env python
exec(open('G:/Working Dir/CateringCalculator/CateringItems.py','r').read())
exec(open('G:/Working Dir/CateringCalculator/CateringProduct.py','r').read())
exec(open('G:/Working Dir/CateringCalculator/CateringMenu.py','r').read())
exec(open('G:/Working Dir/CateringCalculator/CateringWorker.py','r').read())

carne = CateringProduct.load('Vitela Assada')
peixe = CateringProduct.load('Bacalhau com Broa')
sopa = CateringProduct.load('Sopa Legumes')

menu = CateringMenu('Aniversario')
menu.setProduct(carne)
menu.setProduct(peixe)
menu.setProduct(sopa)
menu.save()