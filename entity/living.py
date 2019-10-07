import tcod

from . import Entity

class Living(Entity):
    
    def __init__(self, x=1, y=1, char=ord('!'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.max_hp = 4
        self.hp = 4
        self.dead = False
    
    def attack(self, target):
        self.level.ui_manager.status_line = '{} punch {}'.format(self.name, target.name)
        target.damage(1)
    
    def damage(self, damages):
        self.hp -= damages
        if self.hp <= 0:
            self.die()
    
    def healed(self, points):
        self.hp += points
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def die(self):
        self.bg = tcod.crimson
        self.fg = tcod.darkest_sepia
        self.map.unblock(self.x, self.y)
        self.dead = True
    
    def talk(self):
        pass