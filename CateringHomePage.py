# -*- coding: utf-8 -*-
#!/usr/bin/env python

class CateringHomePage(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.photo = ImageTk.PhotoImage(BG_CINZA)
        
        self.img = Image.open('HomePageBG.png')
        self.img_copy = self.img.copy()
        
        self.bg_photo = ImageTk.PhotoImage(self.img)
        
        self.background = tk.Label(self, image = self.bg_photo)
        self.background.photo = self.bg_photo
        self.background.bind('<Configure>', self.imageResize)
        self.background.place(relx = 0, rely = 0, relheight = 1, relwidth = 1)
        
        title = CateringPageTitleLabel(self, 'CateringWare Casa Da Eira', self.photo)
        title.place(relx = 0.05, y = 50, relwidth = 0.9, height = 60)
        services_separator = CateringPageTitleLabel(self, 'Proximos Serviços', self.photo)
        services_separator.place(relx = 0.1, y = 130, relwidth = 0.8, height = 30)
        
        try:
            today_date = str(date.today())
            data = CateringService.load('', like = True, operator = "AND DATE > {} AND STATUS = 'aberto'".format(today_date))
            dates = []
            for row in data:
                data = row[2]
                if data not in dates:
                    dates.append(row[2])
            dates = sorted(dates, key = lambda d: tuple(map(int, d.split('-'))))
            dates = dates[:5]
            objs = []
            for dat in dates:
                data = CateringDBManager.load(CateringDBManager.db_info['services'], name = dat, where_column = 'DATE')
                if isinstance(data, list):
                    for dat in data:
                        objs.append((dat[1], dat[2], dat[10]))
                else:
                    obj.append(data[1], data[2], data[10])
            y = 180
            if objs:
                for obj in objs:
                    info = CateringPageInfoLabel(self, obj[0], CINZA_ESCURO, default_text = str(obj[1] + " / " + obj[2]), font = MEDIUM_FONT)
                    info.place(relx = 0.15, y = y, relwidth = 0.7, height = 30)
                    y += 50
        except CateringObjectNotFound:
            label = tk.Label(self, text = 'Proximos serviços serão apresentados aqui.', background = CINZA_ESCURO, font = MEDIUM_FONT)
            label.place(relx = 0.15, y = 180, relwidth = 0.7, height = 100)
            
    def imageResize(self, event):
        width = event.width
        height = event.height
        
        self.img = self.img_copy.resize((width, height), Image.ANTIALIAS)
        
        self.bg_photo = ImageTk.PhotoImage(self.img)
        self.background.config(image = self.bg_photo)
        
        
        
        
                