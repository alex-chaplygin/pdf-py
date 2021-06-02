from math import sin, cos


class Matrix3:
    '''
    Матрица 3 x 3
    '''
    def __init__(self, a=1, b=0, c=0, d=1, e=0, f=0):
        '''
        создает матрицу
        a b 0
        c d 0
        e f 1
        '''
        pass


    def translate(self, tx, ty):
        '''
        задает матрицу переноса
        
        a b c d e  f
        1 0 0 1 tx ty
        '''
        pass


    def scale(self, sx, sy):
        '''
        задает матрицу масштабирования

        a  b  c d  e f
        sx 0 0 sy 0 0
        '''
        pass


    def rotate(self, q):
        '''
        задает матрицу поворота

        q - угол в радианах
        a         b        c         d         e f
        cos(q) sin(q) -sin(q) cos(q) 0 0
        '''
        pass

    
    def mult_vector(self, vector):
        '''
        умножение матрицы на вектор

        vector - (x, y, 1)
        x' = a x + c y + e
        y' = b x + d y + f
        возвращает вектор (x', y')
        '''
        pass


    def __mul__(self, matrix):
        '''
        умножение матрицы на матрицу  ( Mt * Mr )

        matrix - другая матрица
        возвращает матрицу Matrix
        '''
        pass


    def __repr__(self):
        '''
        представление объекта в виде строки
        a b 0
        c d 0
        e f 1
        '''
        pass
