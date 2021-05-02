# coding=UTF-8
from NameObject import *

class Tokens(object):

  """
   Части PDF файла

  :version:
  :author:
  """

  def __init__(self, str_list):
    """
     Сохраняет строку в классе

    @param str_list : список строк
    """
    self.data = ' '.join([self.delete_comment(s) for s in str_list])
    print(self.data)


  def delete_comment(self, s):
    """
    Удаляет комментарий, который начинается с % до конца строки
    "123 % ----"
    возвращает "123 "
    """
    if '%' in s:
      return s[:s.index('%')]
    else:
      return s
  
    
  def get(self):
    """
     Возвращает список токенов.
    num1 num2 R заменяет на кортеж ссылки (num1, num2)

    @return  :
    """
    l = []
    while self.data != '':
      l.append(self.get_token())
    return l

  
  def get_token(self):
    """
     Возвращает токен, удаляя его из data.
    Удаляет разделители.
    Анализирует первый символ.
    Цифра - число
    / - NameObject
    Буква - ключевое слово obj endobj stream endstream
    true/false - логическое значение
    null - None
    ( - literal string
    < - hex string
    << - словарь
    [ - массив
    @return  : token
    """
    self.skip_whitespace()
    if self.data == '':
      return None
    elif self.data[0].isdigit():
      return self.get_number()
    elif self.data[0] == '(':
      return self.get_literal_string()
    elif self.data[0] == '/':
      return self.get_name_object()
    elif self.data[:4] == 'true' or self.data[:5] == 'false':
      return self.get_boolean()
    elif self.data[:4] == 'null':
      return self.get_null()
    elif self.data[0].isalpha():
      return self.get_keyword()
    elif self.data[0:2] == '<<':
      tokens = Tokens(string).get()
      data = dict()
      for i in range(0, len(tokens), 2):
        data[tokens[i]] = tokens[i + 1]
      return data
    elif self.data[0] == '<':
      return self.get_hex_string()
    elif self.data[0] == '[':
      t = Tokens(self.get_array_string())
      return t.get()

    
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
        byk = ''
        num = ''
        i_last = 0
        for p in range(len(self.data)):
            if (self.data[p].isdigit()):
                i_last = p

        for i in range(len(self.data)):
            if not(self.data[i].isdigit()) and not(self.data[i] == '-' or self.data[i] == '+' or (self.data[i] == '.' and i < i_last)):
                byk = byk + self.data[i]

        for b in range(len(self.data)):
            if (self.data[b].isdigit()) or (self.data[b] == '-' or self.data[b] == '+' or (self.data[b] == '.' and b < i_last )):
                num = num + self.data[b]

        self.data = byk

        try:
            return int(num)
        except:
            return float(num)

  
  def get_boolean(self):
    """
     Извлекает true или false из строки.
    значение из строки удаляется

    @return  : true или false
    """
    i = 'true'
    a = 'false'
    if i in self.data:
      self.data = self.data.replace(i, '')
      return True
    if a in self.data:
      self.data = self.data.replace(a, '')
    return False


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
    st = self.data
    self.data = self.data[q+1:]
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
    c = 0
    y =0
    for i in range(len(self.data)):
      if self.data[i] == '<':
        c += 1
        x = i + 1
      if self.data[i] == '>':
        c -= 1
        y = i-1
      if c == 0:
        str2=self.data[2:y]
        self.data=self.data[y+2:]
        return str2

  
  def get_null(self):
    """
     Извлекает из data null
    @return  : значение None
    """
    self.data = self.data[4:]
    return None


  def get_name_object(self):
    """
     Извлекает из data name object 
    /Type
    /ASomewhatLongerName
    /1 . 2
    /lime#20Green
    /paired#28#29parentheses
    @return  : NameObject
    """
    name = ''
    n = 0
    if self.data[0] == '/':
      self.data = self.data.replace(self.data[0], '')
    for i in range(len(self.data)):
      if self.data[i] == '#':
        a = ''
        b = ''
        dec = ''
        a = self.data[i+1] + self.data[i+2]
        dec = int(a, base=16)
        b = chr(dec)
        name = name + b
        self.data = self.data.replace('#'+a, b)
        self.data = self.data + '  '
        n = n + 1
    self.data = self.data[:-2*n]
    return NameObject(name)


  def get_keyword(self):
    """
     Извлекает из data ключевое слово
    obj endobj stream endstream
    @return  : Keyword
    """
    pass  
  

if __name__ == '__main__':
#  t = Tokens(['/Type /Xref /Val 12 23'])
 # n = t.get_name_object()
#  print(n, t.data, '|', sep='|')
 # assert n == NameObject('Type')
 # assert t.data == ' /Xref /Val 12 23'
  t = Tokens(['1 1 1'])
  n = t.get_number()
  print(n, t.data, '|', sep='|')
  assert n == 1 and t.data == ' 1 1'
  t = Tokens(['true 32 true'])
  n = t.get_boolean()
  print(n, t.data, '|', sep='|')
  x = Tokens(['<901FA3>ffbbcc<11>'])
  n = x.get_hex_string()
  print(n, t.data, '|', sep='|')
  assert n == b'\x90\x1f\xa3'
  assert x.data == 'ffbbcc<11>'
