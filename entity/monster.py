import tcod

from . import Entity

class Monster(Entity):
    
    def __init__(self, x=1, y=1, char=ord('g'), color=tcod.red):
        super().__init__(x, y, char, color)