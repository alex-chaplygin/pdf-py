# coding=UTF-8
from Tokens import *

class PDF(object):

  """
   Содержит все данные из PDF файла
  """

  def __init__(self, filename):
    """
     Читает PDF файл, загружает все данные
    Заголовок - версия %PDF-1.4
    Тело - список объектов
    Таблица ссылок
    Окончание - trailer Словарь startxref ссылка %%EOF

    @param string filename : имя файла
    """
    print(filename)
    self.f = open(filename, 'rb')
    self.f.seek(-1, 2)
    xref = self.get_xrefpos()
    print('xrefpos', xref)
    self.f.seek(xref)
    obj = self.read_object()


  def read_object(self):
    """
    читает один объект PDF
    """
    s = ''
    ls = []
    while not 'stream' in s:
      s = self.read_string()
      ls.append(s)
    t = Tokens(ls)
    print(t.get())
    
  def get_page(self, page):
    """
     Возвращает список графических примитивов

    @param page : номер страницы
    @return : список графических примитивов
    """
    lines = [(0, 0, 500, 500), (70, 100, 350, 200), (20, 460, 400, 10,), (150, 100, 400, 80)]
    return lines


  def get_version(self):
    """
     Возвращает версию PDF как строку
    self.data - данные из файла
    Алгоритм:
    разбить данные на строки
    из первой строки извлечь версию
    удалить первую строку из списка строк
    """
    pass

  
  def parse_objects(self):
    """
    выделяет из данных строки байт
    преобразует данные файла в список токенов (класс Tokens)
    пока не встретится Keyword('xref')
    создает словарь из объектов (objects)
    ключ (номер_объекта, номер поколения)
    значение - данные объекта (токен)
    """
    pass

  
  def get_xrefpos(self):
    """
    получает и возвращает позицию таблицы ссылок
    """
    lst = []
    pos = 5
    for i in range(pos):
        lst = [self.read_string_reverse()] + lst
    for i in range(len(lst)):
        if lst[i] == 'startxref':
            return int(lst[i + 1])

          
  def read_string_reverse(self):
    """
    читает строку задом наперед с текущей позиции в файле
    возвращает прочитанную строку
    """
    data = b''
    b = b''
    while b != b'\n' and b != b'\r':
        b = self.f.read(1)
        data = b + data
        self.f.seek(-2, 1)
#    print(f.tell())
    while b == b'\n' or b == b'\r':
        b = self.f.read(1)
        self.f.seek(-2, 1)
  #  print(f.tell())
    self.f.seek(1, 1)
    return ''.join([chr(c) for c in data]).strip()


  def read_string(self):
    """
    читает строку начиная с текущей позиции в файле
    возвращает строку
    """
    data = b''
    b = b''
    while b != b'\n' and b != b'\r':
        b = self.f.read(1)
        data = data + b
    while b == b'\n' or b == b'\r':
        b = self.f.read(1)
    self.f.seek(-1, 1)
    return ''.join([chr(c) for c in data]).strip()


  def read_stream(self):
    """
    читает и возвращает поток байт между stream и endstream
    """
    data = b''
    b = b''
    while data[-9:] != b'endstream':
        b = self.f.read(1)
        data = data + b
    return data[:-9].strip()
