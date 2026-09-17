#coding=utf-8
from Core.Game import Game
from GameObjects.Levels.LevelManager import LevelManager

from GameObjects.UI._Text import UIText


class LevelNameLabel(UIText):
    def __init__(self, name):
        super().__init__()
        self.text_string = name
        self.__timer = 5
        
    def _start(self):
        super()._start()
        from Core.Vector import Vector2
        
        self.text.setText(self.text_string)
        
        max_line_lenght = self.__get_max_line_lenght()
        
        self.setPosition(
            Game.getWindowCenter() - Vector2(max_line_lenght * self.getFontSize() / 3, self.getFontSize() / 2)
        )
        
    def _update(self):
        super()._update()
        self.__timer -= Game.DELTA_TIME
        
    def _afterUpdated(self):
        if self.__timer <= 0:
            LevelManager.instance.getCurrentLevel().start()
            Game.findGameObjectWithName('timer_hub').play()
            self.destroy()
            
    def __get_max_line_lenght(self):
        lines = self.text_string.splitlines()
        
        bigger = 0
        for line in lines:
            if(len(line) > bigger):
                bigger = len(line)
        
        return bigger