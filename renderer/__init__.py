import tcod

from map_objects.tile import EMPTY_TILE

class Renderer():

    def __init__(self, root_console):
        self.root_console = root_console

    def render_level(self, con, entities, level_map, width, height):
        for tile in level_map.get_tiles():
            con.put_char(tile[0], tile[1], tile[2], tcod.BKGND_NONE)
        
        con.fg[:] = tcod.white
        for entity in entities:
            con.put_char(entity.x, entity.y, entity.char, tcod.BKGND_NONE)
        
        con.blit(self.root_console, 0, 0, 0, 0, width, height)
        tcod.console_flush()

        for entity in entities:
            con.put_char(entity.x, entity.y, EMPTY_TILE, tcod.BKGND_NONE)
    
    def render_fov(self, fov_map, x, y, radius, light_walls=True, algorithm=0):
        tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)