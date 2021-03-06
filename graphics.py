'''
Графика PDF

BX - пропустить
ff
ff
22
X

BT
w
/F5 12 Tf
100 100.5 Tc
0.5 0.5 Ts
(Hello) Tj 
J
ET

/Resources << /Font
                      << /F5 (6, 0)
                            /F6 (7, 0)
                      >>
                        /XObject
                        << /Im1 (13, 0)
                              /Im2 (15, 0)
                         >>
                   >>

(x, y, 1) * 1.2 0 0
                0 1.2 0
                0 0 1
'''
import image
import font
import tokens
import pdf_parser as parser
import pdf_file
from Matrix3 import *

# текущая матрица трансформаций
# преобразование из пользовательских координат в координаты устройства
ctm = Matrix3()

# стек для матрицы трансформаций
# добавление в стек - append
# удаление из стека - pop()
matrix_stack = []

# матрица для вывода текста
text_matrix = Matrix3()

# высота между строками текста
text_leading = 0

# стек операндов
# заполняется перед выполнением оператора
operands_stack = []

# размеры страницы в пользовательских координатах
media_box = ()

# текущая страница
current_page = None

# текущий шрифт
current_font = 'Times'

# текущий размер шрифта
current_size = 12

# список объектов для отрисовки
object_list = []

text_pos = [0, 0, 1]


def set_device(width, height):
    '''
    установка матрицы для преобразования в координаты устройства

    width - ширина страницы в точках (на экране)
    height - высота страницы в точках (на экране)
    a                               b c d                                   e f
    width / media_width 0 0 -height / media_height 0 height
    '''
    global ctm
    ctm = Matrix3(float(width) / media_box[2], 0, 0, float(-height) / media_box[3], 0, height)


def push_stack():
    '''
    сохранить сотояние графики
    '''
    global matrix_stack
    matrix_stack.append(ctm)
    matrix_stack.append(text_matrix)


def pop_stack():
    '''
    восстановить состояние графики
    '''
    global text_matrix
    global ctm
    global matrix_stack
    text_matrix = matrix_stack.pop()
    ctm = matrix_stack.pop()


def set_transformation():
    '''
    модифицирует текущую матрицу трансформаций

    операнды a b c d e f - создается новая матрица
    умножается на текущую
    '''
    global ctm
    f = operands_stack.pop()
    e = operands_stack.pop()
    d = operands_stack.pop()
    c = operands_stack.pop()
    b = operands_stack.pop()
    a = operands_stack.pop()
    ctm = Matrix3(a, b, c, d, e, f) * ctm

    
def set_font():
    '''
    установить шрифт - /F13 12 Tf

    операнды: имя шрифта и размер
    загрузить шрифт из ресурсов (имя шрифта без слэша)
    загрузить словарь подстановок для шрифта (ключ 'ToUnicode')
    '''
    global current_size

    current_size = operands_stack.pop()
    name = operands_stack.pop().data
    font.load(current_page.resources['Font'][name])


def set_text_pos():
    '''
    установить позицию текста

    операнды tx, ty
    установить матрицу для перемещения tx ty
    умножить  матрицу перемещения на матрицу текста и присвоить матрице текста
    '''
    global text_matrix
    ty = operands_stack.pop()
    tx = operands_stack.pop()
    matrix = Matrix3()
    matrix.translate(tx, ty)
    text_matrix = matrix * text_matrix


def set_next_line():
    '''
    установить позицию текста на новой строке

    операнды tx, ty
    установить -ty - расстояние между строками(text_leading)
    создать матрицу для перемещения tx ty
    умножить  матрицу перемещения на матрицу текста и присвоить матрице текста
    '''
    global text_matrix
    global text_leading
    ty = operands_stack.pop()
    tx = operands_stack.pop()
    text_leading = -ty
    matrix = Matrix3()
    matrix.translate(tx, ty)
    text_matrix = matrix * text_matrix


def set_text_matrix():
    '''
    установить текстовую матрицу

    операнды a b c d e f 
    '''
    global text_matrix
    global text_pos
    f = operdans_stack.pop()
    e = operdans_stack.pop()
    d = operdans_stack.pop()
    c = operdans_stack.pop()
    b = operdans_stack.pop()
    a = operdans_stack.pop()
    text_matrix = Matrix3(a, b, c, d, e, f)
    text_pos = [0, 0, 1]


