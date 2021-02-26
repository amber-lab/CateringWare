# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Mon Nov 25 11:06:08 2019

@author: L.A.B
"""
import sqlite3

class CateringDBManager():
    def save(db_info, data):
        conn = sqlite3.connect('CateringDB.db')
        query = "INSERT INTO {t} ({c}) VALUES {v}".format(t = db_info['table'], c = ', '.join(db_info['columns']), v = data)
        conn.execute(query)
        conn.commit()
        conn.close()
        return True
        
    def load(db_info, name, like = False, id_list = False, where_column = '', operator = ''):
        conn = sqlite3.connect('CateringDB.db')
        query = ''
        if like and where_column:
            query = "SELECT {c} FROM {t} WHERE {wc} LIKE '{n}%'".format(c = ', '.join(db_info['columns']), t = db_info['table'], n = name, wc = where_column)
        elif like:
            query = "SELECT {c} FROM {t} WHERE NAME LIKE '{n}%'".format(c = ', '.join(db_info['columns']), t = db_info['table'], n = name)
        elif where_column:
            query = "SELECT {c} FROM {t} WHERE {wc} = '{n}'".format(c = ', '.join(db_info['columns']), t = db_info['table'], n = name, wc = where_column)
        elif isinstance(name, int):
            query = "SELECT {c} FROM {t} WHERE ID = {n}".format(c = ', '.join(db_info['columns']), t = db_info['table'], n = name)
        elif isinstance(name, str):
            query = "SELECT {c} FROM {t} WHERE NAME = '{n}'".format(c = ', '.join(db_info['columns']), t = db_info['table'], n = name)
        if operator:
            query += " {}".format(operator)
        cursor = conn.execute(query)
        if like or where_column or id_list:
            data = cursor.fetchall()
        else:
            data = cursor.fetchone()
        conn.commit()
        conn.close()
        if data:
            return data
        else:
            raise CateringObjectNotFound

    def delete(db_info, data, operator = ''):
        conn = sqlite3.connect('CateringDB.db')
        query = "DELETE FROM {t} WHERE ID = {i}".format(t = db_info['table'], i = data[0])
        if operator:
            query += ' {}'.format(operator)
        conn.execute(query)
        conn.commit()
        conn.close()
        return True
        
    def update(db_info, data, operator = ''):
        conn = sqlite3.connect('CateringDB.db')
        data_str = ''
        for n in range(len(db_info['columns']) - 1):
            if data_str:
                data_str += ', '
            if isinstance(data[n+1], str):
                data_str += db_info['columns'][n+1] + " = '" + str(data[n+1]) + "'"
            else:
                data_str += db_info['columns'][n+1] + ' = ' + str(data[n+1])
        query = "UPDATE {t} SET {d} WHERE ID = {i}".format(t = db_info['table'], d = data_str, i = data[0])
        if operator:
            query += ' {}'.format(operator)
        conn.execute(query)
        conn.commit()
        conn.close()
        return True
        
    def getMaxID(table):
        conn = sqlite3.connect('CateringDB.db')
        query = "SELECT MAX(ID) FROM {t}".format(t = table)
        cursor = conn.execute(query)
        maxID = cursor.fetchone()[0]
        if maxID:
            return maxID + 1
        else:
            return 1
    
        
CateringDBManager.db_info = {'products' : {'table' : 'PRODUCTS', 'columns' : ('ID', 'NAME', 'TYPE', 'COST', 'PRICE', 'LITER', 'WHITE', 'UNI', 'UNI_N')},
                            'sets' : {'table' : 'SETS', 'columns' : ('ID', 'NAME', 'TYPE')},
                            'setsproducts' : {'table' : 'SETSPRODUCTS', 'columns' : ('ID', 'PRODUCTID', 'HOURS')},
                            'workers' : {'table' : 'WORKERS' , 'columns' : ('ID', 'NAME', 'COST', 'TYPE')},
                            'services' : {'table' : 'SERVICES', 'columns' : ('ID', 'NAME', 'DATE', 'NUMBER', 'STATUS', 'CUPS', 'TABLES_TYPE', 'EXTRA_TABLES', 'TRIPS', 'DISTANCE', 'SITE', 'MENU', 'BAR', 'APPETIZERS', 'DESSERTS', 'TEAM', 'APT_L', 'DST_L')}}