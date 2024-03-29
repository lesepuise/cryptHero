from __future__ import annotations
import numpy as np
import tcod

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from map_objects import BaseMap
    from entity import Entity
    from entity.player import Player
    from renderer.ui_manager import UIManager


class BaseLevel():

    def __init__(self, width, height):
        self.map:BaseMap = None
        self.player:Player = None
        self.entities:list[Entity] = []
        self.entrance = (1, 1)
        self.exit = (1, 1)
        self.turn = 0
        self.show_colors = True
        self.ui_manager:UIManager = None
        self.width = width
        self.height = height
        self.recalculate_fov = True
        self.ended = False

        # 0 = triggers
        # 1 = entities
        # 2 = blooded tiles
        self.__buffer = np.empty((width, height, 3), dtype=object, order='F')

    def add_trigger(self, trigger):
        self.__buffer[trigger.x][trigger.y][0] = trigger

    def add_renderer(self, renderer):
        self.renderer = renderer

    def add_entity(self, entity:Entity):
        if entity.blocking:
            self.map.block(entity.x, entity.y, entity.transparent)
        entity.add_map(self.map)
        entity.add_level(self)
        self.entities.append(entity)
        self.__buffer[entity.x][entity.y][1] = entity
        entity.target_console.put_char(entity.x, entity.y, entity.char)
        entity.target_console.fg[entity.x][entity.y] = entity.fg
        entity.target_console.bg[entity.x][entity.y] = entity.bg

    def add_decor(self, entity:Entity):
        if entity.blocking:
            self.map.block(entity.x, entity.y, entity.transparent)
        entity.add_map(self.map)
        entity.add_level(self)
        self.map.decor_console.put_char(entity.x, entity.y, entity.char)
        self.map.decor_console.fg[entity.x][entity.y] = entity.fg
        self.map.decor_console.bg[entity.x][entity.y] = entity.bg

    def blank_entity(self, entity:Entity):
        self.__buffer[entity.x][entity.y][1] = None
        entity.target_console.put_char(entity.x, entity.y, ord(' '))
        entity.target_console.fg[entity.x][entity.y] = tcod.white
        entity.target_console.bg[entity.x][entity.y] = tcod.fuchsia

    def move_entity(self, entity:Entity):
        self.__buffer[entity.x][entity.y][1] = entity
        entity.target_console.put_char(entity.x, entity.y, entity.char)
        entity.target_console.fg[entity.x][entity.y] = entity.fg
        entity.target_console.bg[entity.x][entity.y] = entity.bg

    def add_player(self, player:Player):
        player.x, player.y = self.entrance
        self.player = player
        self.player.fov = 10
        self.add_entity(player)

    def get_map(self):
        if not self.map.generated:
            self.map.generate()
        return self.map

    def is_entrance(self, x, y):
        return self.entrance == (x, y)

    def is_exit(self, x, y):
        return self.exit == (x, y)

    def set_entrance(self, x, y):
        self.entrance = (x, y)
        self.map.set_tile(x, y, ord('0'))
        self.map.decor_console.put_char(x, y, ord('0'))
        self.map.decor_console.fg[x][y] = tcod.gray
        self.map.decor_console.bg[x][y] = tcod.black

    def set_exit(self, x, y):
        self.exit = (x, y)
        self.map.set_tile(x, y, 25)
        self.map.decor_console.put_char(x, y, 25)
        self.map.decor_console.fg[x][y] = tcod.gray
        self.map.decor_console.bg[x][y] = tcod.black

    def pass_turn(self, move):
        self.turn += 1
        # Monster and NPC AI
        for entity in self.entities:
            entity.ai()

        # Trig triggers
        for entity in self.entities:
            trigger_tile = self.__buffer[entity.x][entity.y][0]
            if trigger_tile:
                trigger_tile.trigger(self.renderer, entity)

    def add_ui_manager(self, ui_manager):
        self.ui_manager = ui_manager
        # self.ui_manager.add_menu_line(('.', 'Pass time'))
        # self.ui_manager.add_menu_line(('Arrows', 'Move'))
        # self.ui_manager.add_menu_line(('l', 'Look around you'))
        # self.ui_manager.add_menu_line(('t', 'Target to attack'))

    def get_visible_player(self, fov):
        if fov[self.player.x][self.player.y]:
            return self.player
        else:
            return None

    def get_entity_at(self, x, y):
        return self.__buffer[x][y][1]

    def get_tile_at(self, x, y):
        entity = self.get_entity_at(x, y)
        if entity:
            return entity
        return self.map.tiles_at[x][y]