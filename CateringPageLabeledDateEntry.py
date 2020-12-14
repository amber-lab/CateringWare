# -*- coding: utf-8 -*-
#!/usr/bin/env python
"""
Created on Tue Mar 10 18:51:39 2020

@author: L.A.B
"""

class CateringPageLabeledDateEntry(tk.Frame):
    def __init__(self, master, text, photo):
        tk.Frame.__init__(self, master, background = CINZA)
        
        date = datetime.now()
        
        self.photo = photo
        self.label = tk.Label(self, text = text, image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        self.label.photo = self.photo
        self.label.place(relx = 0, rely = 0, relwidth = 0.6, relheight = 1)
        
        self.day_entry_var = tk.StringVar()
        self.month_entry_var = tk.StringVar()
        self.year_entry_var = tk.StringVar()
        
        self.day_entry = tk.Entry(self, textvariable = self.day_entry_var, font = MINI_FONT, justify = 'center')
        self.day_entry.insert(0, date.day)
        self.month_entry = tk.Entry(self, textvariable = self.month_entry_var, font = MINI_FONT, justify = 'center')
        self.month_entry.insert(0, date.month)
        self.year_entry = tk.Entry(self, textvariable = self.year_entry_var, font = MINI_FONT, justify = 'center')
        self.year_entry.insert(0, date.year)
        
        self.d_label = tk.Label(self, text = 'D', image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        self.m_label = tk.Label(self, text = 'M', image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        self.y_label = tk.Label(self, text = 'A', image = self.photo, compound = 'center', font = MINI_FONT, relief = 'raised')
        
        self.d_label.place(relx = 0.65, rely = 0, relwidth = 0.05, relheight = 1)
        self.day_entry.place(relx = 0.70, rely = 0, relwidth = 0.05, relheight = 1)
        
        self.m_label.place(relx = 0.75, rely = 0, relwidth = 0.05, relheight = 1)
        self.month_entry.place(relx = 0.80, rely = 0, relwidth = 0.05, relheight = 1)
        
        self.y_label.place(relx = 0.85, rely = 0, relwidth = 0.05, relheight = 1)
        self.year_entry.place(relx = 0.90, rely = 0, relwidth = 0.10, relheight = 1)
        
    def get(self):
        d = int(self.day_entry_var.get())
        m = int(self.month_entry_var.get())
        y = int(self.year_entry_var.get())
        try:
            entry_date = date(y, m, d)
            if entry_date == date.today() or entry_date < date.today():
                raise CateringDateError
        except ValueError:
            raise CateringDateError
        else:
            return str(entry_date)
    
    def setEntryValue(self, value):
        n = 0
        for entry in [self.year_entry, self.month_entry, self.day_entry]:
            entry.delete(0, 'end')
            entry.insert(0, value.split('-')[n])
            n += 1