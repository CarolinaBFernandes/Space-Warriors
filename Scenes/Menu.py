from Core.Builders.GameObjectBuilder import GameObjectBuilder
from Core.Scene.Scene import Scene
from Core.Vector import Vector2
from Core.Game import Game
from Core.PPlay.sound import Sound
from Core.GameStateManager import GameStateManager

from Core.Components.SpriteComponent import SpriteComponent

from GameObjects.UI._Text import UIText
from GameObjects.UI.CloseButton import CloseButton
from GameObjects.UI.PlayButton import PlayButton
from GameObjects.UI.RankingButton import RankingButton
from GameObjects.UI.SettingsButton import SettingsButton
from GameObjects.UI.RankingText import RankingText

music = Sound('assets/songs/soundtrack/menu.mp3')

def build(name):
    scene = createScene(name)
    addChangeEvent(scene)
    return scene

def startGame():
    from Core.Scene.SceneManager import SceneManager
    
    SceneManager.changeScene('gameplay')

def openRanking():
    GameStateManager.instance.changeGameState(GameStateManager.RANKING_MENU)

def closeGame():
    Game.window.close()

def settings():
    print('Funcionalidade não implementada!')

def onActiveScene():
    from Core.GameStateManager import GameStateManager
    global music
    
    GameStateManager.instance.changeGameState(GameStateManager.MAIN_MENU)
    music.play()

def onDeactiveScene():
    music.stop()

def addChangeEvent(scene):
    scene.onActiveScene = onActiveScene
    scene.onDeactiveScene = onDeactiveScene
        
def createScene(name):
    scene = Scene(name)
    
    # Start button
    start_button = GameObjectBuilder().startBuild(PlayButton())\
        .setName('start_button')\
        .setPosition(Game.getWindowCenter() - GameObjectBuilder().instance.getObjectCenter())\
        .build()
    start_button.onClick = startGame
    start_button.setText('Novo Jogo')
    
    # Ranking button
    ranking_button = GameObjectBuilder().startBuild(RankingButton())\
        .setName('ranking_button')\
        .setPosition(
			Game.getWindowCenter() - 
			GameObjectBuilder().instance.getObjectCenter() + 
			Vector2(0, GameObjectBuilder.instance.getSize().y + 20)
		)\
        .build()
    ranking_button.onClick = openRanking
    ranking_button.setText('Ranking')
    
    # Settings button
    """ settings_button = GameObjectBuilder().startBuild(SettingsButton())\
        .setName('settings_button')\
        .setPosition(
			Game.getWindowCenter() - 
			GameObjectBuilder().instance.getObjectCenter() + 
			Vector2(0, GameObjectBuilder.instance.getSize().y * 2 + 20 * 2)
		)\
        .build()
    settings_button.onClick = settings
    settings_button.setText('Opções') """
        
    # Close button
    close_button = GameObjectBuilder().startBuild(CloseButton())\
        .setName('close_button')\
        .setPosition(
			Game.getWindowCenter() - 
			GameObjectBuilder().instance.getObjectCenter() + 
			#Vector2(0, GameObjectBuilder.instance.getSize().y * 3 + 20 * 3)
			Vector2(0, GameObjectBuilder.instance.getSize().y * 2 + 20 * 2)
		)\
        .build()
    close_button.onClick = closeGame
    close_button.setText('Sair')
    
    # Texto do ranking
    ranking_text = RankingText()
    
    # Game Title
    title = Game.WINDOW_TITLE
    game_title = GameObjectBuilder().startBuild(UIText())\
        .setName('game_title')\
        .setPosition(
			Game.getWindowCenter() -
			Vector2(len(title) * 30, Game.WINDOW_HEIGHT / 3)
		).build()
    game_title.configureText(80, (24, 42, 168))
    game_title.setText(title)
    
    # Adição dos objetos na cena
    scene\
        .addGameObject(start_button)\
        .addGameObject(ranking_button)\
        .addGameObject(close_button)\
        .addGameObject(game_title)\
        .addGameObject(ranking_text)
        #.addGameObject(settings_button)\
    return scene