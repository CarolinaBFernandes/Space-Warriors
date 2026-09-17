# coding=utf-8

from Core.GameObject import GameObject
from Core.Game import Game
from Core.Vector import Vector2

from Core.Components.TextComponent import TextComponent
from Core.GameStateManager import GameStateManager

from GameObjects.UI._Text import UIText
class TimerDisplay(UIText):
    def __init__(self):
        super().__init__()
        self.timer_total = 100
        self.timer_current = self.timer_total
        self.__tick_size = 1
        self.__tick = self.__tick_size
        
        self.__is_ticking = False
    
    def _start(self):
        super()._start()
        self.configureText(color=(164, 220, 220))
        
    def _update(self):
        if(GameStateManager.isGameState(GameStateManager.GAMEPLAY) and self.__is_ticking):
            self.setText('%02d:%02d' % (self.timer_current // 60, self.timer_current % 60))
            self.setPosition(Vector2((Game.WINDOW_WIDTH / 2 - len(self.text_string) / 2 * self.getFontSize()), 16))
            self.text.setText(self.text_string)
            
            self.__tickTimer()
        
        """ self.setText('%02d:%02d' % (self.timer_current // 60, self.timer_current % 60))
        self.setPosition(Vector2((Game.WINDOW_WIDTH / 2 - len(self.text_string) / 2 * self.getFontSize()), 16))
        self.text.setText(self.text_string)
        
        self.__tickTimer() """
    
    def pause(self):
        self.__is_ticking = False
    
    def play(self):
        self.__is_ticking = True
    
    def setTimer(self, seconds):
        self.timer_total = seconds
        self.timer_current = seconds
        
    def __tickTimer(self):
        self.__tick -= Game.DELTA_TIME
        if(self.__tick <= 0):
            self.timer_current -= 1
            self.__tick = self.__tick_size
            
            if(self.timer_current <= 0):
                self._dispatchEvent('onTimerEnds', True)