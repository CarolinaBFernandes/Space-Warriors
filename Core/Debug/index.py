# conding=utf-8

from Core.Game import Game
from Core.Scene.Scene import Scene

from Core.Debug.GameObjects.FramerateDisplay import FramerateDisplay


def createDebugScene():
    scene = Scene('debug')
    
    Game.debug['scene'] = scene

def showFramerate():
    display = FramerateDisplay()
    
    Game.debug['scene'].addGameObject(display)