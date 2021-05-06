'''
Синтаксический анализатор
'''
import tokens as tok

# текущая лексема
cur_token = None

# функция для следующего токена
get_token = tok.get_token

# функция для следующего байта
get_byte = None

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
    (t, num1) = get_token()
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
    (t, k) = cur_token
    if t != 'id':
        raise Exception('Ожидается endobj')
    if k != 'endobj':
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
    pass


def parse_array():
    '''
    распознавание массива
    [ любые значения ]
    открывающая скобка уже прочитана
    рекурсивно вызывает parse_data пока не встретилась скобка ']'
    накапливает элемент в списке
    возвращает список
    '''
    pass

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
    pass


def parse_stream(data_dict):
    '''
    распознает поток байт (если есть)
    data_dict - словарь из него извлекается по ключу 'Length' длина потока в байтах
    если значение текущего токена = stream
       пропускаются разделители (tok.skip_whitespace)
       читается заданное число байт, накапливается в строке байт
       возвращается строка байт
    иначе возвращает None
    '''
    pass


if __name__ == '__main__':
    data = []
    index = 0


    def next_tok():
        global index
        index += 1
        if index > len(data):
            return -1
        else:
            return data[index - 1]

    get_token = next_tok
        
    def test(in_str, res, func=parse_data):
        global cur_char
        global data
        global index
        data = in_str
        index = 0
        cur_token = get_token()
        parse = func()
        print('Вход:', in_str, 'Ожидается:', res, 'Результат:', parse, end='')
        if parse == res:
            print(' Успех')
        else:
            print(' Неудача')

        
    test([('id', 'null')], None)
    test([('id', 'true')], True)
    test([('id', 'false')], False)
