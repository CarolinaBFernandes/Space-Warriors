# coding= utf-8
from Core.Component import *
from Core.PPlay.sprite import *

# Classe base para componentes que precisam ser desenhados na tela
class DrawingComponent(Component):
    def __init__(self):
        super().__init__()

    def draw(self):
        raise NotImplementedError(f'O método draw() da classe {self.__class__} deve ser implementado')

    def rotate(self):
        raise NotImplementedError(f'O método rotate() da classe {self.__class__} deve ser implementado')