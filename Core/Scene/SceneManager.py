# coding=utf-8
from Core.GameObject import GameObject

class SceneManager:

    __scenes = {}
    __currentScene = None
    __onSceneChangeEvent = []
    __beforeSceneChangeEvent = []
    __afterSceneChangeEvent = []

    @classmethod
    def addScene(cls, scene):
        cls.__scenes[scene.getSceneName()] = scene

    @classmethod
    def getSceneByIndex(self, index: int):
        sceneName = list(self.__scenes.keys())[index]
        return self.__scenes[sceneName]

    @classmethod
    def changeScene(cls, sceneName: str):
        current_scene = cls.getCurrentScene()
        new_scene = cls.__scenes[sceneName]
        
        if(current_scene):
	        cls.__beforeSceneChangeHandler(current_scene)
         
        cls.__sceneChangeHandler(current_scene, new_scene)
        cls.__afterSceneChangeHandler(new_scene)
        
    @classmethod
    def addGameObjectToCurrentScene(cls, gameObject: GameObject):
        cls.getCurrentScene().addGameObject(gameObject)
    
    @classmethod
    def removeGameObjectToCurrentScene(cls, gameObject: GameObject):
        cls.getCurrentScene().removeGameObject(gameObject)

    @classmethod
    def getCurrentScene(cls):
        return cls.__currentScene

    @classmethod
    def onSceneChange(cls, function):
        cls.__onSceneChangeEvent.append(function)
    
    @classmethod
    def beforeSceneChange(cls, function):
        cls.__beforeSceneChangeEvent.append(function)
        
    @classmethod
    def afterSceneChange(cls, function):
        cls.__afterSceneChangeEvent.append(function)

    @classmethod
    def __sceneChangeHandler(cls, fromScene, toScene):
        for event in cls.__onSceneChangeEvent:
            event(fromScene, toScene)
            
        cls.__currentScene = toScene

    @classmethod
    def __beforeSceneChangeHandler(cls, currentScene):
        for event in cls.__beforeSceneChangeEvent:
            event(currentScene)
            
    @classmethod
    def __afterSceneChangeHandler(cls, newSene):
        for event in cls.__afterSceneChangeEvent:
            event(newSene)