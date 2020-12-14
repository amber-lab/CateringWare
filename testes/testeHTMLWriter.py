# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 21:46:11 2020

@author: L.A.B
"""
lista = [('nuno', 15, 1), ('leonardo', 15, 5), ('chico', 10, 5)]
writer = HTMLWriter('teste')
writer.addHeader(text = 'HEADER')
writer.addParagraph('paragrafo 1')
writer.addBreakRow()
writer.addParagraph('paragrafo 2 com break row')
writer.addParagraph('paragrafo 3 bold', p = 'b')
writer.addTable(('nome', 'horas', 'custo'), lista)
writer.close()