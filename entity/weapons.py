import tcod

from . import Entity

class Weapon(Entity):
    
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.action_name = ''


class Punch(Weapon):
    
    def __init__(self, x=1, y=1, char=ord('U'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.action_name = 'punches'


class Dagger(Weapon):
    pass


class ShortSword(Weapon):
    pass


class LongSword(Weapon):
    pass


class BroadSword(Weapon):
    pass


class Spear(Weapon):
    pass


class Claw(Weapon):
    pass


class Hammer(Weapon):
    pass


class Axe(Weapon):
    pass