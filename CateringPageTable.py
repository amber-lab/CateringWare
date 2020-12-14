# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Thu Mar 12 16:54:55 2020

@author: L.A.B
"""

class CateringPageTable(tk.Frame):
    def __init__(self, master, photo, color, headers, **kwargs):
        # HEADERS = LISTA DE NOMES
        super().__init__(master, borderwidth = 5, background = color, **kwargs)
        self.color = color
        self.headers = headers
        self.widgets = {}
        
        self.scrollbar = tk.Scrollbar(self, orient = 'vertical', background = color, command = self.moveLists)
        self.scrollbar.place(relx = 0.95, rely = 0.3, relwidth = 0.05, relheight = 0.7)
        
        x = 0
        w = 0.95 / len(self.headers)
        
        for header in self.headers:
            title = CateringPageTitleLabel(self, header, photo, MEDIUM_FONT)
            title.place(relx = x, rely = 0, relwidth = w, relheight = 0.3)
            listbox = tk.Listbox(self, yscrollcommand = self.scrollbar.set, selectforeground = 'black', selectbackground = color, font = MINI_FONT, selectmode = 'multiple')
            listbox.bind('<MouseWheel>', self.onMouseWheel)
            listbox.bind('<ButtonRelease-1>', self.onClick)
            listbox.bind('<ButtonRelease-3>', self.delValues)
            listbox.place(relx = x , rely = 0.3, relwidth = w, relheight = 0.7)
            self.widgets[header] = listbox
            x += w
        
    def setValues(self, values):
        # values = dict
        for item, value in values.items():
            self.widgets[item].insert('end', value)
    
    def moveLists(self, *args):
        for widget in self.widgets.values():
            widget.yview(*args)

    def onMouseWheel(self, event):
        for widget in self.widgets.values():
            widget.yview_scroll(int(-1 * event.delta / 60), "units")
        return "break"

    def onClick(self, event):
        widget = event.widget
        try:
            selection = widget.curselection()
        except:
            pass
        else:
            for widget in self.widgets.values():
                for item in range(widget.size()):
                    widget.itemconfig(item, background = 'white')
            for widget in self.widgets.values():
                for value in selection:
                    widget.itemconfig(value, background = self.color)
    
    def delValues(self, event):
        widget = event.widget
        try:
            selection = widget.curselection()
        except:
            pass
        else:
            for widget in self.widgets.values():
                widget.delete(selection)
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            