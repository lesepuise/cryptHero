import tcod

from . import Entity

class Weapon(Entity):
    
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = ''
        self.action_name = ''
        self.dammage = 1


class Punch(Weapon):
    
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Punch'
        self.action_name = 'punches'


class Dagger(Weapon):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Dagger'
        self.action_name = 'slashes'
        self.dammage = 3


class ShortSword(Weapon):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Shortswrd'
        self.action_name = 'slashes'
        self.dammage = 5


class LongSword(Weapon):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Longsword'
        self.action_name = 'slashes'
        self.dammage = 6


class BroadSword(Weapon):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Broadswrd'
        self.action_name = 'slashes'
        self.dammage = 7


class Spear(Weapon):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Spear'
        self.action_name = 'pierce'
        self.dammage = 7


class Claw(Weapon):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Claw'
        self.action_name = 'claw'
        self.dammage = 5


class Hammer(Weapon):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Hammer'
        self.action_name = 'hit'
        self.dammage = 7


class Axe(Weapon):
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'Btle axe'
        self.action_name = 'slashes'
        self.dammage = 10