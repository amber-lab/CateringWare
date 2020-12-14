# -*- coding: utf-8 -*-
#!/usr/bin/env python

"""
Created on Wed Feb 19 15:11:37 2020

@author: L.A.B
"""

class CateringPageLabeledEntry(tk.Frame):
    def __init__(self, master, text, photo, extra_label = str(), default_text = str(), on_default = True):
        tk.Frame.__init__(self, master, background = CINZA)
        self.on_default = on_default
        self.photo = photo
        self.label = tk.Label(self, text = text, image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        self.label.photo = self.photo
        self.label.place(relx = 0, rely = 0, relwidth = 0.6, relheight = 1)
        self.entry_v = tk.StringVar()
        self.entry = tk.Entry(self, textvariable = self.entry_v, font = MINI_FONT)
        self.entry.insert(0, default_text)
        self.entry.bind('<Button-1>', self.onClick)
        self.default = default_text
        if extra_label:
            self.entry.place(relx = 0.65, rely = 0, relwidth = 0.25, relheight = 1)
            self.extra_label = tk.Label(self, text = extra_label, image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
            self.extra_label.place(relx = 0.90, rely = 0, relwidth = 0.1, relheight = 1)
        else:
            self.entry.place(relx = 0.65, rely = 0, relwidth = 0.35, relheight = 1)
        
    def get(self):
        value = self.entry_v.get()
        float_val = value.split(',')
        if isinstance(float_val, list) and len(float_val) == 2:
            float_val = str('.').join(float_val)
            try:
                float_val = float(float_val)
            except ValueError:
                pass
            else:
                value = float_val
        if self.on_default:
            if value == self.default or value == str():
                raise CateringDefaultValue
            else:
                return value
        else:
            return value
    
    def onClick(self, event):
        if self.entry_v.get() == self.default and self.on_default:
            event.widget.delete(0, 'end')
    
    def setEntryValue(self, value):
        self.entry.delete(0, 'end')
        self.entry.insert(0, value)