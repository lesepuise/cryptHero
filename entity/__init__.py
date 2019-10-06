import tcod

class Entity(object):
    """
    A generic object to represent players, enemies, items, etc.
    """

    x = 1
    y = 1
    char = ord('?')
    def __init__(self, x=1, y=1, char=ord('?'), color=tcod.white):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.map = None

    def move(self, dx, dy):
        next_x = self.x + dx
        next_y = self.y + dy

        # Move the entity by a given amount
        if self.map and self.map.is_walkable(next_x, next_y):
            self.x += dx
            self.y += dy

    def add_map(self, level_map):
        self.map = level_map