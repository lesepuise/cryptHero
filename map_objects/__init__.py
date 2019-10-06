from tcod.map import Map
import numpy as np


INVISIBLE_TILE = ' '


class DefinedMap(Map):

    def __init__(self, mapfile, order: str = 'C'):
        with open(mapfile) as f:
            self.chars = np.array([list(line) for line in f.read().splitlines()])

        super().__init__(len(self.chars[0]), len(self.chars), order)
        self.walkable[:] = (self.chars[:] == ".") | (self.chars == '+') | (self.chars == '0') | (self.chars == 't') | (self.chars == '>')
        self.transparent[:] = self.walkable[:] | (self.chars == '=')
        self.transparent[:] = self.transparent[:] & (self.chars != '+')

    def get_tiles(self):
        for y, columns in enumerate(self.chars):
            for x, char in enumerate(columns):
                if self.fov[y][x]:
                    yield (x, y, ord(char))
                else:
                    yield (x, y, ord(INVISIBLE_TILE))

    def is_walkable(self, x, y):
        return self.walkable[y][x]