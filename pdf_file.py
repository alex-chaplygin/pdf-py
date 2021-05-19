'''
Работа с PDF файлом
'''
import tokens
import pdf_parser as parser
from NameObject import *
from Object import *


# Файловый объект PDF файла
pdf_file = None
# версия файла
version = None
# словарь загруженных объектов
# ключ - ссылка (11, 0), значение - объект Object
objects = {}
# таблица ссылок, содержит записи ()
xref_table = []
# ссылка на корневой объект - начало документа (ссылка (1, 0))
root_ref = None
# словарь трейлера
trailer = {}


def get_char():
    '''
    Читает и возвращает один символ из файла из текущей позиции
    '''
    return chr(get_bytes(1)[0])


def get_bytes(num):
    '''
    Читает и возвращает байты из файла из текущей позиции

    num - число байт
    возвращает: байтовая строка 
    '''
    return pdf_file.read(num)


def load(file_name):
    '''
    Загружает заголовок и таблицу ссылок PDF файла

    file_name - имя файла
    Если файл был открыт, то закрывает файл
    Загружает заголовок, трейлер и таблицу ссылок.
    Загрузка корневого объекта
    '''
    global pdf_file
    global version
    if pdf_file != None:
        close(pdf_file)
    tokens.get_char = get_char
    parser.get_bytes = get_bytes
    pdf_file = open(file_name, 'rb')
    version = load_header()
    xref_pos = load_xrefpos()
    pdf_file.seek(xref_pos)
    load_xref_table()
    load_trailer()


def load_xref_stream():
    '''
    Загружает таблицу ссылок из потока (второй вариант)

    12 0 obj
    << /Type /XRef
          /Size количество объектов
          /Index [начальный объект, конечный объект]
         /Root (1, 0) - ссылка на корневой объект
         /W [1, 2, 1] - размеры полей в байтах
    >>
      stream
      таблица
      endsream
    endobj
    '''
    global xref_table
    global root_ref
    global objects
    obj = parser.parse_object()
    objects[(obj.num1, obj.num2)] = obj
    if obj.get('Type') != NameObject('XRef'):
        raise Exception('Not XRef')
    size = obj.get('Size')
    root_ref = obj.get('Root')
    if NameObject('Index') in obj.data:
        i = obj.get('Index')
        index = (i[0], i[1])
    else:
        index = (0, size)
    w = obj.get('W')
    xref_table.clear()
    pos = 0
    for i in range(0, len(obj.stream), sum(w)):
        entry = [0, 0, 0] # 0 12 12 10
        for j in range(3):
            offset = 0
            for k in range(w[j]): 
                offset = offset << 8
                offset += obj.stream[pos]
                pos += 1
            entry[j] = offset
        xref_table.append(tuple(entry))


def load_xref_table():
    '''
    Загружает таблицу ссылок

    xref - первый вариант таблицы
    0 6 - первый и последний номера объектов
    offset generation n - занятый объект
    offset generation f - свободный объект
    ...
    '''
    global xref_table
    global root_ref
    global objects
    tokens.cur_char = tokens.get_char()
    parser.cur_token = tokens.get_token()
    if parser.cur_token != ('id', 'xref'):
        load_xref_stream()
    else:
        pass
        #raise Exception('Первый вариант таблицы ссылок')
    

def load_header():
    '''
    Загружает заголовок PDF

    Первая строка файла %PDF-1.номер
    Возвращает номер версии: 1.0 - 1.7
    '''
    pass


def load_xrefpos():
    '''
    Загружает позицию таблицы ссылок

    startxref
    ссылка на таблицу ссылок
    %%EOF
    Возвращет позицию таблицы ссылок
    '''
    pdf_file.seek(-1, 2)
    lst = []
    s = ''
    while s != 'startxref':
        s = read_string_reverse()
        lst = [s] + lst
    for i in range(len(lst)):
        if lst[i] == 'startxref':
            return int(lst[i + 1])


def load_trailer():
    '''
    Загружает трейлер

    trailer
    <<
    /Root 1 0 R
    ...
    >>
    '''
    global trailer
    global root_ref
    if root_ref != None:
        return # no trailer
    tokens.cur_char = tokens.get_char()
    parser.cur_token = tokens.get_token()
    while parser.cur_token != ('<<',):
        parser.cur_token = tokens.get_token()
    trailer = parser.parse_data()
    root_ref = trailer['Root']

        
def read_string_reverse():
    """
    читает строку задом наперед с текущей позиции в файле

    возвращает прочитанную строку
    """
    data = b''
    b = b''
    while b != b'\n' and b != b'\r':
        b = pdf_file.read(1)
        data = b + data
        pdf_file.seek(-2, 1)
#    print(f.tell())
    while b == b'\n' or b == b'\r':
        b = pdf_file.read(1)
        pdf_file.seek(-2, 1)
  #  print(f.tell())
    pdf_file.seek(1, 1)
    return ''.join([chr(c) for c in data]).strip()

        

def get_object(ref):
    '''
    Загружает объект PDF

    ref - ссылка на объект: (12, 0)
    Если объект есть в словаре, то объект берется оттуда
    иначе загружает объект из файла (parse_object)
    установка позиции из таблицы
    установка текущего символа (cur_char)
    установка текущей лексемы (cur_token)
    Возвращает объект Object
    '''
    global objects
    pass


def set_object_pos(ref):
    '''
    Установка позиции для чтения объекта

    ref - ссылка на объект
    первый номер объекта - индекс в таблице ссылок
    Элемент таблицы: (тип, значение1, значение2)
    тип = 0 - свободный
              1 - обычный объект
              2 - сжатый объект
    если тип свободный - то исключение
    если тип 1, то значение1 - смещение в файла
    если тип 2, то значение1 - номер объекта с сжатыми объектами
                            значение2 - индекс
    '''
    pass


def get_content_stream_object(obj_num, index):
    pass


if __name__ == '__main__':
    from sys import argv
    load(argv[1])
    print('Version:', version)
    print('objects:', objects)
    print('trailer:', trailer)
    print('root:', root_ref)
    print('xref_table:', xref_table)
