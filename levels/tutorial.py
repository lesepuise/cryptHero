import tcod

from .base import BaseLevel
from map_objects import DefinedMap
from entity.monster import TutorialGoblin
from entity.npc import NPC
from entity.player import Player
from entity.trigger import Trigger
from map_objects.structure import Fountain

class TutorialLevel(BaseLevel):

    def __init__(self):
        lvl_map = DefinedMap('levels/tutorial.xp')
        super().__init__(lvl_map.width, lvl_map.height)
        self.map = lvl_map
        self.show_colors = False
        self.set_entrance(52, 30)
        self.set_exit(8, 34)
        tutorial_goblin = TutorialGoblin(23, 29)
        self.add_entity(tutorial_goblin)
        self.map.fov[:] = False
        self.map.fov[52][30] = True
        self.recalculate_fov = False
        tutorial_npc = NPC(8, 30)
        tutorial_npc.name = 'Young boy'
        tutorial_npc.dialog = (
            'Welcome, Hero.\nThis world is for you and you are for this world.\n\n'
            'Take that sword and make your way down the crypt as it is your\n'
            'destiny to traverse it. But beware, those walls are infested with\n'
            'monsters.\n\n'
            'At the end of the crypt you’ll find the passage to the lair of an\n'
            'evil that was created for you. Beat him and wait for the world to\n'
            'be released from you and into the void once again.'
        )
        self.add_entity(tutorial_npc)

        def exit_altar(renderer, entity):
            self.map.compute_fov(self.player.x, self.player.y, self.player.fov, True, 0)
            renderer.flash(tcod.white, self.player, self.entities, self.get_map(), colors=self.show_colors)
            self.ui_manager.add_menu_line(('l', 'Look around you'))
            self.recalculate_fov = True
        
        self.add_trigger(
            Trigger(46, 30, exit_altar, Player)
        )

        def get_hit(renderer, entity):
            self.ui_manager.add_menu_line(('Arrows', 'Attack'))

        self.add_trigger(
            Trigger(24, 29, get_hit, Player)
        )

        def npc_talk(renderer, entity):
            tutorial_npc.talk()

        self.add_trigger(
            Trigger(14, 30, npc_talk, Player)
        )

        def show_credits(renderer, entity):
            self.ui_manager.show_popup(
                'Credits',
                (
                    'Crypt Hero\n'
                    'Made for the Ludum Dare 45 - Start with nothing\n\n'
                    'Design\n'
                    'Belug\n\n'
                    'Programming\n'
                    'Belug\n\n'
                    'Art\n'
                    'Belug & cp437\n\n'
                    'Still missing music\n'
                    'Belug\n\n'
                    'Still missing sound effects\n'
                    'Belug\n\n'
                    'Windows version\n'
                    'Belug\n\n'
                    'Developed on Linux with python, libtcod and Rexpaint.\n\n'
                    'Special thanks to all the participants, all the players\n'
                    'that rated my game during the competition, to my friend\n'
                    'Guillaume Lapoint-Munger that help me a lot in game\n'
                    'developement, to my wife and children that support me\n'
                    'during those competitions and to all the players that\n'
                    'are still playing it today.\n\n'
                    'Thanks you!'
                ),
                'ESC to close'
            )

        self.add_trigger(
            Trigger(40, 19, show_credits, Player, False)
        )


    def pass_turn(self, move:tuple):
        super().pass_turn(move)
        if move == (0, 0):
            self.ui_manager.log('Time as passed...')
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
                self.player.fov = 100
                self.map.fov[50:55, 28] = True
                self.map.fov[48:55, 29] = True
                self.map.fov[46:55, 30] = True
                self.map.fov[48:55, 31] = True
                self.map.fov[50:55, 32] = True
                self.player.can_move = True
        self.move_entity(self.player)

    def add_ui_manager(self, ui_manager):
        self.ui_manager = ui_manager
        self.ui_manager.add_menu_line(('.', 'Pass time'))
    
    def add_player(self, player):
        super().add_player(player)
        self.player.fov = 1
        self.player.char = ord(' ')
        self.move_entity(self.player)
        self.player.can_move = False
