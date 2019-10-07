import tcod

from entity.cursor import Cursor
from entity.monster import Living
from handler import handle_events

def handle_action(action, renderer, level):
    looping = True
    cur_map = level.get_map()
    cursor = Cursor(level.player.x, level.player.y, ord('X'), tcod.green)
    cursor.add_map(cur_map)
    line = False

    if action == 'look':
        handler = look
    elif action == 'target':
        handler = target
        line = True
    
    while looping:
        renderer.render_level(level.player, level.entities, cur_map, colors=level.show_colors, cursor=cursor, line=line)

        actions = handle_events()
        looping = handler(actions, cursor, level)


def look(actions, cursor, level):
    move = actions.get('move')
    exit = actions.get('exit')
    # select = actions.get('accept')

    if move:
        cursor.move(*move)

    if exit:
        return False

    return True


def target(actions, cursor, level):
    move = actions.get('move')
    exit = actions.get('exit')
    select = actions.get('accept')
    if move:
        cursor.move(*move)

    if exit:
        return False
    
    if select:
        target = level.get_entity_at(cursor.x, cursor.y)
        if isinstance(target, Living):
            target.attacked(1)
            return True


    return True