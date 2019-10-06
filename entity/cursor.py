import tcod

from . import Entity

class Cursor(Entity):
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x=1, y=1, char=ord('?'), color=tcod.white):
        self.x = x
        self.y = y
        self.char = char
        self.color = color

    def move(self, dx, dy):
        next_x = self.x + dx
        next_y = self.y + dy

        # Move the entity by a given amount
        if self.map and self.map.is_visible(next_x, next_y):
            self.x = next_x
            self.y = next_y