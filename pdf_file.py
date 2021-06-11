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

# тип объекта
FREE = 0
NORMAL = 1
COMPRESSED = 2
# таблица ссылок, содержит записи ()
#   ключ: номер объекта
#    Элемент таблицы: (тип, значение1, значение2)
#   тип = FREE - свободный
#              NORMAL - обычный объект
#              COMPRESSED - сжатый объект
#    если тип свободный - то исключение
#    если тип NORMAL, то значение1 - смещение в файла
#    если тип COMPRESSED, то значение1 - номер объекта с сжатыми объектами
#                            значение2 - индекс
xref_table = {}
# ссылка на корневой объект - начало документа (ссылка (1, 0))
root_ref = None
# словарь трейлера
trailer = {}
# позиция при считывании из потока объекта
stream_pos = 0


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
    Загружает заголовок, таблицу ссылок и трейлер.
    '''
    global pdf_file
    global version
    global objects
    global root_ref
    if pdf_file != None:
        pdf_file.close()
        xref_table.clear()
        objects.clear()
        root_ref = None
    tokens.get_char = get_char
    parser.get_bytes = get_bytes
    pdf_file = open(file_name, 'rb')
    version = load_header()
    xref_pos = load_xrefpos()
    pdf_file.seek(xref_pos)
    load_xref_table()


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
    #print(obj, len(obj.stream))
    objects[(obj.num1, obj.num2)] = obj
    if obj.get('Type') != NameObject('XRef'):
        raise Exception('Not XRef')
    size = obj.get('Size')
    root_ref = obj.get('Root')
    if 'Index' in obj.data:
        i = obj.get('Index')
        index = (i[0], i[1])
    else:
        index = (0, size)
    w = obj.get('W')
    pos = 0
    for i in range(index[1]):
        entry = [0, 0, 0] # 0 12 12 10
        for j in range(3):
            offset = 0
            for k in range(w[j]): 
                offset = offset << 8
                offset += obj.stream[pos]
                pos += 1
            entry[j] = offset
        xref_table[index[0] + i] = tuple(entry)
    if 'Prev' in obj.data:
        prev = obj.get('Prev')
        pdf_file.seek(prev)
        load_xref_table()


def load_xref_table():
    '''
    Загружает таблицу ссылок

    xref - первый вариант таблицы
    0 6 - первый номер объекта и количество объектов
    offset generation n - занятый объект
    offset generation f - свободный объект
    ...
    '''
    global xref_table
    tokens.cur_char = tokens.get_char()
    parser.cur_token = tokens.get_token()
    if parser.cur_token != ('id', 'xref'):
        load_xref_stream()
    else:
        parser.cur_token = tokens.get_token()
        index = parser.parse_data()
        size = parser.parse_data()
        for i in range(size):
            offset = parser.parse_data()
            gen = parser.parse_data()
            t = parser.parse_data()
            if t == 'f':
                t = FREE
            elif t == 'n':
                t = NORMAL
            else:
                raise Exception("Неверный тип")
            xref_table[index + i] = (t, offset, gen)
        load_trailer()
    

def load_header():
    '''
    Загружает заголовок PDF

    Первая строка файла %PDF-1.номер
    Возвращает номер версии: 1.0 - 1.7
    '''
    header = pdf_file.read(8)
    return '1.' + chr(header[-1])


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
    tokens.cur_char = tokens.get_char()
    parser.cur_token = tokens.get_token()
    while parser.cur_token != ('<<',):
        parser.cur_token = tokens.get_token()
    trailer = parser.parse_data()
    if root_ref == None:
        root_ref = trailer['Root']
    if 'Prev' in trailer:
        prev = trailer['Prev']
        pdf_file.seek(prev)
        load_xref_table()

        
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
    Если объекта нет в таблице ссылок, возвращается пустой объект
    Если объект есть в словаре, то объект берется оттуда
    иначе загружает объект из файла:
    анализируется тип записи в таблице
    если обычный объект то 
       установка позиции в файле из таблицы
       установка текущего символа (cur_char)
       установка текущей лексемы (cur_token)
       чтение объекта (parse_object)
       добавляем объект в словарь
    если свободный объект, то возвращает пустой объект
    если сжатый объект вызываем чтение сжатого объекта get_object_stream_object
    Возвращает объект Object
    '''
    global objects
    if objects.get(ref):
        obj = objects[ref]
    else:
        if ref[0] not in xref_table:
            return Object(ref[0], ref[1], None)
        r = xref_table[ref[0]]
        if r[0] == NORMAL:
            pdf_file.seek(r[1])
            tokens.cur_char = tokens.get_char()
            parser.cur_token = tokens.get_token()
            obj = parser.parse_object()
            objects[ref] = obj
        elif r[0] == FREE:
            return Object(ref[0], ref[1], None)
        elif r[0] == COMPRESSED:
            obj = get_object_stream_object(r[1], r[2], ref[0])
        else:
            print(r[0])
            raise Exception("Unknown type")
    return obj


def get_object_stream_object(obj_stream_num, index, obj_num):
    '''
    Чтение сжатого объекта

    obj_stream_num - старший номер объекта, содержащий сжатые объекты, второй всегда 0
    index - индекс искомого объекта
    obj_num - номер искомого объекта
    пример:
    15 0 obj
        << /Type /ObjStm
             /Length 1856
             /N 3
        >>
    stream - распакованный
    11 0 12 547 13 665
    << ... >> данные объекта 1
    << ... >> данные объекта 2
    << ... >> данные объекта 3
    
    читаем объект obj_num (get_object)
    проверяем тип Type = ObjStm
    читаем поле словаря N - число объектов
    настраиваем лексичексий анализатор, чтобы читал из потока объекта
    проходим по всем парам (номер объекта, смещение) пока не перейдем на index
    проверям что номер объекта в списке совпадает с искомым
    устанавливаем смещение в потоке
    читаем данные объекта (parse_data)
    добавляем объект в словарь
    возвращает: объект Object
    '''
    global stream_pos
    obj = get_object((obj_stream_num, 0))
    if obj.get('Type') != NameObject('ObjStm'):
        raise Exception("Тип объекта = ObjStm")
    num = obj.get('N')
    stream_pos = 0

    def get_stream_char():
        global stream_pos
        stream_pos += 1
        if stream_pos  > len(obj.stream):
            return -1
        else:
            return chr(obj.stream[stream_pos - 1])

    tokens.get_char = get_stream_char
    tokens.cur_char = tokens.get_char()
    parser.cur_token = tokens.get_token()
    objs = []
    for i in range(num):
        on = parser.parse_data()
        ofs = parser.parse_data()
        objs.append(on)
    for i in range(num):
        data = parser.parse_data()
        o = Object(objs[i], 0, data)
        objects[(objs[i], 0)] = o
    tokens.get_char = get_char
    return objects[(objs[index], 0)]


if __name__ == '__main__':
    from sys import argv
    load(argv[1])
    print('Version:', version)
#    print('objects:', objects)
    print('trailer:', trailer)
    print('root:', root_ref)
    print('xref_table:', xref_table)
    print(get_object((int(argv[2]), 0)))
