import numpy as np
from .final import FinalLevel
from .random_level import RandomLevel
from .tutorial import TutorialLevel


levels = [
    TutorialLevel(),
    RandomLevel(),
    RandomLevel(),
    RandomLevel(),
    FinalLevel(),
]


class BaseLevel():

    def __init__(self, width, height):
        self.map = None
        self.player = None
        self.entities = []
        self.entrance = (1, 1)
        self.exit = (1, 1)

        # 0 = triggers
        # 1 = entities
        self.__buffer = np.empty((height, width, 2), dtype=object)

    def add_trigger(self, trigger):
        trigger.add_map(self.map)
        self.__buffer[trigger.x][trigger.y][0] = trigger

    def add_entity(self, entity):
        entity.add_map(self.map)
        self.entities.append(entity)
        self.__buffer[entity.x][entity.y][1] = entity
    
    def add_player(self, player):
        self.player = player
        self.add_entity(player)

    def get_map(self):
        if not self.map.generated:
            self.map.generate()
        return self.map
    
    def is_entrance(self, x, y):
        return self.entrance == (x, y)
    
    def is_exit(self, x, y):
        return self.exit == (x, y)
    
    def set_entrance(self, x, y):
        self.entrance = (x, y)
    
    def set_exit(self, x, y):
        self.exit = (x, y)