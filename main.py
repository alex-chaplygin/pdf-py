from PDF import *
from tkinter import *
from tkinter import filedialog
import random


class Main:
    def __init__(self):
        self.window = Tk()
        self.window.title('PDF просмотр')
        self.window.geometry('500x500')
        self.canvas = Canvas(self.window, width=500, height=500)
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
            if type(elem[2]) == str:
                self.canvas.create_text(elem[0], elem[1], fill="black", font=(elem[3],elem[4]) ,text=elem[2])
            else:
                self.canvas.create_line(elem)
        self.i = PhotoImage(width=30, height=60)
        width = 30
        height = 60
        rgb_colors = ([random.randint(0,255) for i in range(0,3)] for j in range(0,width*height))
        pixels=" ".join(("{"+" ".join(('#%02x%02x%02x' %
            (0, 110, 130) for i in range(width)))+"}" for j in range(height)))
        self.i.put(pixels,(0, 0, width - 1, height-1))
        self.canvas.create_image(100, 100, image = self.i, anchor=NW)
        data = '''#define image_width 15
        #define image_height 15
        static unsigned char image_bits[] = {
        0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x38, 0x1c, 0x30, 0x0c, 0x60, 0x06,
        0x60, 0x06, 0xc0, 0x03, 0xc0, 0x03, 0x60, 0x06, 0x60, 0x06, 0x30, 0x0c,
        0x38, 0x1c, 0x00, 0x00, 0xa0, 0xa0 };'''

        self.bm = BitmapImage(data=data)
        self.canvas.create_image(200, 200, image = self.bm, anchor=NW)
        
    def next(self):
        self.page += 1
        self.pdf.getPage(self.page)


    def previous(self):
        self.page -= 1
        self.pdf.getPage(self.page)

        
main = Main()
main.run()
