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
     Сохраняет строку в классе

    @param list data : данные 
    """
    self.data = data

    
  def get(self):
    """
     Возвращает список токенов.
    Удаляет комментарии, которые начинаются с % до конца строки
    num1 num2 R заменяет на кортеж ссылки (num1, num2)

    @return  :
    """
    pass

  
  def get_token(self):
    """
     Возвращает токен, удаляя его из data.
    Удаляет разделители.
    Анализирует первый символ.
    Цифра - число
    / - NameObject
    Буква - ключевое слово (в виде строки) obj endobj stream endstream
    true/false - логическое значение
    null - None
    ( - literal string
    < - hex string
    << - словарь
    [ - массив
    @return  : token
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
    c = 0
    for i in range(len(self.data)):
      if self.data[i] == '(':
	c += 1
	x = i + 1
      if self.data[i] == ')':
        c -= 1
	y = i
      if c == 0:
	return self.data[1:y]

      
  def get_hex_string(self):
    """
     Извлекает строку в скобках из строки.
    значение из строки data удаляется
    Примеры: <901FA3> Возвращает b'\x90\x1f\xa3'
    @return  : байтовая строка
    """
    for i in range (len(self.data)):
		if self.data[i] == '<':
			z = i + 1  
		if self.data[i] == '>':
			q = i
    s = self.data[1:q] 
    ste = []
	
    for i in range(0, len(s), 2):
      x = int(s[i:i+2], 16)
      ste.append(x)
    return bytes(ste)

  
  def get_array_string(self):
    """
     Извлекает строку в скобках из строки. Внутренние скобки включаются в строку
    массив из строки data удаляется
    Примеры: [1 2 3 4] Возвращает "1 2 3 4"
                     [ [1]  [2] ] Возвращает " [1] [2] "
    @return  : строка массива
    """
    pass

  
  def get_dictionary_string(self):
    """
     Извлекает строку словаря из строки. Внутренние скобки включаются в строку
    словарь из строки data удаляется
    Примеры: << /Name 1 >>          Возвращает " /Name 1 "
                     << /Name 1
                         /Dict << /M 2 >>
                     >> Возвращает " /Name 1
                         /Dict << /M 2 >> "
    @return  : строка словаря
    """
    pass

  
  def get_null(self):
    """
     Извлекает из data null
    @return  : значение None
    """
    pass  
