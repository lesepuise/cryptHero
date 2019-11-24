import argparse

import tcod
from tcod import event

from entity.player import Player
from handler import handle_events
from handler.actions import handle_action
from map_objects.tile import EMPTY_TILE
from map_objects import DefinedMap
from renderer import Renderer
from renderer.ui_manager import UIManager
from levels import levels, reset_levels


def main(debug=False):
    screen_width = 80
    screen_height = 80
    map_width = 60
    map_height = 60
    menu_width = 20
    menu_height = 80
    action_width = 60
    action_height = 20

    cur_level_idx = 0
    cur_level = levels[cur_level_idx]
    player = Player()
    cur_level.add_player(player)
    tutorial_map = cur_level.get_map()
    player.add_map(tutorial_map)
    ui_manager = UIManager(player, screen_width, screen_height)
    cur_level.add_ui_manager(ui_manager)
    
    tcod.console_set_custom_font(
        'tileset/cp437_10x10.png',
        tcod.FONT_TYPE_GRAYSCALE | tcod.FONT_LAYOUT_ASCII_INROW
    )

    root_console = tcod.console_init_root(
        screen_width, screen_height, 'Crypt Hero', False,
        tcod.RENDERER_SDL2, order='F', vsync=True)

    renderer = Renderer(root_console, ui_manager, debug=debug)
    cur_level.add_renderer(renderer)

    recompute = True
    while True:
        if recompute and cur_level.recalculate_fov:
            recompute = False
            tutorial_map.compute_fov(player.x, player.y, player.fov, True, 0)

        renderer.render_level(player, cur_level.entities, tutorial_map, colors=cur_level.show_colors)

        actions = handle_events()

        move = actions.get('move')
        pass_time = actions.get('pass_time')
        exit = actions.get('exit')
        act = actions.get('act')
        restart = actions.get('restart')
        fullscreen = actions.get('fullscreen')
        god_mod = actions.get('god_mod')

        if god_mod and debug:
            player.activate_god_mod()

        if move and player.can_move and not ui_manager.popup:
            recompute = True
            player.move(*move)
            cur_level.pass_turn(move)
        
        if pass_time:
            cur_level.pass_turn((0, 0))

        if exit:
            if ui_manager.popup:
                ui_manager.remove_popup()
            else:
                return True
            if player.dead or cur_level.ended:
                return True
        
        if act:
            handle_action(act, renderer, cur_level, ui_manager)
        
        if restart and (player.dead or cur_level.ended):
            reset_levels()
            player = Player(char=ord(' '))
            ui_manager = UIManager(player, screen_width, screen_height)
            renderer = Renderer(root_console, ui_manager)
            cur_level_idx = 0
            cur_level = levels[cur_level_idx]
            cur_level.add_player(player)
            tutorial_map = cur_level.get_map()
            player.add_map(tutorial_map)
            cur_level.add_ui_manager(ui_manager)
            cur_level.add_renderer(renderer)
            recompute = True

        if fullscreen:
            tcod.console_set_fullscreen(not tcod.console_is_fullscreen())

        if player.is_on_exit():
            cur_level_idx += 1
            cur_level = levels[cur_level_idx]
            cur_level.add_player(player)
            tutorial_map = cur_level.get_map()
            player.add_map(tutorial_map)
            cur_level.add_ui_manager(ui_manager)
            cur_level.add_renderer(renderer)
            recompute = True

        if player.dead:
            ui_manager.show_popup('You are dead', 'This world falls into crumbles.\nMay you be more lucky next time.', 'Press r to reset or ESC to quit')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-D', dest='debug', action='store_const',
                    const=True, default=False, help='Enable debug mode')

    args = parser.parse_args()
    main(debug=args.debug)
