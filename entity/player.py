import tcod

from . import Entity

class Player(Entity):

    def __init__(self, x=1, y=1, char=ord('@'), color=tcod.white):
        super().__init__(x, y, char, color)