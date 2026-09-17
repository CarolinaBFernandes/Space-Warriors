# coding= utf-8

class GameObjectBuilder():

    instance = None

    @classmethod
    def startBuild(cls, gameObject):
        cls.instance = gameObject
        return cls

    @classmethod
    def addComponent(cls, component):
        cls.instance.addComponent(component)
        return cls

    @classmethod
    def setPosition(cls, position):
        cls.instance.setPosition(position)
        return cls

    @classmethod
    def setName(cls, name):
        cls.instance.setName(name)
        return cls

    @classmethod
    def build(cls):
        cls.instance.awake()
        return cls.instance