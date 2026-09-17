# coding= utf-8
from Core.GameObject import GameObject
from Core.Vector import Vector2
from Core.Game import Game
from Core.GameStateManager import GameStateManager

from Core.Components.ClickableComponent import ClickableComponent
from Core.Components.TextComponent import TextComponent

from GameObjects.UI._Text import UIText

# Classe responsável por representar a bola do Pong
class UIButton(GameObject):
    def __init__(self):
        super().__init__()
        self.text_container = None
        
    def _awake(self):
        self.text_container = UIText()

        self.addComponent(ClickableComponent())
        self.addChild(self.text_container)
    
    def setText(self, text):
        self.text_container.setText(text)
    