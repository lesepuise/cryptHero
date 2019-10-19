import numpy as np

class Structure():
    width = 1
    height = 1
    
    def __init__(self):
        # 0 == walkable
        # 1 == transparent
        self.__buffer = np.zeros((self.width, self.height, 2), dtype=np.bool_, order='F')
        self.chars = np.empty((self.width, self.height), dtype=np.int8, order='F')

    def can_spawn_on(self, map, x, y):
        pass
