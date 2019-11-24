import tcod

from .living import Living
from .monster import Monster
from .interactables import Interactable
from .npc import NPC
from . import weapons
from . import armors


class Player(Living):

    def __init__(self, x=1, y=1, char=ord('@'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.base_hp = 8
        self.name = 'You'
        self.description = (
            'This is your body, freshly born from the void\n'
            'in a world created for you.'
        )
        self.blocking = False
        self.entity_level = 0
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
            if isinstance(target, Interactable):
                target.interact(self)
    
    def xp(self):
        self.kills += 1
        if self.kills > self.entity_level * 3:
            self.kills = 0
            self.entity_level += 1
            self.max_hp += self.base_hp
            self.hp = self.max_hp
            if not self.weapon:
                self.weapon = weapons.BroadSword()
                self.armor = armors.Cloth()
    
    def attack(self, target):
        super().attack(target)
        if target.dead:
            self.xp()
    
    def is_on_exit(self):
        return (self.x, self.y) == self.level.exit
    
    def activate_god_mod(self):
        self.weapon = weapons.Axe()
        self.armor = armors.HolyCloth()

    def die(self):
        self.level.blank_entity(self)
        self.target_console = self.map.decor_console
        self.bg = tcod.crimson
        self.fg = tcod.darkest_sepia
        self.level.add_decor(self)
        self.map.unblock(self.x, self.y)
        self.dead = True
        self.level.ui_manager.log('You died.')
