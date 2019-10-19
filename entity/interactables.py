import tcod

from . import Entity
from .living import Living

class Interactable(Entity):
    
    def __init__(self, x=1, y=1, char=ord('8'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.blocking = True
    
    def interact(self, entity: Entity):
        pass


class Fontain(Interactable):
    
    def __init__(self, x=1, y=1, char=ord('?'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.blocking = True
        self.filled = True
    
    def interact(self, entity: Living):
        entity.healed(entity.max_hp)
