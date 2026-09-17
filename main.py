# coding= utf-8
from Core.Game import *
from Core.Builders.GameObjectBuilder import GameObjectBuilder
from Core.Scene.Scene import Scene
from Core.GameStateManager import GameStateManager

from GameObjects.Player import Player

from Scenes.Menu import build as bsMenu
from Scenes.Gameplay import build as bsGameplay
from Scenes.GameOver import build as bsGameOver

game = Game()
Game.setBackground('assets/images/backgrounds/blue_resized.jpg')
game_state_manager = GameStateManager()

# Instanciação de gameobjects
player = GameObjectBuilder\
    .startBuild(Player())\
    .setName('Player1')\
    .setPosition(Vector2(
        Game.WINDOW_WIDTH / 2 - GameObjectBuilder.instance.width / 2,
        Game.WINDOW_HEIGHT - GameObjectBuilder.instance.height
    ))\
    .build()

menu = bsMenu('main_menu')
gameplay = bsGameplay('gameplay')
game_over = bsGameOver('game_over')

game.start()