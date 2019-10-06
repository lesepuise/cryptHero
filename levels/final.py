from . import BaseLevel
from map_objects import DefinedMap

class FinalLevel(BaseLevel):
    
    def __init__(self):
        super().__init__()
        self.map = DefinedMap('levels/tutorial.map')

    