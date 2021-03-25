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
     Возвращает список токенов.
    Удаляет комментарии, которые начинаются с % до конца строки

    @return  :
    """
    pass

  def skip_whitespace(self):
    """
     Удаляет из строки разделители \x00 \x09 \x0a \x0c \x0d \x20 

    """
    pass  
  
  def get_number(self):
    """
     Извлекает число из строки.
    Примеры чисел: 123 43445 +17 -98 0
    Вещественные: 34.5 -3.62 +123.4 4. -0.002 0.0
    Число из строки удаляется

    @return  : int или float число
    """
    pass

  def get_boolean(self):
    """
     Извлекает true или false из строки.
    значение из строки удаляется

    @return  : true или false
    """
    pass


  def get_literal_string(self):
    """
     Извлекает строку в скобках из строки.
    Примеры:
    (111 22 33 44)
    Strings may contain newlines
    and such .)
    ( Strings may contain balanced parentheses ( ) and
    special characters ( * ! & } ^ % and so on ) . )
    (The following is an empty string .)
    ()
    (It has zero ( 0 ) length .)
    Последовательности внутри строк \n \r \t \b \f \( \) \\ \ddd (восьмиричный код)
    ( These \
    two strings \
    are the same . )
    ( These two strings are the same . )
    ( This string contains \245two octal characters\307 . )
    the literal
    ( \0053 )
    denotes a string containing two characters, \005 (Control-E) followed by the digit 3, whereas both
    ( \053 )
    and
    ( \53 )
    denote strings containing the single character \053, a plus sign (+).
    значение из строки удаляется

    @return  : строка
    """
    pass
  
  def get_hex_string(self):
    """
     Извлекает строку в скобках из строки.
    Примеры: <901FA3>
    @return  : байтовая строка
    """
    pass
