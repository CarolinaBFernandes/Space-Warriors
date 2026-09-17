# coding= utf-8
from Core.GameObject import GameObject
from Core.Vector import Vector2
from Core.Game import Game

from Core.Components.ClickableComponent import ClickableComponent
from Core.Components.TextComponent import TextComponent

class UIText(GameObject):
    def __init__(self):
        super().__init__()
        self.text_string = ''
        self.__color = None
        self.__font_size = None

    def _awake(self):
        self.text = TextComponent()
        self.addComponent(self.text)
        
        self.configureText()         
        
    def _start(self):
        self.text.setText(self.text_string)
        
        if(self.transform.parent):
            self.setLocalPosition(
            	self.transform.parent.gameObject.getObjectCenter() -
            	Vector2(len(self.text_string) * self.getFontSize() / 2.8, self.getFontSize() / 1.8)
			)
        
    def setText(self, text):
        self.text_string = text
        
    def setColor(self, color):
        self.__color = color
        
    def getFontSize(self):
        if(self.__font_size == None):
            self.__font_size = 22
        return self.__font_size
    
    def setFontSize(self, size):
        self.__font_size = size
        
    def configureText(self, size = 22, color = (128, 172, 164), family = 'assets/fonts/kenvector_future.ttf'):
        self.__color = color
        self.__font_size = size
        
        self.text\
            .setFontColor(self.__color)\
            .setFontSize(self.__font_size)\
            .setFontFamily(family)