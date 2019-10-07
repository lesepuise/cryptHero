import tcod
from tcod import event

from entity.player import Player
from handler import handle_events
from handler.actions import handle_action
from map_objects.tile import EMPTY_TILE
from map_objects import DefinedMap
from renderer import Renderer
from renderer.ui_manager import UIManager
from levels import levels


def main():
    cur_level_idx = 0
    cur_level = levels[cur_level_idx]
    player = Player(char=ord(' '))
    cur_level.add_player(player)
    tutorial_map = cur_level.get_map()
    player.add_map(tutorial_map)
    ui_manager = UIManager()
    cur_level.add_ui_manager(ui_manager)

    screen_width = 100
    screen_height = 80
    map_width = 65
    map_height = 60
    menu_width = 35
    menu_height = 80
    action_width = 66
    action_height = 20
    
    tcod.console_set_custom_font(
        'tileset/arial10x10.png',
        tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD
    )

    root_console = tcod.console_init_root(
        screen_width, screen_height, 'libtcod tutorial revised', False,
        tcod.RENDERER_OPENGL2, order='F', vsync=True)

    map_con = tcod.console.Console(map_width, map_height, order='F')
    menu_con = tcod.console.Console(menu_width, menu_height, order='F')
    action_con = tcod.console.Console(action_width, action_height, order='F')

    renderer = Renderer(root_console, map_con, menu_con, action_con, ui_manager)
    cur_level.add_renderer(renderer)

    recompute = True
    while True:
        if recompute:
            recompute = False
            tutorial_map.compute_fov(player.x, player.y, player.fov, True, 0)

        renderer.render_level(player, cur_level.entities, tutorial_map, colors=cur_level.show_colors)

        actions = handle_events()

        move = actions.get('move')
        exit = actions.get('exit')
        act = actions.get('act')
        restart = actions.get('restart')
        fullscreen = actions.get('fullscreen')

        if move:
            recompute = True
            player.move(*move)
            cur_level.pass_turn(move)

        if exit:
            return True
        
        if act:
            handle_action(act, renderer, cur_level)
        
        if restart and player.dead:
            cur_level_idx = 0
            cur_level = levels[cur_level_idx]
            player = Player(char=ord(' '))
            cur_level.add_player(player)
            tutorial_map = cur_level.get_map()
            player.add_map(tutorial_map)
            ui_manager = UIManager()
            cur_level.add_ui_manager(ui_manager)
            cur_level.add_renderer(renderer)
            recompute = True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

if __name__ == '__main__':
    main()