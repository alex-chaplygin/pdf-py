import tokens
import pdf_parser as parser
import pdf_file
from Matrix3 import *
from NameObject import *

# словарь подстановок для текущего шрифта
cmap = {}

# кодировка для текущего шрифта
encoding = {}

# матрица трансформации из пространства шрифта в пользовательское
font_matrix = None

#первый код в шрифте
first_char = 0

# список размеров символов в шрифте
widths = []

standart_encoding = {
        NameObject('A'): 'A',
        NameObject('B'): 'B',
        NameObject('C'): 'C',
        NameObject('D'): 'D',
        NameObject('E'): 'E',
        NameObject('F'): 'F',
        NameObject('G'): 'G',
 	NameObject('afii10017'): 'А',
 	NameObject('afii10018'): 'Б',
 	NameObject('afii10019'): 'В',
 	NameObject('afii10020'): 'Г',
 	NameObject('afii10021'): 'Д',
 	NameObject('afii10022'): 'Е',
 	NameObject('afii10023'): 'Ё',
 	NameObject('afii10024'): 'Ж',
 	NameObject('afii10025'): 'З',
 	NameObject('afii10026'): 'И',
 	NameObject('afii10027'): 'Й',
 	NameObject('afii10028'): 'К',
 	NameObject('afii10029'): 'Л',
 	NameObject('afii10030'): 'М',
 	NameObject('afii10031'): 'Н',
 	NameObject('afii10032'): 'О',
 	NameObject('afii10033'): 'П',
 	NameObject('afii10034'): 'Р',
 	NameObject('afii10035'): 'С',
 	NameObject('afii10036'): 'Т',
 	NameObject('afii10037'): 'У',
 	NameObject('afii10038'): 'Ф',
 	NameObject('afii10039'): 'Х',
 	NameObject('afii10040'): 'Ц',
 	NameObject('afii10041'): 'Ч',
 	NameObject('afii10042'): 'Ш',
 	NameObject('afii10043'): 'Щ',
 	NameObject('afii10044'): 'Ъ',
 	NameObject('afii10045'): 'Ы',
 	NameObject('afii10046'): 'Ь',
 	NameObject('afii10047'): 'Э',
 	NameObject('afii10048'): 'Ю',
 	NameObject('afii10049'): 'Я',
		
 	NameObject('afii10050'): 'Ґ',
 	NameObject('afii10051'): 'Ђ',
 	NameObject('afii10052'): 'Ѓ',
 	NameObject('afii10053'): 'Є',
 	NameObject('afii10054'): 'Ѕ',
 	NameObject('afii10055'): 'І',
 	NameObject('afii10056'): 'Ї',
 	NameObject('afii10057'): 'Ј',
 	NameObject('afii10058'): 'Љ',
 	NameObject('afii10059'): 'Њ',
 	NameObject('afii10060'): 'Ћ',
 	NameObject('afii10061'): 'Ќ',
 	NameObject('afii10062'): 'Ў',
 	NameObject('afii10145'): 'Џ',
 	NameObject('afii10146'): 'Ѣ',
 	NameObject('afii10147'): 'Ѳ',
 	NameObject('afii10148'): 'Ѵ',
		
 	NameObject('afii10065'): 'а',
 	NameObject('afii10066'): 'б',
 	NameObject('afii10067'): 'в',
 	NameObject('afii10068'): 'г',
 	NameObject('afii10069'): 'д',
 	NameObject('afii10070'): 'е',
 	NameObject('afii10071'): 'ё',
 	NameObject('afii10072'): 'ж',
 	NameObject('afii10073'): 'з',
 	NameObject('afii10074'): 'и',
 	NameObject('afii10075'): 'й',
 	NameObject('afii10076'): 'к',
 	NameObject('afii10077'): 'л',
 	NameObject('afii10078'): 'м',
 	NameObject('afii10079'): 'н',
 	NameObject('afii10080'): 'о',
 	NameObject('afii10081'): 'п',
 	NameObject('afii10082'): 'р',
 	NameObject('afii10083'): 'с',
 	NameObject('afii10084'): 'т',
 	NameObject('afii10085'): 'у',
 	NameObject('afii10086'): 'ф',
 	NameObject('afii10087'): 'х',
 	NameObject('afii10088'): 'ц',
 	NameObject('afii10089'): 'ч',
 	NameObject('afii10090'): 'ш',
 	NameObject('afii10091'): 'щ',
 	NameObject('afii10092'): 'ъ',
 	NameObject('afii10093'): 'ы',
 	NameObject('afii10094'): 'ь',
 	NameObject('afii10095'): 'э',
 	NameObject('afii10096'): 'ю',
 	NameObject('afii10097'): 'я',
}

