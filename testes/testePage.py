import tkinter as tk

exec(open('CateringPage.py', 'r', encoding = 'utf-8').read())

app = tk.Tk()
tst = CateringPage(app)
tst.pack()

app.mainloop()