#coding=utf-8

from GameObjects.Enemies._Enemy import EnemyBase
from Core.Game import Game
from Core.Vector import Vector2

from Core.Components.KineticsComponent import KineticsComponent
from Core.Components.SpriteComponent import SpriteComponent
from Core.Components.CollisionComponent import CollisionComponent

from random import randint

class Enemy2(EnemyBase):
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
        self.addComponent(SpriteComponent('assets/images/sprites/enemies/enemy_green_2.png'))
        self.addComponent(CollisionComponent())
        
    # Executa no momento em que o inimigo é habilitado em cena
    def _start(self):
        super()._start()
        self.move_speed = Game.SPEED_BASE * .8
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
    
    def configure_spawn(self):
        spawn_offset = 30
        
        vertical_horizontal = randint(0, 1)
        if(vertical_horizontal == 1): # vertical
            top_bottom = -1 * (self.width + spawn_offset)
            
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
            	randint(spawn_offset * -1, Game.WINDOW_HEIGHT / 2 + spawn_offset)
        	))
    
    def _fire(self):
        from GameObjects.GunFire import GunFire
        from Core.Scene.SceneManager import SceneManager
        
        # Irei bolar um tiro no formato |
        # Primeiro, crio os 3 tiros
        shoot = GunFire()
        shoot.setSound('assets/songs/sfx/sfx_laser2.ogg')
        
        
        # É NECESSÁRIO adicioná-los como filha ANTES de alterar as propriedades
        SceneManager.addGameObjectToCurrentScene(shoot)
        
        
        # Fazemos a bala "olhar" para a direção da nave
        angleOffset = 180 # Apenas porque a imagem da bala está invertida
        shoot.transform.vectorRotate(self.direction_vector, angleOffset)
        
        
        # Colocamos elas para nascerem em frente a nave
        shoot.setPosition(
            # Pegamos a posição central do inimigo e somamos com "a direção que olha com metade de seu próprio tamanho"
			self.getPosition() + self.getObjectCenter() + (self.direction_vector * (self.width / 2.3))	
		)
        
        
        # Configuro agora a movimentação dos tiros
        shoot.kinetics.setVelocity(self.direction_vector * shoot.moveSpeedBase * 1.2)
        
        
        # Após todas as configurações, colocamos a bala para colidir com o Player
        shoot.addCollisionWithPlayer()