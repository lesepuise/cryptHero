import random

import numpy as np
import tcod
from tcod.map import compute_fov
from tcod.path import AStar

from . import armors, weapons
from .living import Living


class Monster(Living):
    
    def __init__(self, x=1, y=1, char=ord('g'), color=tcod.light_red):
        super().__init__(x, y, char, color)
        self.blocking = True
    
    def ai(self):
        if not self.dead:
            super().ai()
            fov = compute_fov(self.map.transparent, (self.x, self.y), self.fov, True, tcod.constants.FOV_BASIC)
            player = self.level.get_visible_player(fov)
            if player:
                path = tcod.path_new_using_map(self.map, 0)
                tcod.path_compute(path, self.x, self.y, player.x, player.y)
                if tcod.path_size(path) == 1:
                    self.attack(player)
                elif not tcod.path_is_empty(path):
                    px, py = tcod.path_walk(path, True)
                    self.move(px - self.x, py - self.y)

    
class Kobold(Monster):
    def __init__(self, x=1, y=1, level=1):
        super().__init__(x, y, ord('k'))
        self.name = 'Kobold'
        self.description = 'The mix of a rat and an ugly dog, the Kobold is a small pest.'
        self.fov = 8
        self.hp = 4

        self.weapon = weapons.Dagger()
        self.armor = armors.Cloth()

    
class Goblin(Monster):
    def __init__(self, x=1, y=1, level=1):
        super().__init__(x, y)
        self.name = 'Goblin'
        self.description = 'Disgusting little green creatues that will try to kill you at sight.'
        self.fov = 8
        self.hp = 5

        self.weapon = weapons.Dagger()
        self.armor = armors.Leather()

    
class Orc(Monster):
    def __init__(self, x=1, y=1, level=1):
        super().__init__(x, y, ord('o'))
        self.name = 'Orc'
        self.description = 'A big green brute with bloodied eye, it will not hesitate to evicerate you.'
        self.fov = 8
        self.hp = 6

        self.weapon = weapons.ShortSword()
        self.armor = armors.Leather()

    
class Bugbear(Monster):
    def __init__(self, x=1, y=1, level=1):
        super().__init__(x, y, ord('b'))
        self.name = 'Bugbear'
        self.description = 'Like an ord, big green and brutal, but with more fur, pointier nose and sharp teeth'
        self.fov = 8
        self.hp = 7

        self.weapon = weapons.LongSword()
        self.armor = armors.Leather()

    
class Troll(Monster):
    def __init__(self, x=1, y=1, level=1):
        super().__init__(x, y, ord('T'))
        self.name = 'Troll'
        self.description = 'A huge creature with grey fur and blue eyes. At the moment they saw you, saliva is drooling from its mouth. Its long muscular arms could rip your\'s right off.'
        self.fov = 8
        self.hp = 8

        self.weapon = weapons.Spear()
        self.armor = armors.Leather()


class TutorialGoblin(Goblin):
    def __init__(self, x=1, y=1):
        super().__init__(x, y)
        self.fov = 1
        self.hp = 1
        self.weapon = None
        self.armor = None
        self.can_move = False
    
    def die(self):
        super().die()
        self.level.show_colors = True
        self.level.renderer.flash(tcod.red, self.level.player, self.level.entities, self.level.get_map(), colors=self.level.show_colors)

    
class Daemon(Monster):
    def __init__(self, x=1, y=1, level=1):
        super().__init__(x, y, char=ord('D'), color=tcod.darkest_crimson)
        self.name = 'Daemon'
        self.description = 'An evil creature that rose from the abyss.'
        self.fov = 100
        self.hp = 7 * level

        self.weapon = weapons.Claw()
        self.armor = armors.Chain()
    
    def die(self):
        super().die()
        name = 'Far echoed voice of a young boy'
        dialog = (
            'You have done well Hero,\n\n'
            'The evil is now vanquished, but this world is not yet\n'
            'free. You must leave it and return to the void.\n\n'
            'By doing so it can return to the void, to be born again\n'
            'at an other place and an other time so the player can\n'
            'enjoy it again.\n\n'
            'Thank you.'
        )
        self.level.ended = True
        self.level.ui_manager.show_popup(name, dialog, 'Press r to reset or ESC to quit', centered=False)

