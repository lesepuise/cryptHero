import tcod
from tcod import event

from .key_handler import handle_keys


def handle_events():
    actions = {}
    for evt in tcod.event.get():
        action = {}
        if evt.type == "QUIT":
            print(evt)
            raise SystemExit()
        elif evt.type == "KEYDOWN":
            # print(evt)
            action = handle_keys(evt)
        elif evt.type == "MOUSEBUTTONDOWN":
            # print(evt)
            pass
        elif evt.type == "MOUSEMOTION":
            # print(evt)
            pass
        else:
            # print(evt)
            pass
        actions.update(action)
    return actions