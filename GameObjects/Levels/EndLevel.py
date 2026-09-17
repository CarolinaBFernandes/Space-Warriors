#coding=utf-8

from Core.GameObject import GameObject
from Core.PPlay.sound import Sound
from Core.Game import Game
from Core.Scene.SceneManager import SceneManager
from Core.GameStateManager import GameStateManager

from GameObjects.Spawner import Spawner
from GameObjects.UI._Text import UIText

class EndLevel(GameObject):
    def __init__(self, text):
        super().__init__()
        self.soundtrack: Sound = None
        self.__activated = False
        self.__text = text
        
    def setSoundTrack(self, music_name):
        self.soundtrack = Sound(music_name)
    
    def active(self):
        from GameObjects.Levels.LevelNameLabel import LevelNameLabel
        
        timer = Game.findGameObjectWithName('timer_hub')
        timer.pause()
        
        level_label = LevelNameLabel(self.__text)
        SceneManager.addGameObjectToCurrentScene(level_label)
        
        GameStateManager.instance.changeGameState(GameStateManager.WAITING)
        self.__activated = True
    
    def start(self):
        self.save()
        
    def deactive(self):
        self.soundtrack.stop()
            
        self.__activated = False
        
        self.save()
    
    def findSpawnerWithName(self):
        return None
    
    def save(self):
        from Core.FileScoreManager import gravaPontuacao
        
        nome_jogador = input("Digite o nome para aparecer no ranking: ")
        
        current_ranking = gravaPontuacao((nome_jogador, Game.score))
        
        Game.window.close()
    
    def onLevelChanges(self, level):
        if(level == self):
            self.active()
        else:
            if self.__activated:
                self.deactive()