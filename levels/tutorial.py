import tcod

from .base import BaseLevel
from map_objects import DefinedMap
from entity.monster import TutorialGoblin
from entity.npc import NPC
from entity.player import Player
from entity.trigger import Trigger

class TutorialLevel(BaseLevel):

    def __init__(self):
        lvl_map = DefinedMap('levels/tutorial.map')
        super().__init__(lvl_map.width, lvl_map.height)
        self.map = lvl_map
        self.show_colors = False
        self.set_entrance(58, 6)
        self.set_exit(2, 8)
        tutorial_goblin = TutorialGoblin(31, 5)
        self.add_entity(tutorial_goblin)
        tutorial_npc = NPC(3, 6)
        self.add_entity(tutorial_npc)

        def exit_altar(renderer, entity):
            self.map.compute_fov(self.player.x, self.player.y, self.player.fov, True, 0)
            renderer.flash(tcod.white, self.player, self.entities, self.get_map(), colors=self.show_colors)
            self.ui_manager.add_menu_line(('l', 'Look around you'))

        self.add_trigger(
            Trigger(49, 6, exit_altar, Player)
        )

    def pass_turn(self, move:tuple):
        super().pass_turn(move)
        if move == (0, 0):
            self.ui_manager.status_line = 'Time as passed...'
        if self.turn == 1:
            self.player.char = ord('.')
        elif self.turn == 2:
            self.player.char = ord(',')
        elif self.turn == 3:
            self.player.char = ord(';')
        elif self.turn == 4:
            self.player.char = ord('o')
        elif self.turn == 5:
            self.player.char = ord('O')
        elif self.turn == 6:
            self.player.char = ord('8')
        elif self.turn == 7:
            self.player.char = ord('a')
        elif self.turn == 8:
            self.player.char = ord('@')
            self.ui_manager.add_menu_line(('Arrows', 'Move'))
            if self.player.fov == 1:
                self.player.fov = 10

    def add_ui_manager(self, ui_manager):
        self.ui_manager = ui_manager
        self.ui_manager.add_menu_line(('.', 'Pass time'))
    
    def add_player(self, player):
        super().add_player(player)
        self.player.fov = 1
        self.player.char = ord(' ')
