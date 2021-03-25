# coding=UTF-8
from list import *

class Stream(object):

  """
   stream
   endstream

  :version:
  :author:
  """

  """ ATTRIBUTES

   stream - список байт

  dictionary - словарь атрибутов

  """
  def __init__(self, dictionary, stream):
    """
    Создает объект Stream на основе словаря dictionary и строки байт stream
    В словаре по ключу /Length проверяется длина потока
    """
    pass

  def decode(self):
    """
    Декодирует поток в зависимости от /Filter
    Если есть /DL то проверяется длина декодированной строки
    @return : декодированная строка
    """
    pass

  def decode_lzw(self):
    """
    @return : декодированная строка
    """
    pass

  def decode_ascii85(self):
    """
    @return : декодированная строка
    """
    pass
  
  def decode_flate(self):
    """
    @return : декодированная строка
    """
    pass

  def decode_runlength(self):
    """
    @return : декодированная строка
    """
    pass

  def decode_ccitt(self):
    """
    @return : декодированная строка
    """
    pass
  
  def decode_jbig2(self):
    """
    @return : декодированная строка
    """
    pass

  def decode_dct(self):
    """
    @return : декодированная строка
    """
    pass
