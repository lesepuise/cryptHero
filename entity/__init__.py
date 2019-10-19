import tcod

class Entity(object):
    """
    A generic object to represent players, enemies, items, etc.
    """
    def __init__(self, x=1, y=1, char=ord('?'), color=tcod.white):
        self.x = x
        self.y = y
        self.char = char
        self.fg = color
        self.bg = tcod.black
        self.map = None
        self.level = None
        self.fov = 10
        self.name = ''
        self.description = ''
        self.blocking = False
        self.transparent = False

    def move(self, dx, dy):
        next_x = self.x + dx
        next_y = self.y + dy

        # Move the entity by a given amount
        if self.map and self.map.is_walkable(next_x, next_y):
            self.map.unblock(self.x, self.y)
            self.level.blank_entity(self)
            self.x = next_x
            self.y = next_y
            self.level.move_entity(self)
            if self.blocking:
                self.map.block(self.x, self.y)

    def add_map(self, level_map):
        self.map = level_map

    def add_level(self, level):
        self.level = level
    
    def ai(self):
        pass