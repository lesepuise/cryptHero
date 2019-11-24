import tcod

from . import Entity
from .weapons import Punch
from .armors import Armor
from map_objects import BaseMap

class Living(Entity):
    
    def __init__(self, x=1, y=1, char=ord('!'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.base_hp = 4
        self.max_hp = self.base_hp
        self.hp = 4
        self.dead = False
        self.blocking = True
        self.entity_level = 1
        self.punch = Punch()
        self.naked = Armor()
        self.weapon = None
        self.armor = None
    
    def attack(self, target):
        weapon = self.get_weapon()
        self.level.ui_manager.log('{} {} {}'.format(self.name, weapon.action_name, target.name))
        target.damage(weapon.dammage)
    
    def damage(self, damages):
        armor = self.get_armor()
        dmg = max(damages - armor.protection, 0)
        self.hp -= dmg
        if self.hp <= 0:
            self.die()
    
    def healed(self, points):
        self.hp += points
        if self.hp > self.max_hp:
            self.hp = self.max_hp
    
    def get_weapon(self):
        if self.weapon:
            return self.weapon
        else:
            return self.punch
    
    def get_armor(self):
        if self.armor:
            return self.armor
        else:
            return self.naked

    def die(self):
        self.level.blank_entity(self)
        self.target_console = self.map.decor_console
        self.bg = tcod.crimson
        self.fg = tcod.darkest_sepia
        self.level.add_decor(self)
        self.map.unblock(self.x, self.y)
        self.dead = True
    
    def talk(self):
        pass

    def add_map(self, level_map:BaseMap):
        super().add_map(level_map)
        self.target_console = level_map.living_console