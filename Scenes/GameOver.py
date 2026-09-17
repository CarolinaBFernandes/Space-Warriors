#coding=utf-8

from Core.Scene.Scene import Scene

def build(name):
    scene = createScene(name)
    addChangeEvent(scene)
    return scene

def onActiveScene():
    from Core.GameStateManager import GameStateManager
    global obstacle_spawner
    
    GameStateManager.instance.changeGameState(GameStateManager.GAME_OVER)

def addChangeEvent(scene):
    scene.onActiveScene = onActiveScene

def createScene(name):
    from GameObjects.UI.GameOver import GamerOver
    
    scene = Scene(name)
    
    # ------------------------------- GAME OVER TEXT ----------------------------------
    game_over = GamerOver()    
    
    
    
    # ------------------------------- ADICIONAR A CENA --------------------------------
    scene.addGameObject(game_over)
    
    
    return scene