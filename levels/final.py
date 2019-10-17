from .base import BaseLevel
from map_objects import DefinedMap
from entity.monster import Daemon

from entity.weapons import Axe

class FinalLevel(BaseLevel):
    
    def __init__(self):
        lvl_map = DefinedMap('levels/final.map')
        super().__init__(lvl_map.width, lvl_map.height)
        self.map = lvl_map
        self.set_entrance(58, 6)
        boss = Daemon(3, 6, 10)
        self.add_entity(boss)
    
    def add_player(self, player):
        super().add_player(player)
        self.player.fov = 100
        self.player.weapon = Axe()