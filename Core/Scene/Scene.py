# coding=utf-8

from Core.Scene.SceneManager import SceneManager
from Core.Components.Abstracts.DrawingComponent import DrawingComponent
from Core.GameObject import GameObject

class Scene:
    def __init__(self, sceneName):
        # Objetos padrões usados para iniciar a cena, não deverão ser modificados
        self.__gameObjects = []

        self.__sceneName = sceneName
        self.__activated = False

        SceneManager.addScene(self)
        SceneManager.beforeSceneChange(self.__beforeSceneChangeHandler)
        SceneManager.afterSceneChange(self.__afterSceneChangeHandler)
        
# ------------------------- GAMEOBJECT ----------------------
    def addGameObject(self, gameObject: GameObject):
        ''' Adiciona uma gameobject à cena.'''
        self.__gameObjects.append(gameObject)
        
        if(self.__activated):
            gameObject.forceInit()
            
        return self
    
    """ Método e ideia descontinuada
    def addGameObjectToScene(self, gameObject: GameObject, forceInit = True):
        ''' Adiciona uma gameobject à cena em execução '''
        from copy import deepcopy
        
        gameObject.forceInit()
        
        self.__gameObjects.append(gameObject.copy()) 
    """
    
    def removeGameObject(self, gameObject):
        if gameObject in self.__gameObjects:
	        self.__gameObjects.remove(gameObject)

    def getGameObjects(self):
        return self.__gameObjects

    def getGameObjectWithName(self, name):
        for gameObject in self.__gameObjects:
            if(gameObject.getName() == name):
                return gameObject
        return None

# --------------------- MANIPULADORES DE CENA ----------------
    def getSceneName(self):
        return self.__sceneName

    def activeScene(self):
        self.__enableScene()

# ---------------------- LIFE CYCLE ---------------------------
    def play(self):        
        # Update
        for gameObject in self.__gameObjects:
            gameObject.update()

        # Desenho
        for gameObject in self.__gameObjects:
            gameObject.draw()

# ------------------------- GAMEOBJECT ----------------------
    def __startGameObjects(self):        
        for gameObject in self.__gameObjects:
            gameObject.awake()

        for gameObject in self.__gameObjects:
            gameObject.start()
    
    def __destroyAllGameObjects(self):
        try:
            while(len(self.__gameObjects) > 0):
                self.__gameObjects[0].destroy()
        except:
            exit()
    
# --------------------- MANIPULADORES DE CENA ----------------
    def __enableScene(self): 
        if(not self.__activated):
            self.__startGameObjects()
            self.__activated = True
        
    def __disableScene(self):
        if(self.__activated):
            #self.__destroyAllGameObjects()
            self.__activated = False

# ---------------------- EVENTS ---------------------------
    def onActiveScene(self):
        pass
    
    def onDeactiveScene(self):
        pass
    
    def __afterSceneChangeHandler(self, new_scene):
        if(self.getSceneName() == new_scene.getSceneName()):
            self.activeScene()
            self.onActiveScene()
            
    def __beforeSceneChangeHandler(self, current_scene):
        if(self.getSceneName() == current_scene.getSceneName()):
            self.__disableScene()
            self.onDeactiveScene()