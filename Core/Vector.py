# coding= utf-8

# Classe dedicada à manipulação de vetores bi-dimensionais
class Vector2:
    def __init__(self, x, y):
        self.x = x
        self.y = y


    def normalize(self):
        ''' Retorna uma nova instancia do vetor dado de forma unitária '''
        if(self.x == 0 and self.y == 0):
            return Vector2.zero()
        return Vector2(self.x, self.y) * (1/((self.x**2 + self.y**2)**(1/2)))

#------------------------GETTERS PRIVADOS-------------------------------
    def zero():
        ''' Retorna uma instancia do vetor nulo '''
        return Vector2(0, 0)
    
    def up():
        ''' Retorna uma instancia do vetor unitário que aponta para cima '''
        return Vector2(0, 1)
    
    def down():
        ''' Retorna uma instancia do vetor unitário que aponta para baixo '''
        return Vector2(0, -1)
    
    def left():
        ''' Retorna uma instancia do vetor unitário que aponta para esquerda '''
        return Vector2(-1, 0)
    
    def right():
        ''' Retorna uma instancia do vetor unitário que aponta para direita '''
        return Vector2(1, 0)

#------------------------MÉTODOS PRIVADOS-------------------------------
    def __normalize(self):
        pass
    

#------------------------MÉTODOS PADRÕES DA LINGUAGEM-------------------------------
    def __add__(self, vector2):
        return Vector2(self.x + vector2.x, self.y + vector2.y)
    
    def __sub__(self, vector2):
        return Vector2(self.x - vector2.x, self.y - vector2.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def __truediv__(self, scalar):
        return Vector2(self.x * 1.0 / scalar, self.y * 1.0 / scalar)

    def __repr__(self):
        return f'({self.x},{self.y})'