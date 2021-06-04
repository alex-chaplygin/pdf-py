'''
Синтаксический анализатор
'''
import tokens as tok
from Object import *
from NameObject import *


# текущая лексема
cur_token = None

# функция для следующего токена
get_token = tok.get_token

# функция для следующего байта
get_bytes = None


def parse_object():
    '''
    12 0 obj 
    (Test)
    endobj
    13 0 obj 
    true
    endobj
    '''
    global cur_token
    (t, num1) = cur_token
    if t != 'num':
        raise Exception('Ожидается число')
    (t, num2) = get_token()
    if t != 'num':
        raise Exception('Ожидается число')
    (t, k) = get_token()
    if t != 'id':
        raise Exception('Ожидается obj')
    if k != 'obj':
        raise Exception('Ожидается obj')
    cur_token = get_token()
    data = parse_data()
    stream = parse_stream(data)
    tok = cur_token
    if tok[0] != 'id':
        raise Exception('Ожидается endobj')
    if tok[1] != 'endobj':
        raise Exception('Ожидается endobj')
    return Object(num1, num2, data, stream)


def parse_data():
    '''
    распознает данные внутри объекта
    текущий объект в cur_token (тип, значение)
    возвращает данные
    если тип = 'id'
    true - True
    false - False
    null - None
    если тип = '/' то прочитать следующий id и вернуть NameObject
    если тип = '[' то вернуть parse_array
    если тип = '<<' то вернуть parse_dict
    иначе возвращает значение из токена
    в каждом случае перед возвратом значения - присвоить новое значение текущему токену
    '''
    global cur_token
    t = cur_token
    cur_token = get_token()
    if t == ('id', 'true'):
        return True
    elif t == ('id', 'false'):
        return False
    elif t == ('id', 'null'):
        return None
    elif t == ('/',):
        c = cur_token
        cur_token = get_token()
        return NameObject(c[1])
    elif t == ('[',):
        return parse_array()
    elif t == ('<<',):
        return parse_dict()
    else:
        return t[1]


def parse_array():
    '''
    распознавание массива
    [ любые значения ]
    открывающая скобка уже прочитана
    рекурсивно вызывает parse_data пока не встретилась скобка ']'
    накапливает элемент в списке
    возвращает список
    '''
    global cur_token
    arr = []
    while cur_token != (']',):
        arr.append(parse_data())
    cur_token = get_token()
    if 'R' in arr:
        arr2 = []
        for i in range(len(arr)):
            if arr[i] == 'R':
                p2 = arr2.pop()
                p1 = arr2.pop()
                arr2.append((p1, p2))
            else:
                arr2.append(arr[i])
        arr = arr2
    return arr


def parse_dict():
    '''
    распознавание словаря
    открывающая скобка уже прочитана
    << ключ1 значение1 ключ2 значение2 ... >>
    рекурсивно вызывает parse_data пока не встретилась скобка '>>'
    значение может быть как ссылка:
    1 0 R (num num id)
    ссылку можно распознать прочитав еще один токен
    если текущее значение - число
    и следующей токен - число (и после него идет id('R'))
    то тогда это ссылка
    иначе следующий токен - это новый ключ
    в этом случае в словарь записывается кортеж из двух чисел (1, 0)
    ключи и значения записываются в словаре
    ключ записывается как строка (data из NameObject)
    возвращает словарь
    '''
    global cur_token
    dic = {}
    while cur_token != ('>>',):
        key = parse_data()
        val = parse_data()
        if cur_token[0] == 'num':
            val = (val, cur_token[1])
            cur_token = get_token() # R
            cur_token = get_token()
        dic[key.data] = val
    cur_token = get_token()
    return dic

def parse_stream(data_dict):
    '''
    stream
    0x00 0x01 ...
    endstream
    распознает поток байт (если есть)
    если текущий токен не stream, то выход
    data_dict - словарь из него извлекается по ключу 'Length' длина потока в байтах
    если длина косвенная, то считываются байты, пока не встретится endstream
    если значение текущего токена = stream
       пропускаются переводы строк
       читается заданное число байт (get_bytes - чтение байт), 
       накапливается в строке байт
       в конеце нужно проверить наличие endstream
       выводится предупреждение, если фильтр отличен от FlateDecode
       возвращается строка байт
    иначе возвращает None
    '''
    global cur_token
    if cur_token != ('id', 'stream'):
        return b''
    length = data_dict['Length']
#    print(data_dict)
    if type(length) == tuple:
#    print('dict', data_dict)
        s = b''
        while s[-9:] != b'endstream':
            s += get_bytes(1)
#        print(s)
        s = s[:-9].strip()
#        print(s)
    else:
        s = get_bytes(length) # 0xa already read
        if s[0] == 0x0a:
            s += get_bytes(1)
            s = s[1:]
        cur_token = get_token()
        if cur_token != ('id', 'endstream') and cur_token != ('id', 'xendstream'):
            raise Exception('No endstream')
    cur_token = get_token()
    if data_dict['Filter'] != NameObject('FlateDecode'):
        print('Неподдерживается фильтр', data_dict['Filter'])
        return b''
    return s
