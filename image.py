'''
загрузка и обработка изображений
'''
from collections import namedtuple
import pdf_file
import tokens
import pdf_parser as parser

# структура для изображений
# width - ширина
# height - высота
# data - байтовая строка закодированных пикселей изображения
# num_components - число цветовых компонент (1 - черно-белое, 3 - цветное)
# bpp - число бит в data для одного цветового компонента
Image = namedtuple('Image', 'width height data num_components bpp')


def load(ref):
    '''
    загружает внешний объект(изображение)

    ref - ссылка на объект
    сохраняем состояние парсера
    устанавливаем парсер на чтение из файла
    загружаем объект через pdf_file.get_object
    если объект пустой, то возвращаем None
    проверяем парамтеры словаря объекта:
       если тип объекта 'Type' не 'XObject' возвращаем None
       если подтип объекта 'Subtype' не 'Image' возвращаем None
    читаем параметры словаря изображения:
      'Width' - ширина
      'Height' - высота
      'BitsPerComponent' - число бит на компонент цвета
      'ColorSpace' - может быть или нет(если нет, то возвращаем None)
        '/DeviceGray' - один компонент
        '/DeviceRGB' - три компонента
        '/DeviceCMYK' - четыре компонента
        если другой, то возвращаем None
    если в прочитанном объекте stream пустой, то возвращаем None
    иначе stream присваиваем в поле data изображения
    восстанавливаем состояние парсера
    возвращает объект Image или None - если изображение не загружено
    '''
    old = tokens.get_char # сохраняем состояние парсера
    old_c = tokens.cur_char
    old_t = parser.cur_token
    tokens.get_char = pdf_file.get_char # устанавливаем парсер на чтение из файла
    xobj = pdf_file.get_object(ref)


    tokens.get_char = old # восстанавливаем состояние парсера
    tokens.cur_char = old_c
    parser.cur_token = old_t


def interpolate(im, new_width, new_height):
    '''
    изменяет размеры изображения
    
    im - исходное изображение
    new_width - новая ширина
    new_height - новая высота
    возвращает измененное изображение Image
    '''
    pass
    
