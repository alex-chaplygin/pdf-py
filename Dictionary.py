# coding=UTF-8
from dictionary import *

class Dictionary(object):

  """
   <</Columns 5/Predictor 12>>

  :version:
  :author:
  """

  """ ATTRIBUTES

   словарь из токен

  data  (private)

  """
  def __init_(self, string):
    """
    Создается словарь на основе строки string.
    Строка разбивается на токены (Класс Tokens)
    Пары ключ значение добавляются в data
    Ключи из NameObject преобразуются в string
    """
    tokens = Tokens(string).get()
    self.data = dict()
    for i in range(0, len(tokens), 2):
      self.data[tokens[i]] = tokens[i + 1]


