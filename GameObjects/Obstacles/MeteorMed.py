# coding= utf-8
import math

from Core.GameObject import GameObject
from Core.Game import Game
from Core.Vector import Vector2

from Core.Components.KineticsComponent import KineticsComponent
from Core.Components.SpriteComponent import SpriteComponent
from Core.Components.CollisionComponent import CollisionComponent

from random import randint

class MeteorMed(GameObject):
    ''' Classe de gameobject que representará um inimigo genérico '''
    def __init__(self):
        super().__init__()
        self.difficulty = 1 # Dificuldade do inimigo. Usado para definir sua frequência de spawn
        self.move_speed = None # Setado durante o Start
        self.__can_destroy = False

    def _awake(self):
        self.addComponent(KineticsComponent())
        self.addComponent(SpriteComponent('assets/images/sprites/meteors/meteor_brown_med1.png'))
        self.addComponent(CollisionComponent())

    def _start(self):
        self.kinetics = self.getComponent(KineticsComponent)
        self.sprite = self.getComponent(SpriteComponent)
        self.collision = self.getComponent(CollisionComponent)
        
        self.move_speed = Game.SPEED_BASE / 1.6
        self.kinetics.disableGravity()
        
        self.collision.addCollisionWith(Game.player)
        self.configure_spawn()

    def _update(self):
        # Destroy o objeto apenas após ele entrar e sair da tela
        if(Game.elementOnWindow(self)):
            self.__can_destroy = True
        elif(self.__can_destroy):
            self.destroy()
        
    def configure_spawn(self, horizontal_offset = 0, vertical_offset = 0):        
        spawn_offset = 30
        
        vertical_horizontal = randint(0, 1)
        if(vertical_horizontal == 1): # vertical
            top_bottom = randint(0, 1)
            top_bottom = Game.WINDOW_HEIGHT * top_bottom
            top_bottom = -1 * (self.width + spawn_offset) if top_bottom == 0 else top_bottom + spawn_offset
            
            self.setPosition(Vector2(
            	randint(spawn_offset * -1, Game.WINDOW_WIDTH + spawn_offset),
            	top_bottom
        	))
        else: # Horizontal
            left_right = randint(0, 1)
            left_right = Game.WINDOW_WIDTH * left_right
            left_right = -1 * (self.width + spawn_offset) if left_right == 0 else left_right + spawn_offset
            
            self.setPosition(Vector2(
            	left_right,
            	randint(spawn_offset * -1, Game.WINDOW_HEIGHT + spawn_offset)
        	))
        
        self.__moveTo()
    
    def __moveTo(self):
        direction_vector = Game.getWindowCenter() - self.getPosition()
        direction_vector = direction_vector.normalize()
        vetor_ruido = Vector2(randint(-0, 10), randint(0, 10)) / 100
        direction_vector = (direction_vector + vetor_ruido).normalize()
        
        self.kinetics.setVelocity(direction_vector * self.move_speed)
    
    # Função executada quando ocorre uma colisão com o player
    def onCollided(self, gameObject):
        from GameObjects.Player import Player
        from GameObjects.GunFire import GunFire
        
        if(isinstance(gameObject, Player)):
            Game.player.damage()
        elif(isinstance(gameObject, GunFire)):
            gameObject.destroy()