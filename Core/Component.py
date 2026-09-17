# coding= utf-8

# Classe que representa um comportamento de um gameobject.
class Component:
    def __init__(self):
        pass

    def start(self):
        self._start()

    def update(self):
        self._update()
        self.afterUpdated()

    def afterUpdated(self):
        pass

    def setGameObject(self, gameObject):
        ''' Seta a instância do gameobject ao qual o componente pertence '''
        self.gameObject = gameObject
    
    def _update(self):
        raise NotImplementedError("O metodo deve ser sobrescrito")
    
    def _start(self):
        pass