from .base import BaseLevel
from map_objects import DefinedMap

class FinalLevel(BaseLevel):
    
    def __init__(self):
        lvl_map = DefinedMap('levels/tutorial.map')
        super().__init__(lvl_map.width, lvl_map.height)
        self.map = lvl_map

    