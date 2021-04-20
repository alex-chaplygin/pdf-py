class Keyword:
    """
    Класс для ключевых слов
    data - строка (obj endobj stream endstream R xref trailer)
    """
    def __init__(self, string):
        self.data = string


    def __repr__(self):
        return 'Key:' + self.data


    def __eq__(self, other):
        """
        метод сравнения объектов
        """
        return self.data == other.data
    
