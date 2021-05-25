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


# дерево страниц
page_tree = []

# класс для страниц
# p1 = Page(resources=(100, 0), contents=(200, 0))
Page = namedtuple('Page', 'resources media_box contents')


def load(file_name):
    '''
    загружает документ

    file_name - имя файла
    формирует дерево страниц
    '''
    global page_tree
    pdf_file.load(file_name)
    catalog = pdf_file.get_object(pdf_file.root_ref)
    if catalog.get('Type') != NameObject('Catalog'):
        raise Exception('No catalog')
    pages = pdf_file.get_object(catalog.get('Pages'))
    page_tree = load_tree(pages)


def load_tree(node):
    '''
    загружает дерево страниц из узла

    node - объект узел (Pages)
    создаем пустой список
    проходим по всем элементам списка Kids
        загружаем объект по ссылке
        если тип объекта - Page, то создаем страницу и добавляем в список
        иначе если тип - Pages, вызываем load_tree для этого узла и добавляем результат в список
        иначе ошибка
    возвращает: список страниц
    '''
    pass


def get_page(num):
    '''
    загрузка страницы

    num - номер страницы (начиная с 1)
    ищет страницу в дереве страниц
    возвращает страницу Page
    '''
    page, count = get_page_from_node(page_tree, num, 1)
    return page


def get_page_from_node(node, page_num, num):
    '''
    поиск страницы в узле

    node - узел список, в котором ищем
    page_num - номер страницы, которую ищем
    num - счетчик страниц
    обходим все элементы списка node
       если текущий элемент списка - список, тогда вызываем get_page_from_node с элементом, номером страницы, счетчик + 1
                          если страница не была найдена, то увеличить счетчик на count
       если номер страницы равен счетчику то возвращаем страницу (элемент, 0)
       увеличиваем счетчик num
    после цикла вернуть (None, число элементов в списке) - не найдено
    возвращает: (страницу, число элементов если узел)
    '''
    pass
