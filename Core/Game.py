# coding= utf-8
from Core.PPlay.window import Window
from Core.Components.Abstracts.DrawingComponent import DrawingComponent
from Core.PPlay.gameimage import GameImage
from Core.Vector import Vector2

from Core.Scene.SceneManager import SceneManager


class Game:
  

#--------------------Configurações do jogo------------------------------
    WINDOW_TITLE = None
    WINDOW_WIDTH = None
    WINDOW_HEIGHT = None

    INITIAL_GAME_DIFFICULTY = None
    SPEED_BASE = None
    SCORE_MULTIPLIER_BASE = None
    
    DEVELOPMENT_MODE = None
#--------------------------------------------------

    GAME_DIFFICULTY = None
    DELTA_TIME = 0
    GAME_MODE = 1

    window = None
    player = None
    debug = {
		'scene': None
	}
    score = 0

    def __init__(self):
        self.__getDefaultConf()
        self.__bootstrap()

#------------------------------- ESTÁTICOS -------------------------------------
    @classmethod
    def getWindowCenter(cls):
        ''' Obtém o ponto central da janela do jogo '''
        return Vector2(
            Game.WINDOW_WIDTH / 2,
            Game.WINDOW_HEIGHT / 2
        )
        
    @classmethod
    def elementOnWindow(cls, element):
        offset = 100
        
        topLeft = Vector2(-element.width - offset, -element.height - offset)
        bottomRight = Vector2(Game.WINDOW_WIDTH + element.width + offset, Game.WINDOW_HEIGHT + element.height + offset)
        
        if(
            element.x < topLeft.x or\
            element.y < topLeft.y or\
            element.x > bottomRight.x or\
            element.y > bottomRight.y
        ):
            return False
        return True

    @classmethod
    def getKeyboard(cls):
        ''' Obtém a atual instância do teclado sendo utilizada '''
        return Game.window.get_keyboard()

    @classmethod
    def getMouse(cls):
        ''' Obtém a atual instância do mouse sendo utilizada '''
        return Game.window.get_mouse()

    @staticmethod
    def findGameObjectWithName(name):
        return SceneManager.getCurrentScene().getGameObjectWithName(name)

    @classmethod
    def developmentMode(cls):
        cls.DEVELOPMENT_MODE = True
    
    @classmethod
    def gameOver(cls):
        from .FileScoreManager import gravaPontuacao
        
        SceneManager.changeScene('game_over')
        

# ------------------------------- ADIÇÃO DE ELEMENTOS -------------------------------------
    @classmethod
    def setBackground(self, backgroundPath):
        ''' Adiciona um background para o Game '''
        self.background = GameImage(backgroundPath)

    @classmethod
    def setPlayer(cls, player):
        ''' Seta o jogador para que o mesmo possa ser visto globalmente '''
        cls.player = player

# ------------------------------- LIFECYCLE -------------------------------------
    def __getDefaultConf(self):
        from Core.Config import get_config
        config = get_config()
        
        Game.WINDOW_TITLE = config['GAME_NAME']
        Game.WINDOW_HEIGHT = config['WINDOW_HEIGHT']
        Game.WINDOW_WIDTH = config['WINDOW_WIDTH']
        Game.INITIAL_GAME_DIFFICULTY = config['INITIAL_GAME_DIFFICULTY']
        Game.SPEED_BASE = config['SPEED_BASE']
        Game.SCORE_MULTIPLIER_BASE = config['SCORE_MULTIPLIER_BASE']
        Game.DEVELOPMENT_MODE = config['DEVELOPMENT_MODE']
    
    def __bootstrap(self):
        window = Window(Game.WINDOW_WIDTH, Game.WINDOW_HEIGHT)
        window.set_title(Game.WINDOW_TITLE)
        Game.GAME_DIFFICULTY = Game.INITIAL_GAME_DIFFICULTY
        
        Game.window = window
    

    def start(self):
        if(Game.DEVELOPMENT_MODE):
            from Core.Debug import index
            
            SceneManager.changeScene(SceneManager.getSceneByIndex(0).getSceneName())

            index.createDebugScene()
            index.showFramerate()
            
            Game.debug['scene'].activeScene()
        else:
            SceneManager.changeScene(SceneManager.getSceneByIndex(0).getSceneName())

        self.__gameLoop()
        
    def __gameLoop(self):
        while(True):
            Game.DELTA_TIME = self.window.delta_time()

            # Desenhando background
            try:
                self.background.draw()
            except Exception:
                Game.window.set_background_color((0, 0, 0))

            SceneManager.getCurrentScene().play()
            
            if(Game.DEVELOPMENT_MODE):
                Game.debug['scene'].play()

            # Atualizando a janela
            Game.window.update()