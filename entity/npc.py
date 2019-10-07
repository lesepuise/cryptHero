import tcod

from .living import Living

class NPC(Living):
    
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)