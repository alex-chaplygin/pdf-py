from NameObject import *


class XRef:
    """
    Таблица ссылок на объекты PDF
    size - размер таблицы
    index - диапазон номеров (начальный_номер объекта, количество)
    w - размеры полей в записи в байтах
    """
    def __init__(self, obj):
        """
        obj - объект таблицы ссылок
        """
        if obj.get('Type') != NameObject('XRef'):
            raise Exception('Not XRef')
        self.size = obj.get('Size')
        if obj.data.has_key(NameObject('Index')):
            i = obj.get('Index')
            self.index = (i[0], i[1])
        else:
            self.index = (0, self.size)
        w = obj.get('W')
        self.w = (w[0], w[1], w[2])
