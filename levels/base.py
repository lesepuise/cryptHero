import numpy as np


class BaseLevel():

    def __init__(self, width, height):
        self.map = None
        self.player = None
        self.entities = []
        self.entrance = (1, 1)
        self.exit = (1, 1)
        self.turn = 0
        self.show_colors = True
        self.ui_manager = None
        self.width = None
        self.height = None

        # 0 = triggers
        # 1 = entities
        # 2 = blooded tiles
        self.__buffer = np.empty((width, height, 3), dtype=object, order='F')

    def add_trigger(self, trigger):
        self.__buffer[trigger.x][trigger.y][0] = trigger

    def add_renderer(self, renderer):
        self.renderer = renderer

    def add_entity(self, entity):
        if entity.blocking:
            self.map.block(entity.x, entity.y)
        entity.add_map(self.map)
        entity.add_level(self)
        self.entities.append(entity)
        self.__buffer[entity.x][entity.y][1] = entity

    def blank_entity(self, entity):
        self.__buffer[entity.x][entity.y][1] = None

    def move_entity(self, entity):
        self.__buffer[entity.x][entity.y][1] = entity
    
    def add_player(self, player):
        player.x, player.y = self.entrance
        self.player = player
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
    
    def set_exit(self, x, y):
        self.exit = (x, y)
    
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