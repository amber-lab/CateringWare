# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Sat Feb  8 15:54:57 2020

@author: L.A.B
"""

try:
    dir(os)
except NameError:
    import os

class HTMLWriter():
    def __init__(self, name, page_name):
        self.name = name
        username = os.environ['USERNAME']
        try:
            os.mkdir('C:\\Users\\{u}\\Desktop\\InventariosCatering'.format(u = username))
        except FileExistsError:pass
        try:
            os.mkdir('C:\\Users\\{u}\\Desktop\\InventariosCatering\\{n}'.format(n = self.name, u = username))
        except FileExistsError:pass
        self.file = open('C:\\Users\\{u}\\Desktop\\InventariosCatering\\{n}\\{pn}.htm'.format(n = self.name, pn = page_name, u = username), 'w+')
        self.file.write('<!DOCTYPE html>\n')
        self.file.write('<html>\n')
        self.file.write('<head>\n')
        self.file.write('<title>{t}</title>\n'.format(t = name))
        self.file.write('<style>\n')

        self.file.write('table {padding: 10px;}\n')
        self.file.write('table, th, td {padding: 15px; vertical-align:top;}\n')
        self.file.write('h2 {color:grey;}\n')
        self.file.write('</style>\n')
        self.file.write('</head>\n')
        self.file.write('<body>\n')
        self.addHeader(str(self.name), h = 'h1')
        self.addHeader(str(page_name), h = 'h2')
        self.addBreakRow()
        self.file.write('<div class = "clearfix">\n')

    def openDiv(self):
        self.file.write('<div>\n')
        
    def closeDiv(self):
        self.file.write('</div>\n')
        
    def openTable(self):
        self.file.write('<table>\n')
        
    def closeTable(self):
        self.file.write('</table>\n')
    
    def openRow(self):
        self.file.write('<tr>\n')
        
    def closeRow(self):
        self.file.write('</tr>\n')
    
    def openCell(self):
        self.file.write('<td>\n')
        
    def closeCell(self):
        self.file.write('</td>\n')
    
    def addHeader(self, text, h = 'h3'):
        self.file.write('<{h}>{t}</{h}>\n'.format(h = h, t = text))
        
    def addParagraph(self, text, p = 'p'):
        self.file.write('<{p}>{t}</{p}>\n'.format(p = p, t = text))

    def addBreakRow(self):
        self.file.write('<br>')

    def addTable(self, title, data):
        self.file.write('<table>\n')
        self.file.write('<tr>\n')
        for t in title:
            self.file.write('<th><b>{h}</b></th>\n'.format(h = t))
        self.file.write('</tr>\n')
        for tup in data:
            self.file.write('<tr>\n')
            for d in tup:
                self.file.write('<td>{d}</td>\n'.format(d = d))
            self.file.write('</tr>\n')
        self.file.write('</table>\n')

    def close(self):
        self.file.write('</div>\n')
        self.file.write('</body>')
        self.file.write('</html>')
        self.file.close()
        try:
            os.remove('C:\\Users\\L.A.B\\Desktop\\CateringCalculator\\Inventarios\\{n}\\debug.log'.format(n = self.name))
        except FileNotFoundError:pass
        except PermissionError:pass