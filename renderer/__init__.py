from datetime import datetime, timedelta
import tcod
from tcod.console import Console

from .ui_manager import UIManager
from map_objects.tile import EMPTY_TILE
from map_objects import BaseMap
from entity.player import Player

class Renderer():

    def __init__(self, root_console:Console, ui_manager:UIManager):
        self.root_console = root_console
        self.flash_console = None
        self.flash_alpha = 1
        self.width = self.root_console.width
        self.height = self.root_console.height
        self.map_dest_coords = (0, 1)
        self.ui_manager = ui_manager
        self.vision_console = Console(60, 60, 'F')

    def render_level(self, player:Player, entities:list, level_map:BaseMap, colors:bool=True, cursor=None, line:bool=False):
        if self.ui_manager.console:
            self.ui_manager.print_ui()
            self.ui_manager.console.blit(self.root_console, 0, 0, 0, 0, 0, 0, key_color=tcod.fuchsia)

        if level_map.terrain_console:
            level_map.terrain_console.blit(
                self.root_console,
                self.map_dest_coords[0],
                self.map_dest_coords[1],
                0, 0, 0, 0,
                key_color=tcod.fuchsia
            )
        if level_map.decor_console:
            level_map.decor_console.blit(
                self.root_console,
                self.map_dest_coords[0],
                self.map_dest_coords[1],
                0, 0, 0, 0,
                key_color=tcod.fuchsia
            )
        if level_map.living_console:
            level_map.living_console.blit(
                self.root_console,
                self.map_dest_coords[0],
                self.map_dest_coords[1],
                0, 0, 0, 0,
                key_color=tcod.fuchsia
            )

        #Set FOV
        self.vision_console.bg[:] = tcod.black
        self.vision_console.bg[level_map.fov] = tcod.fuchsia
        self.vision_console.blit(
            self.root_console,
            self.map_dest_coords[0],
            self.map_dest_coords[1],
            0, 0, 0, 0,
            key_color=tcod.fuchsia
        )

        if not colors:
            self.root_console.fg[:] = tcod.white
            self.root_console.bg[:] = tcod.black
        
        if self.flash_console:
            self.flash_console.blit(self.root_console, 0, 0, 0, 0, self.flash_console.width, self.flash_console.height, self.flash_alpha, self.flash_alpha)
        
        if self.ui_manager.popup:
            self.show_popup(*self.ui_manager.popup)
        tcod.console_flush()
    
    def show_popup(self, title, text, exit_text):
        title_width = self.get_text_width(title)
        text_width = self.get_text_width(text)
        exit_width = self.get_text_width(exit_text)
        min_width = max(title_width, text_width, exit_width)
        min_height = self.get_text_height(text)
        popup_rect = self.calculate_popup_rect(min_width, min_height)
        self.root_console.draw_frame(popup_rect[0] - 2, popup_rect[1] - 2, popup_rect[2] + 4, popup_rect[3] + 4, title, fg=tcod.white, bg=tcod.black)
        self.root_console.print_box(popup_rect[0], popup_rect[1], popup_rect[2], popup_rect[3], text, fg=tcod.white, bg=tcod.black, alignment=tcod.CENTER)
        self.root_console.print_box(popup_rect[0] + popup_rect[2] - exit_width, popup_rect[1] + popup_rect[3] + 1, exit_width, 1, exit_text, fg=tcod.white, bg=tcod.black, alignment=tcod.RIGHT)

    def get_text_width(self, text):
        lines = text.split('\n')
        width = 0
        for line in lines:
            line_width = len(line)
            if line_width > width:
                width = line_width
        return width

    def get_text_height(self, text):
        lines = text.split('\n')
        return len(lines)
    
    def calculate_popup_rect(self, width, height):
        hmid = self.width // 2
        vmid = self.height // 2
        popup_hmid = width // 2
        popup_vmid = height // 2
        return (hmid - popup_hmid, vmid - popup_vmid, width, height)
        
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

