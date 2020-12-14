# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Wed Oct  2 12:08:56 2019

@author: L.A.B
"""

import sqlite3
from os import chdir
chdir('C:/Users/L.A.B/Desktop/CateringCalculator')
exec(open('CateringItems.py','r', encoding = 'utf-8').read())
exec(open('CateringProduct.py','r', encoding = 'utf-8').read())
exec(open('CateringSet.py','r', encoding = 'utf-8').read())
exec(open('CateringWorker.py','r', encoding = 'utf-8').read())
exec(open('CateringService.py','r', encoding = 'utf-8').read())

conn = sqlite3.connect('CateringDB.db')
query = "DELETE FROM {t} WHERE ID > 0;"
tabelas = ['WORKERS','PRODUCTS','SETS', 'SETSPRODUCTS', 'SERVICES']
for tabela in tabelas:
    conn.execute(query.format(t=tabela))

print("Executado")
conn.commit()
conn.close()
