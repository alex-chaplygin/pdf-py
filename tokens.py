'''
Лексический анализатор
'''

# текущий символ
cur_char = ''

# функция - следующий символ
# возвращает следующий символ или -1 если конец потока
get_char = None

separators = ['\x00', '\x09', '\x0a',  '\x0c',  '\x0d',  '\x20']
delimiters = ['(', ')', '<', '>', '[', ']', '{', '}', '/', '%']
digits = [x for x in "0123456789"]
letters = [x for x in ".abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"]



def get_token():
    """
    Возвращает очередной токен.

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
    Возвращает  : token

    """
    global cur_char
    if cur_char == -1:
        return ('end',)
    skip_whitespace()
    if cur_char == -1:
        return ('end',)
    if cur_char in digits or cur_char == '+' or cur_char == '-':
        return get_number()
    elif cur_char in letters:
        return get_id()
    elif cur_char == '(':
        return get_literal_string()
    elif cur_char == '<':
        c = get_char()
        if c != '<':
            return get_hex_string(c)
        else:
            cur_char = get_char()
            return ('<<',)
    elif cur_char == '>':
        c = get_char()
        if c == '>':
            cur_char = get_char()
            return ('>>',)
        else:
            raise Exception('Неожиданное >')
    else:
        c = cur_char
        cur_char = get_char()
        return (c,)


def skip_whitespace():    
    """
    Пропускает разделители и комментарии

    Разделители \x00 \x09 \x0a \x0c \x0d \x20 
    Комментарий: вызов skip_comment

    """
    global cur_char

    while cur_char in separators or cur_char == '%':
        if cur_char == '%':
            skip_comment()
        cur_char = get_char()


def skip_comment():
    """
    Пропуск комментария

    Пропустить комментарий, который начинается с % до конца строки
    "123 % ----"

    """
    global cur_char
    while  cur_char != '\n':
        cur_char = get_char()


def get_number():
    """
    Извлекает число

    Примеры чисел: 123 43445 +17 -98 0
    Вещественные: 34.5 -3.62 +123.4 4. -0.002 0.0
    Возвращает  : ('num', число)

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
    Возвращает: ('id', строка_идентификатора)

    """
    global cur_char
    iden = ''
    while cur_char not in separators and cur_char not in delimiters:
        if cur_char == -1:
            break
        elif cur_char == '#':
            c1, c2 = get_char(), get_char()
            cur_char = chr(int(c1 + c2, 16))
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

    Возвращает  : ('str', строка)
    """
    global cur_char
    stroka = ''
    s = 1
    cur_char = get_char()
    while cur_char != -1:
        if cur_char == '(':
            s += 1
        elif cur_char == ')':
            s -= 1
        if s == 0:
            break
        if cur_char == '\\':
            c1 = get_char()
            if c1 == '(':
                stroka += '('
            elif c1 == ')':
                stroka += '('
            elif c1 == 'n':
                stroka += '\n'
            else:
                c2, c3 = get_char(), get_char()
                stroka += chr(int(c1 + c2 + c3, 8))
        else:
            stroka += cur_char
        cur_char = get_char()
    cur_char = get_char()
    return ('str', stroka)


def get_hex_string(first):
    """
    Распознает hex строку.

    first - первый символ
    значение из строки data удаляется
    Примеры: 901FA3> Возвращает b'\x90\x1f\xa3'
    Возвращает  : ('hex', байтовая строка)

    """
    global cur_char
    bs = first
    cur_char = get_char()
    b = []
    while cur_char != '>' and cur_char != -1:
        bs += cur_char
        cur_char = get_char()
    for i in range(0, len(bs), 2):
        x = int(bs[i:i + 2], 16)
        b.append(x)
    cur_char = get_char()
    return ('hex', bytes(b))
