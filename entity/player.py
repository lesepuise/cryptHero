import tcod

from .living import Living
from .monster import Monster
from .npc import NPC

class Player(Living):

    def __init__(self, x=1, y=1, char=ord('@'), color=tcod.white):
        super().__init__(x, y, char, color)

    def move(self, dx, dy):
        if not self.dead:
            target_x = self.x + dx
            target_y = self.y + dy
            super().move(dx, dy)

            target = self.level.get_entity_at(target_x, target_y)
            if isinstance(target, Living):
                if isinstance(target, Monster):
                    self.attack(target)
                if isinstance(target, NPC):
                    target.talk()
