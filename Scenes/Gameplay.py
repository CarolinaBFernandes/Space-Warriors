#coding=utf-8

from Core.Builders.GameObjectBuilder import GameObjectBuilder
from Core.Scene.Scene import Scene
from Core.Vector import Vector2
from Core.Game import Game

from GameObjects.Levels.LevelManager import LevelManager

obstacle_spawner = None

def build(name):
    scene = createScene(name)
    addChangeEvent(scene)
    return scene

def onActiveScene():
    from Core.GameStateManager import GameStateManager
    global obstacle_spawner
    
    GameStateManager.instance.changeGameState(GameStateManager.GAMEPLAY)
    obstacle_spawner.active()
    LevelManager.instance.startGame()

def addChangeEvent(scene):
    scene.onActiveScene = onActiveScene
    
def createScene(name):
    from GameObjects.Player import Player
    from GameObjects.UI.LivesDisplay import LivesDisplay
    from GameObjects.UI.ScoreDisplay import ScoreDisplay
    from GameObjects.UI.TimerDisplay import TimerDisplay
    from GameObjects.Spawner import Spawner
    from GameObjects.Enemies.EnemyDefault import EnemyDefault
    from GameObjects.Enemies.Enemy2 import Enemy2
    from GameObjects.Enemies.Enemy3 import Enemy3
    from GameObjects.Obstacles._Obstacle import ObstacleBase
    from GameObjects.Obstacles.MeteorMed import MeteorMed
    from GameObjects.Levels.Level import Level
    from GameObjects.Levels.EndLevel import EndLevel
    from Core.Config import get_config
    
    global obstacle_spawner
    
    config = get_config()
    
    scene = Scene(name)
    
    # Player
    player = Player()
    player.setPosition(
        Vector2(Game.WINDOW_WIDTH / 2, Game.WINDOW_HEIGHT) -
		Vector2(player.width / 2, player.height)
    )
    
    # ------------------------------- HUBS --------------------------------
    # Display de vida
    lives_hub = LivesDisplay()
    lives_hub.setName('liver_hub')
    
    score_hub = ScoreDisplay()
    score_hub.setName('score_hub')
    
    timer_hub = TimerDisplay()
    timer_hub.setName('timer_hub')
    
    
    
    
    # ------------------------------- SPAWNS --------------------------------
    enemy_spawner = Spawner()
    enemy_spawner.setName('enemy_spawner')
    enemy_spawner_2 = Spawner()
    enemy_spawner_2.setName('enemy_spawner')
    enemy_spawner_3 = Spawner()
    enemy_spawner_3.setName('enemy_spawner')
    
    enemy_1 = EnemyDefault()
    enemy_2 = Enemy2()
    enemy_2.difficulty = 4
    enemy_3 = Enemy3()
    enemy_3.difficulty = 8
    
    
    enemy_spawner.add(enemy_1)
    enemy_spawner.add(enemy_2)
    
    enemy_spawner_2.add(enemy_2)
    enemy_spawner_2.add(enemy_3)
    
    enemy_spawner_3.add(enemy_1)
    enemy_spawner_3.add(enemy_2)
    enemy_spawner_3.add(enemy_3)
    
    obstacle_spawner = Spawner()
    obstacle_spawner.setRespawnDelay(5)
    obstacle_spawner.setRespawnDelayMin(3)
    obstacle_spawner.setName('obstacle_spawner')
    
    meteor_1 = ObstacleBase()
    meteor_1.difficulty = 3
    meteor_2 = MeteorMed()
    meteor_2.difficulty = 7
    
    obstacle_spawner.add(meteor_1)
    obstacle_spawner.add(meteor_2)
    
    
    
    
    # ------------------------------- LEVELS --------------------------------
    lvl_manager = LevelManager() # Apenas instancia o singleton
    levels = config['levels']
    
    level_spawners = [enemy_spawner, enemy_spawner_2, enemy_spawner_3]
    i = 0
    for key in levels:
        level_config = levels[key]
        
        try:
            level = Level(
				level_config['time'], 
				level_config['text'], 
				level_config['pool_size'], 
				level_config['respawn_delay_base']
        	)
            
            level.addSpawner(level_spawners[i])            
        except:
            level = EndLevel(level_config['text'])
        
        level.setSoundTrack(level_config['music'])
        i += 1
        
        LevelManager.instance.addLevel(level)
    
    
    
    # ------------------------------- ADICIONAR A CENA --------------------------------
    scene.addGameObject(player)
    scene.addGameObject(lives_hub)
    scene.addGameObject(score_hub)
    scene.addGameObject(timer_hub)
    scene.addGameObject(obstacle_spawner)
    
    
    return scene