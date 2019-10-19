import numpy as np
import tcod

from entity import Entity
from entity.interactables import Fountain as eFountain


class Structure():
    
    def __init__(self, width: int, height: int, entity: Entity, state=None, chars=None):
        self.width = width
        self.height = height
        self.entity = entity

        # 0 == walkable
        # 1 == transparent
        self.__buffer = state if state is not None else np.zeros((self.width, self.height, 2), dtype=np.bool_, order='F')
        self.chars = chars if chars is not None else np.empty((self.width, self.height), dtype=np.unicode, order='F')

    @property
    def walkable(self):
        return self.__buffer[0]

    @property
    def transparent(self):
        return self.__buffer[1]

    def can_spawn_on(self, map, x, y):
        return not False in map.walkable[x:x+self.width, y:y+self.height]

    def apply_on_map(self, map, x, y):
        map.chars[x:x+self.width, y:y+self.height] = self.chars
        for i in range(x, x+self.width):
            for j in range(y, y+self.height):
                map.set_tile(i, j, map.chars[i][j])
        map.walkable[x:x+self.width, y:y+self.height] = self.walkable
        map.transparent[x:x+self.width, y:y+self.height] = self.transparent
        self.update_entity(x, y)

    
    def update_entity(self, x, y):
        self.entity.x = x
        self.entity.y = y
    
    def get_entity(self):
        return self.entity


class Fountain(Structure):

    def __init__(self):
        walkable = [[True, True, True],
                    [True, False, True],
                    [True, True, True]]

        transparent = [[True, True, True],
                       [True, False, True],
                       [True, True, True]]

        floor = chr(tcod.constants.CHAR_BLOCK1)
        fountain = eFountain.filled_char
        chars = [[floor, floor, floor, ],
                 [floor, fountain, floor, ],
                 [floor, floor, floor, ],]

        entity = eFountain(0, 0)
        super().__init__(3, 3, entity, np.array([walkable, transparent]), chars)
    
    def update_entity(self, x, y):
        self.entity.x = x + 1
        self.entity.y = y + 1
