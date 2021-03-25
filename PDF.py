# coding=UTF-8

class PDF(object):

  """
   Содержит все данные из PDF файла
  """

  def __init__(self, filename):
    """
     Читает PDF файл, загружает все данные

    @param string filename : имя файла
    """
    print(filename)
    f = open(filename[0], 'rb')
    self.data = f.read()
    f.close()
    self.version = self.get_version()
    print(self.version)

  def get_page(self, page):
    """
     Возвращает список графических примитивов

    @param page : номер страницы
    @return : список графических примитивов
    """
    print(self.data)
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
    преобразует данные файла в список токенов (класс Tokens)
    создает словарь из объектов (objects)
    ключ (номер_объекта, номер поколения)
    значение - данные объекта (токен)
    """
    pass

  def set_indirect(self):
    """
    Во всех объектах (словари в Stream) заменяет ссылки в значениях словарей на значения из объектов (objects)
    ссылка 12 0 R
    """
    pass
  