def next_line():
    '''
    перемещение на новую строку

    создать матрицу перемещения с параметрами 0 -text_leading
    умножить  матрицу перемещения на матрицу текста и присвоить матрице текста
    '''
    global text_matrix
    global text_leading
    global text_pos
    matrix = Matrix3()
    matrix.translate(0, -text_leading)
    text_matrix = matrix * text_matrix
    text_pos = [0, 0, 1]


def show_text():
    '''
    нарисовать текст текущим шрифтом

    операнд: строка текста
    текстовую матрицу умножить на матрицу трансформаций, получаем общую матрицу
    умножаем вектор text_pos на общую матрицу - получаем координаты на экране
    добавляем текстовый объект в список объектов (x, y, string, current_font, current_size)
    '''
    global object_list
    string = ''.join([font.get_char(c) for c in operands_stack.pop()])
    matrix = text_matrix * ctm
    coordinats = matrix.mult_vector(tuple(text_pos))

#    print(string)
  #  print(text_matrix)
    object_list.append((round(coordinats[0]), round(coordinats[1]), string, current_font, round(current_size * ctm.matrix[1][1])))


def next_line_show_text():
    '''
    переместиться на следующую строку и отобразить текст

    вызов next_line и show_text
    '''
    next_line()
    show_text()


def show_text_list():
    '''
    отобразить одну или более строк

    операнд - список
    [ (AWAY again) ] TJ
    [ (A) 120 (W) 120 (A) 95 (Y again) ] TJ
    проходим по списку, если элемент строка, то отображаем строку (show_text),
    если число - то перемещаем текстовую матрицу по горизонтали на это число
    '''
    global operands_stack
    global text_pos
    lst = operands_stack.pop()
    text_pos = [0, 0, 1]
    for i in lst:
        if type(i) == str:
            prev = i
            operands_stack.append(i)
            show_text()
        elif type(i) == int or type(i) == float:
            text_pos[0] = text_pos[0] + float(i) * font.font_matrix.matrix[0][0] + font.get_width(prev, current_size)
        else:
            raise Exception("Неизвестный тип в строке текста")


def begin_text():
    '''
    начало текста

    устанавливает матрицу текста в единичную
    '''
    global text_matrix
    global text_pos
    text_matrix = Matrix3()
    text_pos = [0, 0, 1]

    
def set_leading():
    global text_leading
    text_leading = operands_stack.pop()


def paint_xobject():
    '''
    рисует внешний объект

    операнд - имя объекта как ключ из cловаря XObjects из ресурсов страницы
    у внешнего объекта
    Type - XObject
    Subtype - Image, Form, PS
    '''
    xobj_name = operands_stack.pop()
    if not xobj_name.data in current_page.resources['XObjects']:
        print('Нет такого изображения', xobj_name)
        return
    im = image.load(current_page.resources['XObjects'][xobj_name.data])
    im = image.interpolate(im, ctm.matrix[0][0], ctm.matrix[1][1])
    if im != None:
        coords = ctm.mult_vector((0, 0, 1))
        object_list.append((coords[0], coords[1] - im.height, im.data, im.width, im.height, im.num_components, im.bpp))
    

stream_pos = 0

# операторы графики
operators = {
    'q': push_stack,
    'Q': pop_stack,
    'cm': set_transformation,
    'Tl': set_leading,
    'Tf': set_font,
    'Td': set_text_pos,
    'TD': set_next_line,
    'tm': set_text_matrix,
    'T*': next_line,
    'Tj': show_text,
    '\'': next_line_show_text,
    'TJ': show_text_list,
    'BT': begin_text,
    'Do': paint_xobject,
}
    
def interpret(page, width, height):
    global current_page
    global media_box
    global stream_pos
    global object_list

    print(page)
    current_page = page
    if current_page.media_box != None:
        media_box = current_page.media_box
    object_list.clear()
    set_device(width, height)
    
    stream_pos = 0
    
    def get_stream_char():
        global stream_pos
        stream_pos += 1
        if stream_pos  > len(page.contents):
            return -1
        else:
            return chr(page.contents[stream_pos - 1])
            
            
    tokens.get_char = get_stream_char
    tokens.cur_char = tokens.get_char()
    parser.cur_token = tokens.get_token()
    while parser.cur_token != ('end',):
        data = parser.parse_data()
#        print(data, '', end='')
        if type(data) != dict :
            if (type(data) == list or data not in operators):
                operands_stack.append(data)
            else:
                operators[data]()
    tokens.get_char = pdf_file.get_char
