# coding= utf-8
from Core.Components.KineticsComponent import KineticsComponent
from Core.Components.SpriteComponent import SpriteComponent
from Core.GameObject import *
from Core.Vector import Vector2
from Core.Game import *

from GameObjects.UI._Button import UIButton;

# Classe responsável por representar a bola do Pong
class DifficultyChangeButton(UIButton):
    def __init__(self):
        super().__init__()
        self.difficulty = 1

    def onClick(self):
        Game.findGameObjectWithName('settings_menu').enabled = False
        Game.findGameObjectWithName('main_menu').enabled = True
        Game.findGameObjectWithName('ranking_menu').enabled = False

        Game.GAME_DIFFICULTY = self.difficulty
