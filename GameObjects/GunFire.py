# coding= utf-8
from Core.Components.KineticsComponent import KineticsComponent
from Core.Components.SpriteComponent import SpriteComponent
from Core.GameObject import *
from Core.Vector import Vector2
from Core.Game import *
from Core.Builders.GameObjectBuilder import GameObjectBuilder


from GameObjects.Levels.LevelManager import LevelManager

from Core.PPlay.sound import Sound

class GunFire(GameObject):
    def __init__(self):
        super().__init__()
        self.sound = None

    def _awake(self):
        self.addComponent(SpriteComponent('assets/images/sprites/effects/fire01.png'))
        self.addComponent(KineticsComponent())
        self.addComponent(CollisionComponent())

    def _start(self):
        self.enemy_spawn = LevelManager.instance.findSpawnerWithName('enemy_spawner')
        self.obs_spawn = Game.findGameObjectWithName('obstacle_spawner')
        self.setPosition(self.getPosition() - Vector2(self.width / 2, 0))
        
        self.collision = self.getComponent(CollisionComponent)
        self.kinetics = self.getComponent(KineticsComponent)
        self.kinetics.disableGravity()
        self.moveSpeedBase = Game.SPEED_BASE * 2 * Game.GAME_DIFFICULTY
        
        self.kinetics.setVelocity(Vector2(0, -self.moveSpeedBase))
        
        if(self.sound):
            self.sound.loop = False
            self.sound.play()
        
    def setSound(self, soundName):
        self.sound = Sound(soundName)

    def _afterUpdated(self):
        if(self.y < 0):
            self.destroy()
    
    def destroy(self):
        super().destroy()
        self.enemy_spawn.removeEventListener('onSpawn', self._addColisionWith)
        self.obs_spawn.removeEventListener('onSpawn', self._addColisionWith)
    
    def addCollisionWithEnemies(self):
        enemies_alive = self.enemy_spawn.transform.children
        obstacles = self.obs_spawn.transform.children
        
        for enemy in enemies_alive:
            self._addColisionWith(enemy)
        for obs in obstacles:
            self._addColisionWith(obs)
        
        self.enemy_spawn.addEventListener('onSpawn', self._addColisionWith)
        self.obs_spawn.addEventListener('onSpawn', self._addColisionWith)
        
    def addCollisionWithPlayer(self):
        obstacles = self.obs_spawn.transform.children
        
        for obs in obstacles:
            self._addColisionWith(obs)
            
        self._addColisionPerfectWith(Game.player)
        self.obs_spawn.addEventListener('onSpawn', self._addColisionWith)
    
    def _addColisionWith(self, gameObject):
        self.collision.addCollisionWith(gameObject)
        
    def _addColisionPerfectWith(self, gameObject):
        self.collision.addCollisionPerfectWith(gameObject)
        
    def onCollided(self, gameObject):
        from GameObjects.Enemies._Enemy import EnemyBase
        from GameObjects.Player import Player
        
        if(isinstance(gameObject, EnemyBase)):
            self.destroy()
        if(isinstance(gameObject, Player)):
            gameObject.damage()
            self.destroy()