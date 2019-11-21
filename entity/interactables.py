import tcod

from . import Entity
from .living import Living

class Interactable(Entity):
    
    def __init__(self, x=1, y=1, char=ord('8'), color=tcod.white):
        super().__init__(x, y, char, color)
        self.blocking = True
    
    def interact(self, entity: Entity):
        pass


class Fountain(Interactable):
    filled_char = tcod.constants.CHAR_RADIO_SET
    emptied_char = tcod.constants.CHAR_RADIO_UNSET

    emptied_description = (
        "This is a fountain, the water is filty with mud\n"
        "and blood. The color of the water changed when\n"
        "you drank from it."
    )

    def __init__(self, x=1, y=1):
        char = Fountain.filled_char
        color = tcod.white
        super().__init__(x, y, char, color)
        self.blocking = True
        self.filled = True
        self.name = 'Fountain'
        self.description = (
            "This is a fountain, the water is crystal clear.\n"
            "An holy aura is emanate from the bassin.\n\n"
            "Walk to this fountain to drink from it."
        )
        self.transparent = True

    def interact(self, entity: Living):
        if self.filled:
            entity.healed(entity.max_hp)
            self.filled = False
            self.char = Fountain.emptied_char
            self.level.ui_manager.status_line = "You drink the fountain's water, you feel refreshed."
            self.description = self.emptied_description
        else:
            self.level.ui_manager.status_line = "The water looks filty, you better not drink again."
