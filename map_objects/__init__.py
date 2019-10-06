from tcod.map import Map
import numpy as np


INVISIBLE_TILE = ' '


class DefinedMap(Map):

    def __init__(self, mapfile, order: str = 'F'):
        with open(mapfile) as f:
            self.chars = np.array([list(line) for line in f.read().splitlines()]).transpose()

        super().__init__(len(self.chars), len(self.chars[0]), order)
        self.walkable[:] = (self.chars[:] == ".") | (self.chars == '+') | (self.chars == '0') | (self.chars == 't') | (self.chars == '>')
        self.transparent[:] = self.walkable[:] | (self.chars == '=')
        self.transparent[:] = self.transparent[:] & (self.chars != '+')
        self.generated = True

    def get_tiles(self):
        for x, columns in enumerate(self.chars):
            for y, char in enumerate(columns):
                if self.fov[x][y]:
                    yield (x, y, ord(char))
                else:
                    yield (x, y, ord(INVISIBLE_TILE))

    def is_walkable(self, x, y):
        return self.walkable[x][y]