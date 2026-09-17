# coding= utf-8
from .PPlay.gameobject import GameObject as GameObjectP
from .Component import Component
from .Vector import Vector2
from .Components.TransformComponent import TransformComponent
from .Components.Abstracts.DrawingComponent import DrawingComponent
from .Components.CollisionComponent import CollisionComponent

# Classe customizada para manipula��o de gameobjects
class GameObject():
    def __init__(self, name = ''):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        
        self.components = []
        
        self.transform = TransformComponent()
        self.addComponent(self.transform)
        
        self.name = name
        self.enabled = True

        self.__awaked = False
        self.__started = False
        
        self._events = { }

    def setName(self, name):
        self.transform.setName(name)

    def getName(self):
        return self.transform.name

    def destroy(self):
        from .Scene.SceneManager import SceneManager
        
        if(self.transform.parent):
            self.transform.parent.removeChild(self)
        else:
            SceneManager.getCurrentScene().removeGameObject(self)
            
        self.disable()
        del self

    def setParent(self, parent):
        self.transform.parent = parent

#------------------------COMPONENTS METHODS-------------------------------
    def addComponent(self, component):
        ''' Adiciona uma nova instância de um Component qualquer ao gameobject '''
        if(isinstance(component, Component)):
            component.setGameObject(self)
            self.components.append(component)
        else:
            raise Exception(f"Instancia da classe {component.__class__} nao pertence ao tipo Component.")

    def getComponent(self, componentType):
        ''' Pega a instância do ComponentType requisitado, caso haja, presente no objeto. Retorna None caso não encontra '''
        for component in self.components:
            if(isinstance(component, componentType)):
                return component
        return None
    
    def getAllComponents(self):
        ''' Pega a instância do ComponentType requisitado, caso haja, presente no objeto. Retorna None caso não encontra '''
        return self.components


#------------------------LIFECICLE METHODS OF GAMEOBJECTS-------------------------------
    def awake(self):
        if(not self.__awaked):
            # Seta a posição inicial igual a posição do pai
            if(self.transform.parent):
                self.transform.setPosition(self.transform.parent.getPosition())
                
            self.__awaked = True
            self._awake()

    def start(self):
        for child in self.transform.children:
            child.start()
            
        if(not self.__started):
            for component in self.components:
                component.start()
            self._start()
            self.__started = True

    def update(self):
        if(self.enabled):
            for component in self.components:
                if(isinstance(component, CollisionComponent) and self.transform.parent):
                    parentCollision = self.transform.parent.gameObject.getComponent(CollisionComponent)
                    if(parentCollision and parentCollision.isColliding()):
                        component.update()
                    else:
                        component.update()
                else:
                    component.update()
                
        for child in self.transform.children:
            if(child != None):
	            child.update()

        self._update()
        self._afterUpdated()
        
    def addChild(self, child):
        self.transform.addChild(child)

    def removeChild(self, child):
        self.transform.removeChild(child)

    def getChildByType(self, childType):
        return self.transform.getChildByType(childType)
    
    def getChildByName(self, childName):
        return self.transform.getChildByName(childName)

    def draw(self):
        if (self.enabled):
            drawingComponent = self.getComponent(DrawingComponent)
            if (drawingComponent):
                drawingComponent.draw()

            for child in self.transform.children:
                child.draw()
                
    def disable(self):
        self.enabled = False
        
    def enable(self):
        self.enabled = True


#------------------------POSITION METHODS-------------------------------
    def setPosition(self, position):
        self.transform.setPosition(position)
        
    def setLocalPosition(self, position):
        if(self.transform.parent):
            self.setPosition(self.transform.parent.getPosition() + position)
        else:
            self.setPosition(position)
        
    def getPosition(self):
        return self.transform.getPosition()

    def translate(self, position):
        ''' Move o objeto, a partir da posição atual, o vetor translate dado '''
        self.transform.translate(position)
    

#------------------------SIZE METHODS-------------------------------
    def getSize(self):
        return Vector2(self.width, self.height)

    def setSize(self, witdh, height):
        self.width = witdh
        self.height = height

    def getObjectCenter(self):
        ''' Obtém o ponto central do objeto '''
        return Vector2(
			self.width / 2,
			self.height / 2
		)

#------------------------LIFECICLE METHODS OF INSTANCES-------------------------------        
    def forceInit(self):
        ''' Usado para iniciar um gameobject que acabou de ser instanciado. Não deve ser utilizado
        no início do jogo pois o awake de todos os gameobjects devem ser executados antes do start'''
        self.awake()
        self.start()
    
    def awaked(self):
        return self.__awaked
    
    def started(self):
        return self.__started
    
    def _awake(self):
        pass

    def _start(self):
        pass

    def _update(self):
        pass
	
    def _afterUpdated(self):
        pass

#-------------------------MOUSE EVENTS-------------------------------
    def onClick(self):
        pass

    def onKeyDown(self):
        pass

    def onKeyPressed(self):
        pass

    def onKeyUp(self):
        pass
    
    def addEventListener(self, key, func):
        if(not key in self._events):
            self._events[key] = []
        self._events[key].append(func)
        
    def removeEventListener(self, key, func):
        if(key in self._events):
            events = self._events.get(key)
            if func in events:
                events.remove(func)
    
    def _dispatchEvent(self, eventName, arg):
        if eventName in self._events:
            for event in self._events[eventName]:
                event(arg)
                
#-------------------------EVENTS-------------------------------
    def onCollided(self, gameObject):
        pass
    
    def copy(self):
        import copy
        
        """ copyobj = self.__class__()
        for name, attr in self.__dict__.items():
            if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
                copyobj.__dict__[name] = attr.copy()
            else:
                copyobj.__dict__[name] = copy.deepcopy(attr)
        return copyobj """
        
        copy_obj = copy.copy(self)
        copy_components = copy_obj.getAllComponents()
        
        for component in copy_components:
            component.gameObject = copy_obj
        
        return copy_obj
    
    def collided(self, obj):
        # Module import
        from Core.PPlay.collision import Collision

        return Collision.collided(self, obj)