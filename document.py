'''
Документ PDF

root_ref --> /Type /Catalog
                   /Pages  ------------> /Type /Pages
                                                 /Parent (ссылка на родителя, кроме корня)
                                                 /Kids [ 4 0 R   ---> /Type /Page
                                                            5 0 R]         /Parent (ссылка на родителя)
                                                 /Count 2                /Resources (словарь ресурсов) 
                                                                              /MediaBox [0 0 700 600]
                                                                              /Contents  (содержимое одна или несколько ссылок) ---> /Type /Stream

[ p1 [p2 p3] p4 ]
p1 = (resources={}, media_box=(0, 0, 700, 600), contents=(300, 0))
'''
from collections import namedtuple
import pdf_file


# список страниц
page_list = []
# кэш страниц (страницы вместе с содержимым)
page_cache = {}

# класс для страниц
# p1 = Page(resources=(100, 0), contents=(200, 0))
Page = namedtuple('Page', 'resources media_box contents')


def load(file_name):
    '''
    загружает документ

    file_name - имя файла
    формирует дерево страниц
    '''
    global page_list
    pdf_file.load(file_name)
    catalog = pdf_file.get_object(pdf_file.root_ref)
    if catalog.get('Type') != NameObject('Catalog'):
        raise Exception('No catalog')
    pages = pdf_file.get_object(catalog.get('Pages'))
    load_pages(pages)


def load_pages(node):
    '''
    загружает дерево страниц из узла и формирует список страниц

    node - объект узел (Pages)
    проходим по всем элементам списка Kids
        загружаем объект по ссылке
        если тип объекта - Page, то создаем страницу и добавляем в список
        иначе если тип - Pages, вызываем load_pages для этого узла
        иначе ошибка
    '''
    global page_list
    pass


def get_page(num):
    '''
    загрузка содержимого страницы

    num - номер страницы (начиная с 1)
    если в contents - 1 объект, то загружаем его и присваиваем в contents
    если список, то загружаем все объекты и накапливаем содержимое в contents
    возвращает страницу Page с загруженным содержимым (вместо кортежа - строка байт)
    '''
    page, count = get_page_from_node(page_list, num, 1)
    return page
