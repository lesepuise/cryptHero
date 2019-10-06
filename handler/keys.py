import tcod
from tcod import event


def handle_keys(key):
    # Movement keys
    if key.sym == event.K_UP:
        return {'move': (0, -1)}
    elif key.sym == event.K_DOWN:
        return {'move': (0, 1)}
    elif key.sym == event.K_LEFT:
        return {'move': (-1, 0)}
    elif key.sym == event.K_RIGHT:
        return {'move': (1, 0)}
    elif key.sym == event.K_PERIOD:
        return {'move': (0, 0)}

    elif key.sym == event.K_RETURN and key.mod & event.KMOD_LALT:
        # Alt+Enter: toggle full screen
        return {'fullscreen': True}
    
    elif key.sym == event.K_RETURN and key.mod & event.KMOD_LALT:
        # Enter to accept
        return {'accept': True}

    elif key.sym == event.K_ESCAPE:
        # Exit the game
        return {'exit': True}
    
    elif key.sym == event.K_l:
        return {'act': 'look'}

    elif key.sym == event.K_t:
        return {'act': 'target'}

    # No key was pressed
    return {}