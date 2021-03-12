# coding=UTF-8

class PDF(object):

  """
   Содержит все данные из PDF файла

  :version:
  :author:
  """

  def __init__(self, filename):
    """
     Читает PDF файл, загружает все данные

    @param string filename : имя файла
    @return  :
    @author
    """
    print(filename)
    f = open(filename[0], 'rb')
    self.data = f.read()
    f.close()

  def getPage(self, page):
    """
     Возвращает список графических примитивов

    @param int page : номер страницы
    @return list :
    @author
    """
    print(self.data)
    lines = [(0, 0, 500, 500), (70, 100, 350, 200), (20, 460, 400, 10,), (150, 100, 400, 80)]
    return lines



