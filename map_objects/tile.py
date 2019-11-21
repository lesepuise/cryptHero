
from .identifier import identify

EMPTY_TILE = ord(' ')


class Tile():
    def __init__(self, x, y, char=ord(' ')):
        self.x = x
        self.y = y
        self.char = char
        self.name, self.description, self.fg, self.bg = identify(char)
