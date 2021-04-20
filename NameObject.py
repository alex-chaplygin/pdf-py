# coding=UTF-8

class NameObject(object):

  """
   /Index

  :version:
  :author:
  """

  """ ATTRIBUTES

   имя без слэша

  name  (private)

  """
  def __init__(self, string):
    """
    Инициализирует имя
    string - строка имени без слэша
    #xx - заменяется как символ с 16-ричным кодом
    """
    self.data = string


  def __repr__(self):
    """
    представление объекта в виде строки
    """
    return '/' + self.data


  def __eq__(self, other):
    """
    метод сравнения объектов
    """
    return self.data == other.data


  def __hash__(self):
    return hash(self.data)
