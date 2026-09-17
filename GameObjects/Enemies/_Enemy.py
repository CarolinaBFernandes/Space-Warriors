# coding= utf-8
import math

from Core.GameObject import GameObject
from Core.Game import Game
from Core.Vector import Vector2

from Core.Components.KineticsComponent import KineticsComponent
from Core.Components.SpriteComponent import SpriteComponent
from Core.Components.CollisionComponent import CollisionComponent


class EnemyBase(GameObject):
    ''' Classe de gameobject que representará um inimigo genérico '''
    def __init__(self):
        super().__init__()
        self.difficulty = 1 # Dificuldade do inimigo. Usado para definir sua frequência de spawn
        self.move_speed = None # Setado durante o Start
        self.score_base = 100
        self.lives = 1
        self.direction_vector = None
        self._fire_delay = 2
        self._reload_time = 0        

    def _awake(self):
        self.addComponent(KineticsComponent())
        self.addComponent(SpriteComponent('assets/images/sprites/enemies/enemy_black_1.png'))
        self.addComponent(CollisionComponent())

    def _start(self):
        self.kinetics = self.getComponent(KineticsComponent)
        self.sprite = self.getComponent(SpriteComponent)
        self.collision = self.getComponent(CollisionComponent)
        
        self.move_speed = Game.SPEED_BASE
        self.kinetics.disableGravity()
        
        self.collision.addCollisionPerfectWith(Game.player)

    def _update(self):
        if(self.y > Game.WINDOW_HEIGHT + self.height):
            self.destroy()
        
        if(self._reload_time <= 0):
            self._fire()
            self._reload()
        
    def _afterUpdated(self):
        self._reload_time -= Game.DELTA_TIME
        
    def configure_spawn(self, horizontal_offset = 0, vertical_offset = 0):
        from random import randint

        self.setPosition(Vector2(
            randint(horizontal_offset * -1, Game.WINDOW_WIDTH + horizontal_offset),
            (self.height + vertical_offset) * -1
        ))
        
    def _fire(self):
        pass
    
    def _reload(self):
        from random import randint
        
        percentage = int(self._fire_delay * 0.7)
        self._reload_time = self._fire_delay + randint(-percentage, int(percentage / 2))
    
    def _faceToPlayer(self):
        from random import randint
        
        ''' Vira a rotação do gameobject em direção ao player '''
        playerPosition = Game.player.getPosition()
        position = self.getPosition()
        vector_distance = playerPosition - position
        
        self.direction_vector = vector_distance.normalize()
        vetor_ruido = Vector2(randint(0, 20), randint(0, 20)) / 100
        
        self.direction_vector = (self.direction_vector + vetor_ruido).normalize()

        angle = 0
        if(self.direction_vector.x == 0):
            pass
        else:
            angle = math.atan(self.direction_vector.x/self.direction_vector.y)
            angle = angle * (180/math.pi)
        self.transform.rotate(angle)
        
    def _followPlayer(self):                        
        self.kinetics.setVelocity(self.direction_vector * self.move_speed / 2)
        
    def _tookDamage(self):
        Game.score += self.score_base
        self.lives -= 1
        
        if(self.lives <= 0):
            self.destroy()
        
    # Função executada quando ocorre uma colisão com o player
    def onCollided(self, gameObject):
        from GameObjects.Player import Player
        from GameObjects.GunFire import GunFire
        
        if(isinstance(gameObject, Player)):
            Game.player.damage()
        elif(isinstance(gameObject, GunFire)):
            # Diminui em 1 a vida do inimigo e mata caso a vida zere
            self._tookDamage()