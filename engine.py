import tcod
from tcod import event

from entity.player import Player
from handler import handle_events
from map_objects.tile import EMPTY_TILE
from map_objects import DefinedMap
from renderer import Renderer


def main():
    screen_width = 80
    screen_height = 50
    entities = []
    player = Player()
    entities.append(player)
    tutorial_map = DefinedMap('levels/tutorial.map')
    player.add_map(tutorial_map)

    tcod.console_set_custom_font(
        'tileset/arial10x10.png',
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    )

    root_console = tcod.console_init_root(
        screen_width, screen_height, 'libtcod tutorial revised', False,
        tcod.RENDERER_OPENGL2, vsync=True)

    renderer = Renderer(root_console)    
    con = tcod.console.Console(screen_width, screen_height)


    while True:
        tutorial_map.compute_fov(player.x, player.y, 10, True, 0)
        renderer.render_level(con, entities, tutorial_map, screen_width, screen_height)

        actions = handle_events()

        move = actions.get('move')
        exit = actions.get('exit')
        fullscreen = actions.get('fullscreen')

        if move:
            player.move(*move)

        if exit:
            return True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    main()