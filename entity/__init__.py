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

    def move(self, dx, dy):
        # Move the entity by a given amount
        self.x += dx
        self.y += dy

