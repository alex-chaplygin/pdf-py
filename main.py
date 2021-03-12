from PDF import *
from tkinter import *
from tkinter import filedialog
window = Tk()
window.title('Test1')
window.geometry('500x500')
canvas = Canvas(width=500, height=500)
canvas.grid(column=0, row=0)
file = filedialog.askopenfilenames()
pdf = PDF(file)
for elem in pdf.getPage(1):
    canvas.create_line(elem)
menu = Menu(window)
window.config(menu=menu)


def fileOpen():
    pdf.getPage(1)


menu.add_command(label='Открыть', command=fileOpen)
menu.add_command(label='Контакты')
window.mainloop()
