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
import font
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
    сохранить текущую матрицу трансформаций в стеке
    '''
    matrix_stack.append(ctm)


def pop_stack():
    '''
    восстановить текущую матрицу трансформаций из стека
    '''
    matrix_stack.pop()


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
    mtx = Matrix3(a, b, c, d, e, f)
    ctm = mtx * ctm

    
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
    matrix = matrix.translate(tx, ty)
    text_matrix = matrix * text_matrix


def set_next_line():
    '''
    установить позицию текста на новой строке

    операнды tx, ty
    установить -ty - расстояние между строками(text_leading)
    создать матрицу для перемещения tx ty
    умножить  матрицу перемещения на матрицу текста и присвоить матрице текста
    '''
    pass


def set_text_matrix():
    '''
    установить текстовую матрицу

    операнды a b c d e f 
    '''
    pass


def next_line():
    '''
    перемещение на новую строку

    создать матрицу перемещения с параметрами 0 -text_leading
    умножить  матрицу перемещения на матрицу текста и присвоить матрице текста
    '''
    pass


def show_text():
    '''
    нарисовать текст текущим шрифтом

    операнд: строка текста
    текстовую матрицу умножить на матрицу трансформаций, получаем общую матрицу
    умножаем вектор (0, 0, 1) на общую матрицу - получаем координаты на экране
    добавляем текстовый объект в список объектов (x, y, string, current_font, current_size)
    '''
    pass


def next_line_show_text():
    '''
    переместиться на следующую строку и отобразить текст

    вызов next_line и show_text
    '''
    pass


def show_text_list():
    '''
    отобразить одну или более строк

    операнд - список
    [ (AWAY again) ] TJ
    [ (A) 120 (W) 120 (A) 95 (Y again) ] TJ
    проходим по списку, если элемент строка, то отображаем строку (show_text),
    если число - то перемещаем текстовую матрицу по горизонтали на это число
    '''
    pass


def begin_text():
    '''
    начало текста

    устанавливает матрицу текста в единичную
    '''
    pass


def set_leading():
    global text_leading
    text_leading = operands_stack.pop()

    
def interpret(page):
    global text_leading
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
    }
