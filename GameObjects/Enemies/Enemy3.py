#coding=utf-8

from GameObjects.Enemies._Enemy import EnemyBase
from Core.Game import Game
from Core.Vector import Vector2

from Core.Components.KineticsComponent import KineticsComponent
from Core.Components.SpriteComponent import SpriteComponent
from Core.Components.CollisionComponent import CollisionComponent

from random import randint

class Enemy3(EnemyBase):
    # Construtor. Use APENAS para declarar variáveis
    # Comportamentos iniciais devem ser adicionados no _start
    def __init__(self):
        super().__init__()
        self.lives = 1
        self.score_base = 100
        self._fire_delay = 2
    
        self._reload()
    
    # Executa no momento em que o inimigo é instanciado/criado
    def _awake(self):
        self.addComponent(KineticsComponent())
        self.addComponent(SpriteComponent('assets/images/sprites/enemies/enemy_blue_5.png'))
        self.addComponent(CollisionComponent())
        
    # Executa no momento em que o inimigo é habilitado em cena
    def _start(self):
        super()._start()
        self.move_speed = Game.SPEED_BASE * 3
        # Função do inimigo usado para definir uma posição de spawn.
        # O posicionamento é aleatório e você pode adicionar um fixo, caso queira
        self.configure_spawn()
        
        # Função dos inimigos usado para encarar o player
        self._faceToPlayer()
        # Função dos inimigos usado para andar na direção do player
        self._followPlayer()
    
    # Executa a todo frame
    def _update(self):
        super()._update()
        
    
    # Executa após todo _update
    def _afterUpdated(self):
        super()._afterUpdated()
    
    def _fire(self):
        pass