import tcod

from . import Entity

class NPC(Entity):
    
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)