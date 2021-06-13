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
from NameObject import *
from collections import namedtuple
import pdf_file


# список страниц
page_list = []
# кэш страниц (страницы вместе с содержимым)
page_cache = {}

# класс для страниц
# p1 = Page(resources={}, contents=(200, 0))
Page = namedtuple('Page', 'resources media_box contents')

media_box = (0, 0, 500, 800)


def load(file_name):
    '''
    загружает документ

    file_name - имя файла
    формирует дерево страниц
    '''
    global page_list
    global page_cache
    page_list.clear()
    page_cache.clear()
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
    global media_box
    for i in node.get('Kids'):
        obj = pdf_file.get_object(i)
        if obj.get('Type') == NameObject('Page'):
            if 'MediaBox' in obj.data:
                media_box = obj.get('MediaBox')
            page = Page(resources = obj.get('Resources'), media_box = media_box, contents = obj.get('Contents'))
            page_list.append(page)
        elif obj.get('Type') == NameObject('Pages'):
            load_pages(obj)
        else:
            raise Exception("Unknow page type")


def get_page(num):
    '''
    загрузка содержимого страницы

    num - номер страницы (начиная с 1)
    если в contents - 1 объект, то загружаем его и присваиваем в contents
    если список, то загружаем все объекты и накапливаем содержимое в contents
    возвращает страницу Page с загруженным содержимым (вместо кортежа - строка байт)
    '''
    if num in page_cache:
        return page_cache[num]
    if num < 1 or num > len(page_list):
        return None
    page = page_list[num - 1]
    if type(page.contents) == list:
        contents = b''
        for i in page.contents:
            content = pdf_file.get_object(i)
            contents += content.stream
    else:
        contents = pdf_file.get_object(page.contents).stream
    if type(page.resources) == tuple:
        resources = pdf_file.get_object(page.resources).data
    else:
        resources = page.resources
    new_page = Page(contents=contents, resources=resources, media_box=page.media_box)
    page_cache[num] = new_page
    return new_page


if __name__ == '__main__':
    from sys import argv


    load(argv[1])
    print(get_page(int(argv[2])))
    print(get_page(int(argv[2]) + 1))
