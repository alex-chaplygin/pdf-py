from NameObject import *
"""
Таблица ссылок на объекты PDF
size - размер таблицы
index - диапазон номеров (начальный_номер объекта, количество)
w - размеры полей в записи в байтах
table - таблица ссылок
"""
size = 0
index = (0, 0)
w = None
table = []

def init(obj):
    """
    obj - объект таблицы ссылок
    """
    global table
    global index
    if obj.get('Type') != NameObject('XRef'):
        raise Exception('Not XRef')
    size = obj.get('Size')
    if NameObject('Index') in obj.data:
        i = obj.get('Index')
        index = (i[0], i[1])
    else:
        index = (0, size)
    w = obj.get('W')
    table.clear()
    for i in range(0, len(obj.stream), sum(w)):
        t = obj.stream[i]
        if t == 0:
            table.append((0, -1))
        else:
            offset = 0
            for j in range(w[1]):
                offset = offset << 8
                offset += obj.stream[i + 1 + j]
            table.append((t, offset))


def get(i):
    """
    получить смещение объекта
    i - номер объекта
    возвращает позицию в файле
    """
    (t, offset) = table[i]
    if t == 2:
        return get(offset)
    else:
        return offset
