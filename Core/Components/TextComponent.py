# coding= utf-8
from Core.Component import *
from Core.PPlay.sprite import *
from Core.Game import Game
from pygame import *

from .Abstracts.DrawingComponent import *

# Componente utilizado para a renderização de textos
# Não será possível obter o tamanho dos textos escritos pois seria necessário o uso explícito do pygame
class TextComponent(DrawingComponent):
    def __init__(self):
        super().__init__()
        self.font_color = (255, 255, 255)
        self.font_family = 'assets/fonts/kenvector_future.ttf'
        self.font_size = 12
        self.text = ""
        
        self.font = None
    
    def _start(self):
        if(len(self.font_family.split('/')) > 0):
            self.font = pygame.font.Font(self.font_family, self.font_size)
        else:
        	self.font = pygame.font.SysFont(self.font_family, self.font_size, False, False)
    
    def _update(self):
        pass

    def draw(self):
        lines = self.text.splitlines()
        for i, l in enumerate(lines):
            Game.window.screen.blit(self.font.render(l, 0, self.font_color), (self.gameObject.x, self.gameObject.y + self.font_size*i))
        
    def setText(self, text):
        self.text = text
        return self
        
    def setFontSize(self, fontSize):
        self.font_size = fontSize
        return self
        
    def setFontFamily(self, fontFamily):
        self.font_family = fontFamily
        return self
        
    def setFontColor(self, color):
        self.font_color = color
        return self
