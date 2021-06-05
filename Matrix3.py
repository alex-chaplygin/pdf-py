from math import sin, cos, pi, sqrt


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
        self.matrix = [
            [a, b, 0],
            [c, d, 0],
            [e, f, 1]
        ]


    def translate(self, tx, ty):
        '''
        задает матрицу переноса
        
        a b c d e  f
        1 0 0 1 tx ty
        '''
        self.matrix = [
            [1, 0, 0],
            [0, 1, 0],
            [tx, ty, 1]
        ]
        

    def scale(self, sx, sy):
        '''
        задает матрицу масштабирования

        a  b  c d  e f
        sx 0 0 sy 0 0
        '''
        self.matrix = [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ]


    def rotate(self, q):
        '''
        задает матрицу поворота

        q - угол в радианах
        a         b        c         d         e f
        cos(q) sin(q) -sin(q) cos(q) 0 0
        '''
        self.matrix = [
            [cos(q), sin(q), 0],
            [-sin(q), cos(q), 0],
            [0, 0, 1]
        ]


    def mult_vector(self, vector):
        '''
        умножение матрицы на вектор

        vector - (x, y, 1)
        x' = a x + c y + e
        y' = b x + d y + f
        возвращает вектор (x', y')
        '''
        x1 = self.matrix[0][0] * vector[0] + self.matrix[1][0] * vector[1] + self.matrix[2][0]
        y1 = self.matrix[0][1] * vector[0] + self.matrix[1][1] * vector[1] + self.matrix[2][1]
        return (x1, y1)


    def __mul__(self, matrix):
        '''
        умножение матрицы на матрицу  ( Mt * Mr )

        matrix - другая матрица
        возвращает матрицу Matrix
        создает матрицу
        a b 0
        c d 0
        e f 1
        '''
        a = self.matrix[0][0] * matrix[0][0] + self.matrix[0][1] * matrix[1][0] + self.matrix[0][2] * matrix[2][0]
        b = self.matrix[0][0] * matrix[0][1] + self.matrix[0][1] * matrix[1][1] + self.matrix[0][2] * matrix[2][1]
        c = self.matrix[1][0] * matrix[0][0] + self.matrix[1][1] * matrix[1][0] + self.matrix[1][2] * matrix[2][0]
        d = self.matrix[1][0] * matrix[0][1] + self.matrix[1][1] * matrix[1][1] + self.matrix[1][2] * matrix[2][1]
        e = self.matrix[2][0] * matrix[0][0] + self.matrix[2][1] * matrix[1][0] + self.matrix[2][2] * matrix[2][0]
        f = self.matrix[2][0] * matrix[0][1] + self.matrix[2][1] * matrix[1][1] + self.matrix[2][2] * matrix[2][1]
        return Matrix3(a, b, c, d, e, f)


    def __repr__(self):
        '''
        представление объекта в виде строки
        a b 0
        c d 0
        e f 1
        '''
        return "{}\t{}\t{}\n{}\t{}\t{}\n{}\t{}\t{}".format(self[0][0],self[0][1],self[0][2],self[1][0],self[1][1],self[1][2],self[2][0],self[2][1],self[2][2])


    def __getitem__(self, index):
        return self.matrix[index]

    
if __name__ == '__main__':
    def test(res, req):
        print('req =', req, 'res = ', res, end='')
        if (round(res[0], 4), round(res[1], 4)) != (round(req[0], 4), round(req[1], 4)):
            print(' !!! Неудача')
        else:
            print(' Успех')


    m = Matrix3(1, 2, 3, 4, 5, 6)
    print(m) # тест печати
    test(Matrix3().mult_vector((10, 20, 1)), (10, 20)) # тест единичной матрицы
    m = Matrix3()
    m.translate(1, 1)
    print(m)
    test(m.mult_vector((10, 20, 1)), (11, 21)) # тест переноса
    m = Matrix3()
    m.scale(0.5, 0.5) 
    print(m)
    test(m.mult_vector((10, 20, 1)), (5, 10)) # тест масштабирования
    m = Matrix3()
    m.rotate(pi / 4) 
    print(m)
    test(m.mult_vector((20, 0, 1)), (20 * sqrt(2) / 2, 20 * sqrt(2) / 2)) # тест поворота
    m1 = Matrix3()
    m1.translate(10, 10) 
    m2 = Matrix3()
    m2.scale(0.5, 2) 
    m = m1 * m2 
    print(m1)
    print(m2)
    print(m)
    test(m.mult_vector((10, 20, 1)), (10, 60)) # тест перемножения матриц, комбинация транформаций
