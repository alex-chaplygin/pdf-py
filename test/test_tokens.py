'''
Тестирование лексического анализатора
'''
import sys
sys.path.append('..')
import tokens

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

    tokens.get_char = next_char
        
    def test(in_str, res):
        global cur_char
        global data
        global index
        data = in_str
        index = 0
        tokens.cur_char = tokens.get_char()
        token = tokens.get_token()
        print('Вход:', in_str, 'Ожидается:', res, 'Результат:', token, end='')
        if token == res:
            print(' Успех')
        else:
            print('\n!!!Неудача')

        
    test('stream', ('id', 'stream'))
    test('null', ('id', 'null'))
    test('', ('end',))
    test('12 ', ('num', 12))
    test('lime#20Green', ('id', 'lime Green'))
    test('lime#adGreen', ('id', 'lime\xadGreen'))
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
    print()
    test('(qwe)', ('str','qwe'))
    test('()', ('str',''))
    test('(12@#$%^&*3)', ('str', '12@#$%^&*3'))
    test('((1234))', ('str', '(1234)'))
    test('(12(1234))', ('str', '12(1234)'))
    test('(12(1(23)4))', ('str', '12(1(23)4)'))
    test('(12(1)(23)4)', ('str', '12(1)(23)4'))
    print()
    test('<901F>     <912F>', ('hex', b'\x90\x1f'))
    test('<90>', ('hex', b'\x90'))
    test('<ABFA>', ('hex', b'\xab\xfa'))
    test('<901FA3>', ('hex', b'\x90\x1f\xa3'))
    test('<AA>', ('hex', b'\xaa'))
    test('<9ABFA366DF>', ('hex', b'\x9a\xbf\xa3\x66\xdf'))
    print()
    test('/Type /Obj', ('/',))
    test('[1 2 3 4 5]', ('[',))
    test('] >>', (']',))
    test('<< /Type /Ref >>', ('<<',))
    test('>> stream', ('>>',))
    test('1 0 R>>', ('num', 1))
    test('0 R>>', ('num', 0))
    test('R>>', ('id', 'R'))
    
