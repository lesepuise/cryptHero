import tcod
from . import Entity

class Armor(Entity):
    
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = ''
        self.protection = 0


class Cloth(Armor):
    
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Cloth'
        self.protection = 1


class Leather(Armor):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Leather'
        self.protection = 2


class Chain(Armor):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Chain'
        self.protection = 3


class Scale(Armor):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Scale'
        self.protection = 4


class Plate(Armor):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Plate'
        self.protection = 5


class HolyCloth(Armor):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Holy cloth'
        self.protection = 6