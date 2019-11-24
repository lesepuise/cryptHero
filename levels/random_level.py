import numpy as np
import tcod

from .base import BaseLevel
from map_objects import GeneratedMap
from entity import monster
from map_objects.structure import Fountain

import random


__MONSTER_DISTRIBUTION__ =[
    monster.Kobold,
    monster.Kobold,
    monster.Kobold,
    monster.Kobold,
    monster.Goblin,
    monster.Goblin,
    monster.Goblin,
    monster.Goblin,
    monster.Orc,
    monster.Orc,
    monster.Orc,
    monster.Orc,
    monster.Bugbear,
    monster.Bugbear,
    monster.Bugbear,
    monster.Bugbear,
    monster.Troll,
    monster.Troll,
    monster.Troll,
    monster.Troll,
]


class RandomLevel(BaseLevel):
    
    def __init__(self, width, height, level):
        super().__init__(width, height)
        self.level = level
        self.map = GeneratedMap(width, height)
        self.generate_entrance_exit()
        self.generate_monsters()
        self.generate_fountains()

    def generate_entrance_exit(self):

        path = tcod.path_new_using_map(self.map, 0)
        while tcod.path_size(path) == 0:
            sx = random.randint(0, self.width - 1)
            sy = random.randint(0, self.height - 1)
            while not self.map.walkable[sx][sy]:
                sx = random.randint(0, self.width - 1)
                sy = random.randint(0, self.height - 1)

            ex = random.randint(0, self.width - 1)
            ey = random.randint(0, self.height - 1)
            while not self.map.walkable[ex][ey]:
                ex = random.randint(0, self.width - 1)
                ey = random.randint(0, self.height - 1)
            
            tcod.path_compute(path, sx, sy, ex, ey)

        self.set_entrance(sx, sy)
        self.set_exit(ex, ey)
    
    def generate_monsters(self):
        for tile in self.map.get_tiles():
            if self.map.is_walkable(tile.x, tile.y) and random.randint(0, 100) < self.level:
                monster = self.get_monster()
                self.add_entity(monster(tile.x, tile.y, self.level))

    def get_monster(self):
        rng = random.SystemRandom()
        monster_pos = int(((rng.random() - rng.random()) + 1) * self.level * 2.5)
        return __MONSTER_DISTRIBUTION__[monster_pos]
    
    def generate_fountains(self):
        for _ in range(self.level):
            fountain = Fountain()
            sx = random.randint(0, self.width - 1)
            sy = random.randint(0, self.height - 1)
            while not fountain.can_spawn_on(self.map, sx, sy):
                sx = random.randint(0, self.width - 1)
                sy = random.randint(0, self.height - 1)
            fountain.apply_on_map(self.map, sx, sy)
            self.add_entity(fountain.entity)
