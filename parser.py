'''
Синтаксический анализатор
'''
import tokens as tok

def parse_object():
    '''
    12 0 obj 
    (Test)
    endobj
    13 0 obj 
    true
    endobj
    '''
    (t, num1) = tok.get_token()
    if t != 'num':
        raise Exception('Ожидается число')
    (t, num2) = tok.get_token()
    if t != 'num':
        raise Exception('Ожидается число')
    (t, k) = tok.get_token()
    if t != 'id':
        raise Exception('Ожидается obj')
    if k != 'obj':
        raise Exception('Ожидается obj')
    (t, data) = tok.get_token()
    (t, k) = tok.get_token()
    if t != 'id':
        raise Exception('Ожидается endobj')
    if k != 'endobj':
        raise Exception('Ожидается endobj')
    return Object(num1, num2, data)
    

def parse_boolean():
    pass
