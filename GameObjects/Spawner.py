#coding=UTF-8
from Core.GameObject import GameObject
from Core.Game import Game
from Core.Vector import Vector2
from Core.Scene.SceneManager import SceneManager

from Core.GameStateManager import GameStateManager

class Spawner(GameObject):
    def __init__(self):
        super().__init__()
        self.__pool_size = 3
        self.__pool_enemies = []
        self.__max_pool_difficulty = 10
        
        self.__respawn_delay = 5
        self.__respawn_delay_min = 1
        self.__respawn_ticks = 0
        
        self.__spawner_level = 1
        
        self.__timer = None
        self._is_active = False
    
    def _start(self):
        self.__timer = Game.findGameObjectWithName('timer_hub')
    
    def _update(self):
        if(self._is_active):
	        self._doTick()
    
    def setRespawnDelay(self, delay):
        self.__respawn_delay = delay
    
    def setRespawnDelayMin(self, delay):
        self.__respawn_delay_min = delay
        
    def setPoolSize(self, size):
        self.__pool_size = size
    
    def add(self, enemy):
        if(len(self.__pool_enemies) > 0):
            # Como esse método é chamado pouquíssimas vezes não há problema fazer um método mais custoso como este
            position = [ index for index in range(len(self.__pool_enemies)) if self.__pool_enemies[index].difficulty > enemy.difficulty ]
            if(len(position) > 0):
                self.__pool_enemies.insert(position[0], enemy)
            else:
            	self.__pool_enemies.append(enemy)
        else:
            self.__pool_enemies.append(enemy)
        
        if(enemy.difficulty > self.__max_pool_difficulty):
            self.__max_pool_difficulty = enemy.difficulty
    
    def active(self):
        SceneManager.addGameObjectToCurrentScene(self)
        self._is_active = True
    
    def deactive(self):
        SceneManager.removeGameObjectToCurrentScene(self)
        
        """ 
        while(len(self.__pool_enemies) > 0):
            gameobj = self.__pool_enemies.pop()
            gameobj.disable()
         """
         
        for gameobj in self.transform.children:
            gameobj.destroy()
            
        self._is_active = False
    
    def _doTick(self):
        if not GameStateManager.isGameState(GameStateManager.GAMEPLAY):
            return
        
        self.__respawn_ticks += Game.DELTA_TIME
        if(self.__respawn_ticks >= self.__respawn_delay):
            self.__respawn_ticks = 0
            self.__spawn()
            
            # total - 1
            # 0     - 10
            self.__spawner_level = self.__timer.timer_total // 10 - self.__timer.timer_current // 10
            self.__respawn_delay *= .97
            if self.__respawn_delay < self.__respawn_delay_min:
                self.__respawn_delay = self.__respawn_delay_min            
        
    def __spawn(self):        
        object_to_spawn = self.__choose()
        
        object_to_spawn.setPosition(Vector2(-100, -100))
        
        self.addChild(object_to_spawn)
        self._dispatchEvent('onSpawn', object_to_spawn)
        
    def __choose(self):
        from random import randint
        
        difficulty = randint(0, self.__max_pool_difficulty)
        
        # Esse método é chamado apenas uma vez a cada tick de spawn. Por isso, não terá um impacto tão grande
        # fazer desta forma mais custosa
        index_bigger_aux = [ index for index in range(len(self.__pool_enemies)) if self.__pool_enemies[index].difficulty >= difficulty ]
        index_bigger = len(self.__pool_enemies) - 1
        if(len(index_bigger_aux)):
            index_bigger = index_bigger_aux[0]
        
        previous_enemy = self.__pool_enemies[index_bigger - 1] if index_bigger > 0 else self.__pool_enemies[0]
        next_enemy = self.__pool_enemies[index_bigger]
        
        enemy = None
        # Seleciona o inimigo com a dificuldade mais próxima do número sorteado
        if(difficulty - previous_enemy.difficulty < difficulty - next_enemy.difficulty):
            enemy = previous_enemy
        else:
            enemy = next_enemy
        
        return enemyFactory(type(enemy))
    
def enemyFactory(enemy_type):
    enemy = enemy_type()
    
    return enemy