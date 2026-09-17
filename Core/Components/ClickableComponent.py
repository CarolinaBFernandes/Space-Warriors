# coding= utf-8
from Core.Vector import *
from Core.Game import *
from Core.Component import Component

class ClickableComponent(Component):
    ''' Componente que injeta os eventos de click do mouse no GameObject. 
    Apenas o LMB será levado em consideração ''' 
 
    def __init__(self):
        super().__init__()
        self.dataKey = {
            'pressed': False,
            'is_pressing_element': False,
			'start': None,
			'finish': None
		}
        self.mouse = Game.getMouse()
        
    def update(self):
        if(self.mouse.is_button_pressed(1)):
            if(self.mouse.is_over_object(self.gameObject) and not self.dataKey['pressed']):
                self.__onKeyDown()
                
            self.__onKeyPressed()
        else:
            if(self.dataKey['pressed'] and self.mouse.is_over_object(self.gameObject)):
                if(self.dataKey['is_pressing_element']):
                    self.__onClick()
                self.__onKeyUp()
                self.dataKey['is_pressing_element'] = False

            self.dataKey['pressed'] = False

    def clickDeltaTime(self):
        ''' Obtém o tempo ocorrido entre o início e o fim do click. Retorna -1 se o DeltaTima não estiver definido '''
        if(self.dataKey['start'] and self.dataKey['finish']):
            return self.dataKey['finish'] - self.dataKey['start']
        return -1
        
    def __onClick(self):
        ''' Evento ativado quando o LMB é pressionado e solto em cima do GameObject '''
        self.dataKey['is_pressing_element'] = False

        self.gameObject.onClick()
    
    def __onKeyDown(self):
        ''' Evento ativado quando o LMB é pressionado em cima do GameObject '''
        self.dataKey['is_pressing_element'] = True
        self.dataKey['start'] = Game.window.time_elapsed()
        self.dataKey['finish'] = None

        self.gameObject.onKeyDown()

    def __onKeyPressed(self):
        ''' Evento ativado quando o LMB é pressionado em qualquer lugar da tela '''
        self.dataKey['pressed'] = True

        self.gameObject.onKeyPressed()
    
    def __onKeyUp(self):
        ''' Evento ativado quando o LMB é solto em cima do GameObject '''
        self.dataKey['is_pressing_element'] = False
        self.dataKey['finish'] = Game.window.time_elapsed()
        self.dataKey['pressed'] = False
        
        self.gameObject.onKeyUp()
        