# coding=utf-8

from Core.GameObject import GameObject
from Core.Game import Game
from Core.Vector import Vector2
from Core.GameStateManager import GameStateManager

from Core.Components.TextComponent import TextComponent
from Core.FileScoreManager import obterPontuacao

from math import floor

class RankingText(GameObject):
    def __init__(self):
        super().__init__()
    
    def _awake(self):
        self.text = TextComponent()
        self.addComponent(self.text)
        
        GameStateManager.instance.onChange(self.gameStateChangesHandler)
        
    def _start(self):
        self.text.setFontSize(24)
        ranking = obterPontuacao()
        text = ''
        text_continue = 'Pressione ESC para retornar ao menu'
        max_len = len(text_continue)
                
        for score in ranking:
            text_len = len(score[0]) + len(score[1])
            text += f'{score[0]}'
            for i in range(floor((max_len - text_len) * .9)):
                text += ' . '
            text += f'{score[1]}\n'
        
        text += '\nPressione ESC para retornar ao menu'
        
        self.text.setText(text)
        self.setPosition(Vector2(
            Game.WINDOW_WIDTH / 2 - max_len * 10 / 2, 
            Game.WINDOW_HEIGHT / 2
        ))
    
    def _update(self):
        if(Game.getKeyboard().key_pressed('ESC')):
            GameStateManager.instance.changeGameState(GameStateManager.MAIN_MENU)
    
    def gameStateChangesHandler(self, gameState):
        if(gameState == GameStateManager.RANKING_MENU):
            self.enable()
        else:
            self.disable()