class GameStateManager:
    
    __events = []
    
    instance = None
    
#-------------------- Game States ------------------
    MAIN_MENU = 1
    RANKING_MENU = 2
    
    GAMEPLAY = 10
    PAUSED = 11
    WAITING = 12
    GAME_OVER = 13
    
    __currentGameState = None
   
    def __init__(self):
        from Core.Scene.SceneManager import SceneManager
                
        if(self.instance == None):
            GameStateManager.instance = self
            SceneManager.onSceneChange(self.__sceneChangeHandler)
    
    def changeGameState(self, gameState):
        self.__currentGameState = gameState
        self.onChangeHandler()
    
    def getGameState(self):
        return self.__currentGameState
    
    def onChange(self, func):
        self.__events.append(func)
    
    def onChangeHandler(self):
        for event in self.__events:
            event(self.__currentGameState)
    
    def __sceneChangeHandler(self, fromScene, toScene):
        self.__events = []
    
    @classmethod
    def isGameState(cls, gameState):
        if(not GameStateManager.instance):
            x = GameStateManager()
        return cls.instance.getGameState() == gameState