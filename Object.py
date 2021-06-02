import zlib


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
        if stream != b'':
            self.stream = zlib.decompress(stream)
        else:
            self.stream = None


    def get(self, key):
        if type(self.data) is dict:
            return self.data[key]
        else:
            raise Exception('Данные объекта - не словарь')


    def __eq__(self, other):
        """
        метод сравнения объектов
        """
        return self.data == other.data and self.num1 == other.num1  and self.num2 == other.num2 and self.stream == other.stream

    
    def __repr__(self):
        """
        представление объекта в виде строки
        """
        s = '(Object ' + str(self.num1) + ' ' + str(self.num2) + ' ' + str(self.data) + ')\n'
        if self.stream != None:
            s += ''.join([chr(x) for x in self.stream])
        return s
    
