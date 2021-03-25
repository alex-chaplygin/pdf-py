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
