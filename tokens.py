'''
Лексический анализатор
'''

# текущий символ
cur_char = ''

# функция - следующий символ
# возвращает следующий символ или -1 если конец потока
get_char = None

separators = ['\x00', '\x09', '\x0a',  '\x0c',  '\x0d',  '\x20']


def get_token():
    """
     Возвращает токен
    Удаляет разделители.
    Анализирует первый символ.
    Цифра - число ('num', 14)
    Буква - идентификатор ('id', 'null')
    /   ('/')
    ( - literal string ('str', 'ggg   ggg \n ')
    < - hex string ('hex', b'\x00\x00')
    << >>  ('<<') ('>>')
    [ ]  ('[') (']')
    конец потока ('end')
    @return  : token
    """
    global cur_char
    if cur_char == -1:
        return ('end')
    skip_whitespace()
    if cur_char.isdigit() or cur_char == '+' or cur_char == '-':
        return get_number()
    elif cur_char.isalpha():
        return get_id()
    elif cur_char == '(':
        return get_literal_string()
    elif cur_char == '<':
        c = get_char()
        if c != '<':
            return get_hex_string(c)
        else:
            return ('<<')
    elif cur_char == '>':
        c = get_char()
        if c == '>':
            return ('>>')
        else:
            raise Exception('Неожиданное >')
    else:
        c = cur_char
        cur_char = get_char()
        return (c)


def skip_whitespace():
    """
     Пропускает разделители \x00 \x09 \x0a \x0c \x0d \x20 
    Пропуск комментария

    """
    global cur_char

    while cur_char in separators:
        cur_char=get_char()


def skip_comment():
    """
    Пропустить комментарий, который начинается с % до конца строки
    "123 % ----"
    """
    pass


def get_number():
    """
    Извлекает число
    Примеры чисел: 123 43445 +17 -98 0
    Вещественные: 34.5 -3.62 +123.4 4. -0.002 0.0

    @return  : ('num', число)
    """
    global cur_char
    num = ''
    zn = ''
    if cur_char == '+' or cur_char == '-':
        zn = cur_char
        cur_char = get_char()
    while cur_char != -1 and (cur_char.isdigit() or cur_char == '.'):
            num += cur_char
            cur_char = get_char()
    try: num = int(zn + num)
    except: num = float(zn + num)

    return ('num', num)


def get_id():
    """
    Извлекает идентификатор
    obj null
    Type
    lime#20Green
    """
    global cur_char
    iden = ''
    while cur_char not in separators:
        if cur_char == -1:
            break
        iden += cur_char
        cur_char = get_char()
    return ('id', iden)


def get_literal_string():
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

    @return  : ('str', строка)
    """
    pass


def get_hex_string(first):
    """
    first - первый символ
     Извлекает строку в скобках из строки.
    значение из строки data удаляется
    Примеры: 901FA3> Возвращает b'\x90\x1f\xa3'
    @return  : ('hex', байтовая строка)
    """
    pass


if __name__ == '__main__':
    data = 'stream '
    index = 0


    def next_char():
        global index
        index += 1
        if index > len(data):
            return -1
        else:
            return data[index - 1]

    get_char = next_char
        
    def test(in_str, res):
        global cur_char
        global data
        global index
        data = in_str
        index = 0
        cur_char = get_char()
        token = get_token()
        print('Вход:', in_str, 'Ожидается:', res, 'Результат:', token, end='')
        if token == res:
            print(' Успех')
        else:
            print(' Неудача')

        
    test('stream', ('id', 'stream'))
    test('', ('end'))
    test('12 ', ('num', 12))
    print()
    test('\x0cstream', ('id', 'stream'))
    test('\x00\x09\x0a\x0c\x0d\x20stream', ('id', 'stream'))
    test('        \n\t\t     stream', ('id', 'stream'))
    print()
    test('34.12', ('num', 34.12))
    test('+34.12', ('num', 34.12))
    test('-34.12', ('num', -34.12))
    test('3412', ('num', 3412))
    test('+3412', ('num', 3412))
    test('-3412', ('num', -3412))
