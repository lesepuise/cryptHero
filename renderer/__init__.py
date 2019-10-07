from datetime import datetime, timedelta
import tcod
from tcod.console import Console

from .ui_manager import UIManager
from map_objects.tile import EMPTY_TILE

class Renderer():

    def __init__(self, root_console:Console, map_console:Console, menu_console:Console, action_console:Console, ui_manager:UIManager):
        self.root_console = root_console
        self.map_console = map_console
        self.menu_console = menu_console
        self.action_console = action_console
        self.flash_console = None
        self.flash_alpha = 1
        self.width = self.root_console.width
        self.height = self.root_console.height
        self.map_dest_coords = (0, 0)
        self.menu_dest_coords = (self.map_console.width, 0)
        self.action_dest_coords = (0, self.map_console.height)
        self.ui_manager = ui_manager

    def render_level(self, player, entities, level_map, colors=True, cursor=None, line=False):
        # Draw map
        for tile in level_map.get_tiles():
            self.map_console.put_char(tile.x, tile.y, tile.char, tcod.BKGND_NONE)
            if colors:
                self.map_console.fg[tile.x][tile.y] = tile.fg
                self.map_console.bg[tile.x][tile.y] = tile.bg
            else:
                self.map_console.fg[:] = tcod.white
                self.map_console.bg[:] = tcod.black

        for entity in entities:
            if  level_map.fov[entity.x][entity.y]:
                self.map_console.put_char(entity.x, entity.y, entity.char, tcod.BKGND_NONE)
                if colors:
                    self.map_console.fg[entity.x][entity.y] = entity.fg
                    self.map_console.bg[entity.x][entity.y] = entity.bg

        if cursor:
            self.map_console.put_char(cursor.x, cursor.y, cursor.char, tcod.BKGND_NONE)
            if colors:
                self.map_console.fg[cursor.x][cursor.y] = cursor.color

        self.map_console.blit(self.root_console, self.map_dest_coords[0], self.map_dest_coords[1], 0, 0, self.map_console.width, self.map_console.height)
        
        self.render_menu()
        self.render_actions()

        if self.flash_console:
            self.flash_console.blit(self.root_console, 0, 0, 0, 0, self.flash_console.width, self.flash_console.height, self.flash_alpha, self.flash_alpha)
        
        if player.dead:
            self.root_console.draw_frame(20, 10, self.root_console.width - 40, self.root_console.height - 20, 'You are dead.', fg=tcod.crimson, bg=tcod.black)
            self.root_console.print_box(21, 11, self.root_console.width - 42, self.root_console.height - 22, 'You are dead.', fg=tcod.crimson, bg=tcod.black, alignment=tcod.CENTER)
        tcod.console_flush()

        for entity in entities:
            self.map_console.put_char(entity.x, entity.y, EMPTY_TILE, tcod.BKGND_NONE)
        
        if cursor:
            self.map_console.put_char(cursor.x, cursor.y, EMPTY_TILE, tcod.BKGND_NONE)

    def render_fov(self, fov_map, x, y, radius, light_walls=True, algorithm=0):
        tcod.map_compute_fov(fov_map, x, y, radius, light_walls, algorithm)

    def render_menu(self):
        # Draw borders
        h_repeat = self.menu_console.width - 2
        v_repeat = self.menu_console.height - 2
        self.menu_console.print(0, 0, 'Ú{}¿'.format('Ä' * h_repeat), tcod.white)
        for i in range(v_repeat):
            self.menu_console.print(0, i+1, '³{}³'.format(' ' * h_repeat), tcod.white)
        self.menu_console.print(0, 79, 'À{}Ù'.format('Ä' * h_repeat), tcod.white)

        # Draw menu text
        self.menu_console.print(1, 0, self.ui_manager.menu_title, tcod.white)
        line_idx = 1
        for line in self.ui_manager.menu_lines:
            self.menu_console.print(2, line_idx, line[0], tcod.yellow)
            self.menu_console.print(len(line[0]) + 2, line_idx, ':', tcod.grey)
            self.menu_console.print(len(line[0]) + 4, line_idx, line[1], tcod.white)
            line_idx += 1
        self.menu_console.blit(self.root_console, self.menu_dest_coords[0], self.menu_dest_coords[1], 0, 0, self.menu_console.width, self.menu_console.height)


    def render_actions(self, text='TOTO'):
        # Draw borders
        h_repeat = self.action_console.width - 2
        v_repeat = self.action_console.height - 2
        self.action_console.print(0, 0, 'Ú{}´'.format('Ä' * h_repeat), tcod.white)
        for i in range(v_repeat):
            self.action_console.print(0, i+1, '³{}³'.format(' ' * h_repeat), tcod.white)
        self.action_console.print(0, v_repeat + 1, 'À{}Á'.format('Ä' * h_repeat), tcod.white)

        # Print actions
        self.action_console.print(1, 0, text, tcod.white)
        self.action_console.print(10, self.action_console.height - 1, self.ui_manager.status_line, tcod.pink)
        self.action_console.blit(self.root_console, self.action_dest_coords[0], self.action_dest_coords[1], 0, 0, self.action_console.width, self.action_console.height)

    def flash(self, color, player, entities, level_map, colors=True, cursor=None, line=False, delay=2):
        self.flash_console = Console(self.root_console.width, self.root_console.height, 'F')
        delta = timedelta(seconds=delay)
        start = datetime.now()
        diff = timedelta(seconds=0)
        while diff < delta:
            self.flash_alpha = 1 - (((diff.seconds * 1000000) + diff.microseconds) / (delay * 1000000))
            self.flash_console.draw_rect(0, 0, self.flash_console.width, self.flash_console.height, ord(' '), color, color)
            diff = datetime.now() - start
            self.render_level(player, entities, level_map, colors=colors, cursor=cursor, line=line)
        self.flash_console = None
        self.flash_alpha = 1

