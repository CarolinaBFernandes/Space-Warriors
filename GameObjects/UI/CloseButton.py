# coding= utf-8
from Core.Components.KineticsComponent import KineticsComponent
from Core.Components.SpriteComponent import SpriteComponent
from Core.GameObject import *
from Core.Vector import Vector2
from Core.Game import *
from Core.GameStateManager import GameStateManager

from GameObjects.UI._Button import UIButton;

# Classe responsável por representar a bola do Pong
class CloseButton(UIButton):
    def __init__(self):
        super().__init__()
        
        closeSprite = SpriteComponent('assets/images/sprites/ui/button_red.png')
        self.addComponent(closeSprite)

    def _awake(self):
        super()._awake()

    def _start(self):
        super()._start()
        GameStateManager.instance.onChange(self.gameStateChangesHandler)

    def _update(self):
        pass

    def onClick(self):
        Game.window.close()
    
    def gameStateChangesHandler(self, gameState):
        if(gameState == GameStateManager.MAIN_MENU):
            self.enable()
        else:
            self.disable()