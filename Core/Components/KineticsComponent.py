# coding= utf-8
from Core.Vector import *
from Core.Game import *
from Core.Component import Component

# Possibilitará a presença de cinética dentro de um gameobject
class KineticsComponent(Component):
    def __init__(self):
        super().__init__()
        self.velocity = Vector2(0, 0)
        self.__lastVelocity = self.velocity

        self.setVelocity(Vector2(0, 0))
        self.setGravity()
        self.gravityActivated = True

    def setGravity(self, gravityForce = 9.8):
        self.gravityForce = Vector2(0, gravityForce * 100)

    def disableGravity(self):
        self.gravityActivated = False

    def enableGravity(self):
        self.gravityActivated = True

    def addForce(self, force):
        self.velocity += force
        
    def setVelocity(self, velocity):
        self.__lastVelocity = self.velocity
        self.velocity = velocity
    
    def undoMoviment(self):
        self.gameObject.translate(self.__lastVelocity * -1)

    def _update(self):
        if(self.gravityActivated):
            self.velocity += self.gravityForce

        self.gameObject.translate(self.velocity)