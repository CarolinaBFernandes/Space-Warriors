# coding=utf-8

from Core.GameObject import GameObject
from Core.Game import Game
from Core.Vector import Vector2

from Core.Components.TextComponent import TextComponent
from Core.FileScoreManager import gravaPontuacao

from GameObjects.UI._Text import UIText

class GamerOver(UIText):
    def __init__(self):
        super().__init__()
        self.timer = 3
        
        self.__is_ticking = False
    
    def _awake(self):
        super()._awake()
        
        self.setText('Game\nOver')
        self.setFontSize(120)
    
        self.configureText(color=(164, 220, 220))

    def _start(self):
        from Core.Vector import Vector2
        super()._start()
        
        max_line_lenght = self.__get_max_line_lenght()
        
        self.setPosition(
            Game.getWindowCenter() - Vector2(max_line_lenght * self.getFontSize() / 3, self.getFontSize() / 2)
        )
        
    def _update(self):        
        self.__tickTimer()
        
    def __tickTimer(self):
        self.timer -= Game.DELTA_TIME
        if(self.timer <= 0):
            """ salve_text = UIText()
            self.addChild(salve_text)
            salve_text_string = 'Digite seu nome no console.'
            salve_text.setText(salve_text_string)

            salve_text.configureText(20)
            salve_text.setPosition(
				Game.getWindowCenter() - Vector2(
        			len(salve_text_string) * self.getFontSize() / 3, 
           			-200
            	)
            )
            salve_text.update() """
            
            playerName = input("Digite o seu nome: ")
            gravaPontuacao((playerName, Game.score))
                
            Game.window.close()
            
    def __get_max_line_lenght(self):
        lines = self.text_string.splitlines()
        
        bigger = 0
        for line in lines:
            if(len(line) > bigger):
                bigger = len(line)
        
        return bigger