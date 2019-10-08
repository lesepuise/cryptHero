import tcod

from .living import Living
from .monster import Monster
from .npc import NPC
from .weapons import BroadSword
from .armors import Chain


class Player(Living):

    def __init__(self, x=1, y=1, char=ord('@'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.name = 'You'
        self.description = (
            'This is your body, freshly born from the void\n'
            'in a world created for you.'
        )
        self.blocking = False
        self.player_level = 0
        self.kills = 0


    def move(self, dx, dy):
        if not self.dead:
            target_x = self.x + dx
            target_y = self.y + dy
            super().move(dx, dy)

            target = self.level.get_entity_at(target_x, target_y)
            if isinstance(target, Living) and not target.dead:
                if isinstance(target, Monster):
                    self.attack(target)
                if isinstance(target, NPC):
                    target.talk()
    
    def xp(self):
        self.kills += 1
        if self.kills > self.player_level * 3:
            self.max_hp += self.max_hp
            self.hp = self.max_hp
            self.weapon = BroadSword()
            self.armor = Chain()
    
    def attack(self, target):
        super().attack(target)
        if target.dead:
            self.xp()
    
    def is_on_exit(self):
        return (self.x, self.y) == self.level.exit
