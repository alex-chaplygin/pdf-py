from PDF import *
from tkinter import *
from tkinter import filedialog


class Main:
    def __init__(self):
        self.window = Tk()
        self.window.title('Test1')
        self.window.geometry('500x500')
        self.canvas = Canvas(width=500, height=500)
        self.canvas.grid(column=0, row=0)
        menu = Menu(self.window)
        self.window.config(menu=menu)
        menu.add_command(label='Открыть', command=self.open)
        menu.add_command(label='Предыдущая страница', command=self.next)
        menu.add_command(label='Следующая страница', command=self.previous)
        self.page=1
        self.pdf = None

        
    def run(self):
        self.open()
        self.window.mainloop()


    def open(self):
        (file, ) = filedialog.askopenfilenames()
        self.pdf = PDF(file)
        for elem in self.pdf.get_page(1):
            self.canvas.create_line(elem)

        
    def next(self):
        self.page += 1
        self.pdf.getPage(self.page)


    def previous(self):
        self.page -= 1
        self.pdf.getPage(self.page)

        
main = Main()
main.run()
