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
        self.dialog = ''
        self.can_move = True
    
    def attack(self, target):
        weapon = self.get_weapon()
        target.damage(self, weapon)
    
    def damage(self, source, weapon):
        armor = self.get_armor()
        dmg = max(weapon.dammage - armor.protection, 0)
        self.level.ui_manager.log(
            '{} {} {}, dealing {} damages'.format(
                source.name, weapon.action_name, self.name, dmg
            )
        )
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
        self.level.ui_manager.log(
            'The {} dies'.format(
                self.name
            )
        )
    
    def talk(self):
        self.level.ui_manager.show_popup(self.name, self.dialog, 'ESC to close', False)

    def add_map(self, level_map:BaseMap):
        super().add_map(level_map)
        self.target_console = level_map.living_console