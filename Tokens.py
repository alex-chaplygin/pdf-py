# coding=UTF-8
from list import *

class Tokens(object):

  """
   Части PDF файла

  :version:
  :author:
  """

  def __init__(self, data):
    """
     Сохраняет строку (список байт) в классе

    @param list data : данные (список байт)
    """
    pass

  def get(self):
    """
     Возвращает список токенов

    @return  :
    """
    pass


  def getNumber(self):
    """
     Извлекает число из строки.
    Число из строки удаляется

    @return  : int или float число
    """
    pass

  def getBoolean(self):
    """
     Извлекает true или false из строки.
    значение из строки удаляется

    @return  : true или false
    """
    pass


  def getString(self):
    """
     Извлекает строку в скобках из строки.
    (111 22 33 44)
    значение из строки удаляется

    @return  : строка
    """
    pass
  
