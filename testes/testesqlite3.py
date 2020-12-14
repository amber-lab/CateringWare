#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 13 16:40:30 2019

@author: L.A.B
"""
import sqlite3

conn = sqlite3.connect('CateringDB.db')

#CREATE TABLE
#conn.execute("CREATE TABLE WORKERS (ID INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, COST REAL NOT NULL);")

#INSERT
#conn.execute("INSERT INTO WORKERS(NAME, COST) VALUES ('Chico Sousa', 7)")

#UPDATE
#conn.execute("UPDATE WORKERS SET cost = 5 WHERE ID = 1;")

#DELETE
#conn.execute("DELETE FROM WORKERS WHERE NAME = 'Chico Sousa';")

#SELECT
cursor = conn.execute("SELECT NAME, ID, COST FROM WORKERS")
for row in cursor.fetchall():
   print("NAME = ", row[0])
   print("ID = ", row[1])
   print("SALARY = ", row[2])
   
#conn.commit()
conn.close()