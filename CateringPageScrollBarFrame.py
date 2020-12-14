# -*- coding: utf-8 -*-
"""
Created on Wed Nov 20 09:35:54 2019

@author: L.A.B
"""

class CateringPageScrollBarFrame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)            
        
        vscrollbar = tk.Scrollbar(self, orient='vertical')
        vscrollbar.pack(fill = 'y', side = 'right', expand = False)
        canvas = tk.Canvas(self, bd = 0, highlightthickness = 0, yscrollcommand = vscrollbar.set)
        canvas.pack(side = 'left', fill = 'both', expand = 'True')
        vscrollbar.config(command=canvas.yview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.interior = tk.Frame(canvas, **kwargs)
        interior_id = canvas.create_window((0, 0), window=self.interior, anchor='nw')
        
        def _configure_interior(event):
            canvas.config(scrollregion=canvas.bbox('all'))
            canvas.config(height = self.interior.winfo_reqheight(), width = self.interior.winfo_reqwidth())
            if self.interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=self.interior.winfo_reqwidth(), height = self.interior.winfo_reqheight())
        
        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
                
        canvas.bind('<Configure>', _configure_canvas)

        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/60)), 'units')
            except:pass
        self.interior.bind("<MouseWheel>", _on_mousewheel)