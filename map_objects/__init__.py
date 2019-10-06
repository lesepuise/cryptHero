from tcod.map import Map
import numpy as np


INVISIBLE_TILE = ' '


class DefinedMap(Map):

    def __init__(self, mapfile, order: str = 'F'):
        with open(mapfile) as f:
            self.chars = np.array([list(line) for line in f.read().splitlines()]).transpose()

        super().__init__(len(self.chars), len(self.chars[0]), order)
        self.walkable[:] = (self.chars[:] == ".")

        for c in ('+', '0', 't', '>', '=', chr(25), chr(24)):
            self.walkable[:] = self.walkable[:] | (self.chars == c)

        self.transparent[:] = self.walkable[:]
        for c in ('Ú', 'Ä', 'Â', '¿', '³', 'Ã', 'Å', '´', 'À', 'Á', 'Ù', '~'):
            self.transparent[:] = self.transparent[:] | (self.chars == c)

        self.transparent[:] = self.transparent[:] & (self.chars != '+')
        self.generated = True

    def get_tiles(self):
        for x, columns in enumerate(self.chars):
            for y, char in enumerate(columns):
                if self.fov[x][y]:
                    yield (x, y, ord(char))
                else:
                    yield (x, y, ord(INVISIBLE_TILE))

    def is_visible(self, x, y):
        if x < self.width and y < self.height and x >= 0 and y >= 0:
            return self.fov[x][y]
        else:
            return False
    
    def is_walkable(self, x, y):
        if x < self.width and y < self.height and x >= 0 and y >= 0:
            return self.walkable[x][y]
        else:
            return False

    def block(self, x, y):
        self.walkable[x][y] = False
        self.transparent[x][y] = False

    def unblock(self, x, y):
        self.walkable[x][y] = True
        self.transparent[x][y] = True
