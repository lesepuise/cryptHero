import tcod

from .base import BaseLevel
from map_objects import Debug
from entity.monster import TutorialGoblin
from entity.npc import NPC
from entity.player import Player
from entity.trigger import Trigger
from map_objects.structure import Fountain

class DebugLevel(BaseLevel):

    def __init__(self):
        super().__init__(16, 16)
        self.map = Debug()
        self.show_colors = False
        self.set_entrance(0, 0)
        self.set_exit(15, 15)
    
    def add_player(self, player):
        super().add_player(player)
        player.fov = 50
