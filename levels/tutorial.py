from .base import BaseLevel
from map_objects import DefinedMap
from entity.monster import Monster
from entity.npc import NPC

class TutorialLevel(BaseLevel):
    
    def __init__(self):
        lvl_map = DefinedMap('levels/tutorial.map')
        super().__init__(lvl_map.width, lvl_map.height)
        self.set_entrance(57, 6)
        self.set_exit(2, 8)
        self.map = lvl_map
        # tutorial_goblin = Monster(31, 5)
        # self.add_entity(tutorial_goblin)
        tutorial_npc = NPC(3, 6)
        self.add_entity(tutorial_npc)
