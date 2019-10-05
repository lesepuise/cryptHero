import tcod
from tcod import event

from entity.player import Player
from handler import handle_events
from map_objects.tile import EMPTY_TILE
from map_objects import Map


def main():
    screen_width = 80
    screen_height = 50
    player = Player()

    tcod.console_set_custom_font(
        'tileset/arial10x10.png',
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    )

    root_console = tcod.console_init_root(
        screen_width, screen_height, 'libtcod tutorial revised', False)

    con = tcod.console.Console(screen_width, screen_height)

    tutorial_map = Map('levels/tutorial.map')
    print(tutorial_map.tileschar)
    
    print(chr(player.char))
    while True:
        con.fg[:] = tcod.white
        con.put_char(player.x, player.y, player.char, tcod.BKGND_NONE)
        con.blit(root_console, 0, 0, 0, 0, screen_width, screen_height)
        tcod.console_flush()
        con.put_char(player.x, player.y, EMPTY_TILE, tcod.BKGND_NONE)

        actions = handle_events()

        move = actions.get('move')
        exit = actions.get('exit')
        fullscreen = actions.get('fullscreen')

        if move:
            dx, dy = move
            player.x += dx
            player.y += dy

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    main()