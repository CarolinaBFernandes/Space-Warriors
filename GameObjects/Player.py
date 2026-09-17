# coding= utf-8
from Core.GameObject import GameObject
from Core.Game import Game
from Core.Vector import Vector2

from Core.Components.KineticsComponent import KineticsComponent
from Core.Components.SpriteComponent import SpriteComponent
from Core.Components.CollisionComponent import CollisionComponent

from Core.Builders.GameObjectBuilder import GameObjectBuilder

from GameObjects.GunFire import GunFire

class Player(GameObject):
    ''' Classe de GameObject que será controlada pelo jogador '''
    def __init__(self):
        super().__init__()
        self.__sprite_normal = 'assets/images/sprites/player_ship2_blue.png'
        self.__sprite_invulnerable = 'assets/images/sprites/player_ship2_orange.png'
        
        self.addComponent(KineticsComponent())
        self.addComponent(SpriteComponent(self.__sprite_normal))
        #self.addComponent(CollisionComponent())
        
        self.fireReload = 0
        self.lives = 5
        self.isInvulnerable = False

        self.__invulnerabilityTime = 4
        self.__invulnerableTime = 0
        self.__lastFire = 0
        self.__spawn_position = None
        

    def _awake(self):
        self.kinetics = self.getComponent(KineticsComponent)
        self.sprite = self.getComponent(SpriteComponent)
        self.collision = self.getComponent(CollisionComponent)
        
        Game.setPlayer(self)

    def _start(self):
        self.__spawn_position = self.getPosition()
        
        self.move_speed = Game.SPEED_BASE
        self.kinetics.disableGravity()
        
        self.fireReload = .5 / Game.GAME_DIFFICULTY

    def _update(self):
        keyboard = Game.getKeyboard()
        
        # Movimentação
        velocity = Vector2.zero()
        if(keyboard.key_pressed('W') and self.getPosition().y > 0):
            velocity.y = -1
        elif(keyboard.key_pressed('S') and self.getPosition().y < Game.WINDOW_HEIGHT - self.height):
            velocity.y = 1
        
        if(keyboard.key_pressed('A') and self.getPosition().x > 0):
            velocity.x = -1
        elif(keyboard.key_pressed('D') and self.getPosition().x < Game.WINDOW_WIDTH - self.width):
            velocity.x = 1
        
        self.kinetics.setVelocity((velocity.normalize()) * Game.SPEED_BASE)
        # Fim movimento
        
        # Tiro
        self.__lastFire -= Game.DELTA_TIME 
        
        if(keyboard.key_pressed('SPACE') and self.__lastFire < 0):
            self.fire()
        # Fim tiro
        
        if(self.isInvulnerable):
            self.__tickInvulnerability()
        
    def _afterUpdated(self):
        if(not Game.elementOnWindow(self)):
            self.translate(self.kinetics.velocity.normalize() * Game.SPEED_BASE)
            self.kinetics.setVelocity(Vector2.zero())
            
    def fire(self):
        self.__lastFire = self.fireReload
        
        fire = GameObjectBuilder.startBuild(GunFire())\
                .setPosition(self.getPosition() + Vector2(self.width / 2, 0))\
                .build()
        
        fire.setSound('assets/songs/sfx/sfx_laser1.ogg')
        self.addChild(fire)
        fire.addCollisionWithEnemies()
        
    def damage(self):
        if(self.isInvulnerable):
            return
        
        self.lives -= 1
        
        if(self.lives == 0):
            Game.gameOver()
        self.__imortal_mode()

        self._dispatchEvent('onTookDamage', self.lives)
        
    def __imortal_mode(self):
        self.__invulnerableTime = self.__invulnerabilityTime

        self.sprite.changeSprite(self.__sprite_invulnerable)
        self.setPosition(self.__spawn_position)

        self.isInvulnerable = True
    
    def __tickInvulnerability(self):
        self.__invulnerableTime -= Game.DELTA_TIME
        if(self.__invulnerableTime <= 0):
            self.isInvulnerable = False
            self.sprite.changeSprite(self.__sprite_normal)