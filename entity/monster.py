import numpy as np
import tcod
from tcod.map import compute_fov
from tcod.path import AStar


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

    
class Goblin(Monster):
    def __init__(self, x=1, y=1):
        super().__init__(x, y)
        self.name = 'Goblin'
        self.description = 'Disgusting little green creatues that will try to kill you at sight.'
        self.fov = 7


class TutorialGoblin(Goblin):
    def __init__(self, x=1, y=1):
        super().__init__(x, y)
        self.fov = 1
        self.hp = 1
    
    def die(self):
        super().die()
        self.level.show_colors = True
        self.level.renderer.flash(tcod.red, self.level.player, self.level.entities, self.level.get_map(), colors=self.level.show_colors)