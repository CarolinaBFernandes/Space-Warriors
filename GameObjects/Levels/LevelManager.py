#coding=utf-8

from Core.GameObject import GameObject
from GameObjects.Levels.Level import Level

class LevelManager(GameObject):
    
    instance = None
    
    def __init__(self):
        super().__init__()
        self.__levels = []
        self.__current_level = 0
        
        if(LevelManager.instance == None):
            LevelManager.instance = self
        
    def addLevel(self, level: Level):
        self.__levels.append(level)
        self.addEventListener('onLevelChanges', level.onLevelChanges)
    
    def onLevelChange(self, level):
        self.__current_level += 1
        
        if self.__current_level >= len(self.__levels):
            self.endGame()
            self._dispatchEvent('onGameEnds', True)
        else:
            self._dispatchEvent('onLevelChanges', self.getCurrentLevel())
    
    def getCurrentLevel(self):
        return self.__levels[self.__current_level]
    
    def findSpawnerWithName(self, name):
        return self.getCurrentLevel().findSpawnerWithName(name)
    
    def startGame(self):
        from Core.Game import Game
        
        self.__levels[0].active()
        Game.findGameObjectWithName('timer_hub').addEventListener('onTimerEnds', self.onLevelChange)
    
    def endGame(self):
        self.__levels[-1].deactive()