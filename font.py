# словарь подстановок для текущего шрифта
cmap = {}


def load(ref):
    '''
    загрузить шрифт

    ref - ссылка на шрифт
    загрузка cmap
    '''
    pass


def load_cmap(obj):
    '''
    загрузка словаря подстановки

    obj - объект подстановки
    ...
    endcodespacerange
    4 beginbfrange
    <21> <26> <0021>
    <28> <5F> <0028>
    <61> <7E> <0061>
    <C0> <FF> <0410>
    endbfrange
    35 beginbfchar
    <00> <0060>
    <01> <00B4>
    ...
    endbfchar
    '''
    global cmap
    pass


def get_char(code):
    '''
    возвращает символ по коду
    '''
    pass
