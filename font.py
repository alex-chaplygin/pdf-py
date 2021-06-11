import tokens
import pdf_parser as parser
import pdf_file
# словарь подстановок для текущего шрифта
cmap = {}


def load(ref):
    '''
    загрузить шрифт

    ref - ссылка на шрифт
    загрузка cmap
    '''
    global cmap
    font = pdf_file.get_object(ref)
    m = font.get('ToUnicode')
    cmap.clear()
    if m != None:
        old = tokens.get_char
        old_c = tokens.cur_char
        old_t = parser.cur_token
        tokens.get_char = pdf_file.get_char
        obj = pdf_file.get_object(m).stream
        tokens.get_char = old
        tokens.cur_char = old_c
        parser.cur_token = old_t
        load_cmap(obj)


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
#    print(cmap)
    tokens.get_char = old
    tokens.cur_char = old_c
    parser.cur_token = old_t
    
    
def get_char(code):
    '''
    возвращает символ по коду
    '''
    if ord(code) in cmap:
#        print(code, ord(code), cmap[ord(code)])
        if ord(cmap[ord(code)]) > 0xffff:
            return ' '
        return cmap[ord(code)]
    else:
        return code
