# coding= utf-8
from Core.Vector import *
from Core.Game import *
from Core.Component import Component

# Possibilitará a presença de cinética dentro de um gameobject
class CollisionComponent(Component):
    def __init__(self):
        super().__init__()
        self.objects = []
        self.objects_perfects = []
        self.collidedList = []
        
    def addCollisionWith(self, gameObject):
        if(isinstance(gameObject, list)):
            self.objects.extend(gameObject)
        else:
            self.objects.append(gameObject)
    
    def addCollisionPerfectWith(self, gameObject):
        if(isinstance(gameObject, list)):
            self.objects_perfects.extend(gameObject)
        else:
            self.objects_perfects.append(gameObject)

    def _update(self):
        self.collidedList = []
        
        for obj in self.objects:
            if(obj.enabled and self.gameObject.collided(obj)):
                self.collidedList.append(obj)
                self.onCollided(obj)
                
        for obj in self.objects_perfects:
            if(obj.enabled and self.gameObject.collided(obj)):
                self.collidedList.append(obj)
                self.onCollided(obj)
                
    def isColliding(self):
        return len(self.collidedList) > 0
 
    def onCollided(self, gameObject):
        gameObject.onCollided(self.gameObject)
        self.gameObject.onCollided(gameObject)