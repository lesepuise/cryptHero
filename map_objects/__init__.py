from tcod.map import Map
import numpy as np

from map_objects.tile import Tile

from .generator import BSPGenerator

class BaseMap(Map):
    chars = []

    def __init__(self, width, height, order: str = 'F'):
        super().__init__(width, height, order)
        self.tiles = []
        self.tiles_at = np.empty((self.width, self.height), dtype=object, order='F')

        for x, columns in enumerate(self.chars):
            for y, char in enumerate(columns):
                tile = Tile(x, y, char)
                self.tiles_at[x][y] = tile
                self.tiles.append(tile)

        self.walkable[:] = (self.chars[:] == ' ')

        for c in ('+', '0', 't', '>', '=', '"', chr(25), chr(24)):
            self.walkable[:] = self.walkable[:] | (self.chars == c)

        self.transparent[:] = self.walkable[:]
        for c in ('Ú', 'Ä', 'Â', '¿', '³', 'Ã', 'Å', '´', 'À', 'Á', 'Ù', '~'):
            self.transparent[:] = self.transparent[:] | (self.chars == c)

        self.transparent[:] = self.transparent[:] & (self.chars != '+')
        self.generated = True

    def set_tile(self, x, y, char):
        tmp_tile = Tile(x, y, char)
        tile = self.tiles_at[x][y]
        tile.char = tmp_tile.char
        tile.bg = tmp_tile.bg
        tile.fg = tmp_tile.fg
        if char in (' ', '+', '0', 't', '>', '=', '"', chr(25), chr(24)):
            self.walkable[x][y] = True
        else:
            self.walkable[x][y] = False
        
        if char in ('Ú', 'Ä', 'Â', '¿', '³', 'Ã', 'Å', '´', 'À', 'Á', 'Ù', '~')  or (self.walkable[x][y] and char != '+'):
            self.transparent[x][y] = True
        else:
            self.transparent[x][y] = False

    def get_tiles(self):
        for tile in self.tiles:
            if self.fov[tile.x][tile.y]:
                yield tile
            else:
                yield Tile(tile.x, tile.y)

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


class DefinedMap(BaseMap):

    def __init__(self, mapfile, order: str = 'F'):
        self.mapfile = mapfile
        with open(mapfile) as f:
            self.chars = np.array([list(line) for line in f.read().splitlines()]).transpose()
        super().__init__(len(self.chars), len(self.chars[0]), order)

class GeneratedMap(BaseMap):
    def __init__(self, width, height, order: str = 'F'):

        gen = BSPGenerator(width, height)
        self.mask = gen.get_map()
        self.chars = np.empty((width, height) ,dtype=object, order='F')
        self.chars.fill('#')
        self.chars[self.mask] = ' '

        super().__init__(width, height, order)