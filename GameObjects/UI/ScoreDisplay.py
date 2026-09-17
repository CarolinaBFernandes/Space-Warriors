# coding=utf-8

from Core.GameObject import GameObject
from Core.Game import Game
from Core.Vector import Vector2
from Core.GameStateManager import GameStateManager

from Core.Components.TextComponent import TextComponent


from GameObjects.UI._Text import UIText

class ScoreDisplay(UIText):
    def __init__(self):
        super().__init__()
    
    def _start(self):
        super()._start()
        self.configureText(color=(164, 220, 220))
        
    def _update(self):
        self.setText(f'Score: {Game.score}')
        self.setPosition(Vector2((Game.WINDOW_WIDTH - len(self.text_string) * self.getFontSize()) - 16, 16))
        self.text.setText(self.text_string)