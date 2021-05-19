'''
Тестирование синтаксического анализатора
'''
import sys
sys.path.append('..')
import tokens
import pdf_parser as parser
from NameObject import *
from Object import *

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

        
    def test(in_str, res, func=parser.parse_data):
        global data
        global index
        data = in_str
        index = 0
        tokens.get_char = next_char
        tokens.cur_char = tokens.get_char()
        parser.cur_token = tokens.get_token()
        parse = func()
        print('Вход:', in_str, 'Ожидается:', res, 'Результат:', parse, end='')
        if parse == res:
            print(' Успех')
        else:
            print('\n!!!!Неудача')


    test('null', None)
    test('true', True)
    test('false', False)
    test('12', 12)
    test('(Test)', 'Test')
    test('<AA>', b'\xaa')
    test('/Type', NameObject('Type'))
    test('[1 2 3]', [1, 2, 3])
    test('[1 (Test) 3]', [1, 'Test', 3])
    test('[1 [2 3 4] 3]', [1, [2, 3, 4], 3])
    test('<</Type 1>>', {'Type' : 1})
    test('<</Type /Ref /Length 1000>>', {
        'Type' : NameObject('Ref'),
        'Length' : 1000
    })
    test('<</Length 5 0 R>>', {'Length' : (5, 0)})
    print()
    test('''
    12 0 obj 
          0.0
    endobj    
    ''', Object(12, 0, 0.0), parser.parse_object)
    test('''
    13 0 obj 
          <<
              /Type /Ref
              /Length 1000
          >>
    endobj    
    ''', Object(13, 0, {
        'Type': NameObject('Ref'),
        'Length': 1000
    }), parser.parse_object)
