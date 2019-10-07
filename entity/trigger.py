from entity import Entity


class Trigger():
    def __init__(self, x, y, func, trigger_class:Entity, once=True, triggered=False):
        self.x = x
        self.y = y
        self.func = func
        self.once = once
        self.triggered = triggered
        self.trigger_class = trigger_class
    
    def trigger(self, renderer, entity):
        if not self.triggered and isinstance(entity, self.trigger_class):
            self.func(renderer, entity)
            if self.once:
                self.triggered = True
