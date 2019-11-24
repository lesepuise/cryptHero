import numpy as np
import tcod
from tcod.console import Console
from tcod.map import Map

from map_objects.tile import Tile

from .generator import BSPGenerator


class BaseMap(Map):
    chars = []

    def __init__(self, width, height, order: str = 'F'):
        super().__init__(width, height, order)
        self.living_console:Console = None
        self.decor_console:Console = None
        self.terrain_console:Console = None
        self.tiles = []
        self.tiles_at = np.empty((self.width, self.height), dtype=object, order='F')

        for x, columns in enumerate(self.chars):
            for y, char in enumerate(columns):
                tile = Tile(x, y, char)
                self.tiles_at[x][y] = tile
                self.tiles.append(tile)

        self.walkable[:] = (self.chars[:] == ord(' '))

        for c in ('+', chr(197), '0', 't', '>', '=', '"', chr(25), chr(24), chr(250)):
            self.walkable[:] = self.walkable[:] | (self.chars == ord(c))

        self.transparent[:] = self.walkable[:]
        for c in ('Ú', 'Ä', 'Â', '¿', '³', 'Ã', 'Å', '´', 'À', 'Á', 'Ù', '~', chr(176), chr(3), chr(247)):
            self.transparent[:] = self.transparent[:] | (self.chars == ord(c))

        self.transparent[:] = self.transparent[:] & (self.chars != ord('+'))
        self.transparent[:] = self.transparent[:] & (self.chars != chr(197))
        self.generated = True

    def set_tile(self, x, y, char):
        tmp_tile = Tile(x, y, char)
        tile = self.tiles_at[x][y]
        tile.char = tmp_tile.char
        tile.bg = tmp_tile.bg
        tile.fg = tmp_tile.fg
        tile.name = tmp_tile.name
        tile.description = tmp_tile.description
        if chr(char) in (' ', '+', chr(197), '0', 't', '>', '=', '"', chr(25), chr(24), chr(250)):
            self.walkable[x][y] = True
        else:
            self.walkable[x][y] = False
        
        if chr(char) in ('Ú', 'Ä', 'Â', '¿', '³', 'Ã', 'Å', '´', 'À', 'Á', 'Ù', '~', chr(176), chr(3))  or (self.walkable[x][y] and char != '+'):
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

    def block(self, x, y, transparent=False):
        self.walkable[x][y] = False
        self.transparent[x][y] = transparent

    def unblock(self, x, y):
        self.walkable[x][y] = True
        self.transparent[x][y] = True


class DefinedMap(BaseMap):

    def __init__(self, mapfile, order: str = 'F'):
        self.mapfile = mapfile
        consoles = tcod.console_list_load_xp(mapfile)
        self.chars = consoles[0].ch.transpose()
        super().__init__(len(self.chars), len(self.chars[0]), order)
        if len(consoles) > 0:
            self.terrain_console = consoles[0]
            self.terrain_console._order = order
        if len(consoles) > 1:
            self.decor_console = consoles[1]
            self.decor_console._order = order
        if len(consoles) > 2:
            self.living_console = consoles[2]
            self.living_console._order = order

class GeneratedMap(BaseMap):
    def __init__(self, width, height, order: str = 'F'):

        gen = BSPGenerator(width, height)
        self.mask = gen.get_map()
        self.chars = np.empty((width, height) ,dtype='int', order='F')
        self.chars.fill(ord('#'))
        self.chars[self.mask] = 250
        super().__init__(width, height, order)
        self.terrain_console = Console(width, height, order=order)
        self.terrain_console.ch[:] = self.chars[:]
        self.terrain_console.fg[:] = tcod.dark_gray
        self.terrain_console.bg[:] = tcod.gray
        self.terrain_console.fg[self.mask] = tcod.darkest_grey
        self.terrain_console.bg[self.mask] = tcod.black
        self.decor_console = Console(width, height, order=order)
        self.decor_console.fg[:] = tcod.gray
        self.decor_console.bg[:] = tcod.fuchsia
        self.living_console = Console(width, height, order=order)
        self.living_console.fg[:] = tcod.gray
        self.living_console.bg[:] = tcod.fuchsia

class Debug(BaseMap):
    def __init__(self, order: str = 'F'):

        def to_char(v):
            return chr(v)

        ords = np.arange(0, 256)
        chars = np.vectorize(to_char)(ords)
        chars = np.reshape(chars, (16, 16), order='F')
        chars[0][0] = ' '
        self.chars = chars

        super().__init__(16, 16, order)
        self.walkable[:] = True
        self.transparent[:] = True

    def set_tile(self, x, y, char):
        tmp_tile = Tile(x, y, char)
        tile = self.tiles_at[x][y]
        tile.char = tmp_tile.char
        tile.bg = tmp_tile.bg
        tile.fg = tmp_tile.fg
        self.walkable[x][y] = True
        self.transparent[x][y] = True
