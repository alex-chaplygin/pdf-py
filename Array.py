# coding=UTF-8
from Tokens import *

class Array(object):

  """
   [112 12 334]

  :version:
  :author:
  """

  """ ATTRIBUTES

   список токенов

  data  (private)

  """

  def __init__(self, string):
    """
    Инициализирует массив
    string - строка массива преобразуется в список лексем используя класс Tokens
    """
    self.array = Tokens(string).get()



