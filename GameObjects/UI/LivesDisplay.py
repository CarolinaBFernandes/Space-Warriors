# coding=utf-8

from Core.GameObject import GameObject
from Core.Game import Game
from Core.Vector import Vector2

from Core.Components.TextComponent import TextComponent

class LivesDisplay(GameObject):
    def __init__(self):
        super().__init__()
        self.livesMarginRight = 8
        
    def _start(self):
        Game.player.addEventListener('onTookDamage', self.playerTookDamageHandler)
        livesQnt = Game.player.lives
        position = Vector2(
			16,
			16 if not Game.DEVELOPMENT_MODE else 48 # Margin dada por conta da exibição dos framerates
        )
        
        self.setPosition(position)
        for i in range(livesQnt):
            self.addLive()
        
    def playerTookDamageHandler(self, lives):
        self.removeLive()
        
    def addLive(self):
        from Core.Components.SpriteComponent import SpriteComponent
        live = GameObject()
        live.addComponent(SpriteComponent('assets/images/sprites/ui/player_life1_blue.png'))
        
        self.addChild(live)
        
        live.setLocalPosition(Vector2(
            live.width * (len(self.transform.children) - 1) + self.livesMarginRight * (len(self.transform.children) - 1), 
            0
        ))
    
    def removeLive(self):
        self.removeChild(self.transform.children[-1])
    