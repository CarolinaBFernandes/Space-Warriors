# coding= utf-8
from Core.Component import *
from Core.PPlay.sprite import *
from Core.Game import Game
from Core.Component import Component

from .Abstracts.DrawingComponent import *
from copy import deepcopy

# Adicionará sprites aos gameobjects
class SpriteComponent(DrawingComponent):
    def __init__(self, spritePath):
        super().__init__()
        self.changeSprite(spritePath)
    
    def changeSprite(self, spritePath):
        self.sprite = pygame.image.load(spritePath).convert_alpha()        
    
    def _update(self):
        pass
    
    def setGameObject(self, gameObject):
        super().setGameObject(gameObject)
        self.gameObject.setSize(self.sprite.get_width(), self.sprite.get_height())
        self.gameObject.transform.onRotate(self.rotate)

    def draw(self):
        Game.window.get_screen().blit(self.sprite, (self.gameObject.x, self.gameObject.y))

    def rotate(self, angle):
        self.sprite = pygame.transform.rotate(self.sprite, self.gameObject.transform.rotateAngle)