import tcod

from map_objects.tile import EMPTY_TILE

class Renderer():

    def __init__(self, root_console, map_console, menu_console, action_console):
        self.root_console = root_console
        self.map_console = map_console
        self.menu_console = menu_console
        self.action_console = action_console
        self.width = self.root_console.width
        self.height = self.root_console.height
        self.map_dest_coords = (0, 0)
        self.menu_dest_coords = (self.map_console.width + 1, 0)
        self.action_dest_coords = (0, self.map_console.height + 1)

    def render_level(self, player, entities, level_map, colors=True, cursor=None, line=False):
        for tile in level_map.get_tiles():
            self.map_console.put_char(tile[0], tile[1], tile[2], tcod.BKGND_NONE)
        
        self.map_console.fg[:] = tcod.white

        for entity in entities:
            if  level_map.fov[entity.x][entity.y]:
                if colors:
                    self.map_console.fg[entity.x][entity.y] = entity.color
                else:
                    self.map_console.bf[:] = tcod.black

                self.map_console.put_char(entity.x, entity.y, entity.char, tcod.BKGND_NONE)
        
        if cursor:
            if colors:
                self.map_console.fg[cursor.x][cursor.y] = cursor.color

            self.map_console.put_char(cursor.x, cursor.y, cursor.char, tcod.BKGND_NONE)
        
        self.map_console.blit(self.root_console, 0, 0, self.map_dest_coords[0], self.map_dest_coords[1], self.map_console.width, self.map_console.height)
        tcod.console_flush()

        for entity in entities:
            self.map_console.put_char(entity.x, entity.y, EMPTY_TILE, tcod.BKGND_NONE)
        
        if cursor:
            self.map_console.put_char(cursor.x, cursor.y, EMPTY_TILE, tcod.BKGND_NONE)
        
    def render_fov(self, fov_map, x, y, radius, light_walls=True, algorithm=0):
        tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)
