import zlib
from NameObject import *


class Object:
    """
    Объект - единица PDF файла
    """
    def __init__(self, num1, num2, data, stream=b''):
        """
        num1 - номер объекта
        num2 - номер поколения (увеличивается при изменении объекта)
        data - данные объекта
        stream - поток объекта (содержимое)
        """
        self.num1 = num1
        self.num2= num2
        self.data = data
        self.stream = zlib.decompress(stream)


    def get(self, key):
        if type(self.data) is dict:
            return self.data[NameObject(key)]
        else:
            raise Exception('Данные объекта - не словарь')