def load(ref):
    '''
    загрузить шрифт

    ref - ссылка на шрифт
    загрузка cmap
    '''
    global cmap
    global encoding
    global font_matrix
    global widths
    global first_char
    old = tokens.get_char
    old_c = tokens.cur_char
    old_t = parser.cur_token
    tokens.get_char = pdf_file.get_char
    font = pdf_file.get_object(ref)
    matrix = font.get('FontMatrix')
    if matrix == None:
        font_matrix = Matrix3(0.001, 0, 0, 0.001, 0, 0)
    else:
        font_matrix = Matrix3(matrix[0], matrix[1], matrix[2], matrix[3], matrix[4], matrix[5])
    print(font)
    widths = font.get('Widths')
    first_char = font.get('FirstChar')
    if first_char == None:
        first_char = 0
    if 'Resources' in font.data and 'Widths' in font.get('Resources'):
        widths = font.get('Resources')['Widths']
    if type(widths) == tuple:
        widths = pdf_file.get_object(widths).data
    if widths == None:
        widths = [10 for x in range(256)]
    encoding.clear()
    if 'Encoding' in font.data:
        load_encoding(font.get('Encoding'))
    #print(widths)
    m = font.get('ToUnicode')
    cmap.clear()
    if m != None:
        obj = pdf_file.get_object(m).stream
        load_cmap(obj)
    tokens.get_char = old
    tokens.cur_char = old_c
    parser.cur_token = old_t


stream_pos = 0
        

def load_cmap(stream):
    '''
    загрузка словаря подстановки

    stream - поток объекта подстановки
    ...
    endcodespacerange
    4 beginbfrange
    <21> <26> <0021>
    <28> <5F> <0028>
    <61> <7E> <0061>
    <C0> <FF> <0410>
    endbfrange
    35 beginbfchar
    <00> <0060>
    <01> <00B4>
    ...
    endbfchar
    '''
    global cmap
    global stream_pos
#    print(stream)
    stream_pos = 0


    def get_stream_char():
        global stream_pos
        stream_pos += 1
        if stream_pos  > len(stream):
            return -1
        else:
            return chr(stream[stream_pos - 1])

    old = tokens.get_char
    old_c = tokens.cur_char
    old_t = parser.cur_token
    tokens.get_char = get_stream_char
    tokens.cur_char = tokens.get_char()
    parser.cur_token = tokens.get_token()

    data = ''
    while data != 'endcodespacerange':
        data = parser.parse_data()
    while parser.cur_token != ('id', 'endcmap'):
        num = parser.parse_data()
        typ = parser.parse_data()
        for i in range(num):
            if typ == 'beginbfrange':
                start = parser.parse_data()[0]
                end = parser.parse_data()[0]
                data = parser.parse_data()
                if len(data) == 1:
                    data = chr(data[0])
                else:
                    data = data.decode('utf-16be')
                code_start = ord(data)
#                print(start, end, code_start)
                for i in range(start, end + 1):
                    cmap[i] = chr(code_start + i - start)
            elif typ == 'beginbfchar':
                code = parser.parse_data()[0]
                data = parser.parse_data().decode('utf-16be')
                cmap[code] = data
        parser.parse_data()
 #   print(cmap)
    tokens.get_char = old
    tokens.cur_char = old_c
    parser.cur_token = old_t


def load_encoding(ref):
    global encoding
    if type(ref) != tuple:
        encoding = [i for i in range(256)]
        return
    en = pdf_file.get_object(ref)
    dif = en.get('Differences')
    for d in dif:
        if type(d) == int:
            code = d
        else:
            encoding[code] = d
            code += 1
    #print(encoding)
    
    
def get_char(code):
    '''
    возвращает символ по коду
    '''
    if not cmap:
        if ord(code) in encoding:
            name = encoding[ord(code)]
        else:
            return code
        #print(name, type(name))
        if name in standart_encoding:
            return standart_encoding[name]
        else:
            return code
    if ord(code) in cmap:
#        print(code, ord(code), cmap[ord(code)])
        if ord(cmap[ord(code)]) > 0xffff:
            return ' '
        return cmap[ord(code)]
    else:
        return code


def get_width(s, size):
    '''
    возвращает длину строки в пользовательском пространстве

    s - строка
    '''
    global first_char
    width = 0
    for c in s:
        code = ord(c) - first_char
      #  if ord(c) == 32:
        #    width += 100
        if code >= len(widths):
            width += 1000
        else:
            width += widths[code]
    return width * size * font_matrix.matrix[0][0]
