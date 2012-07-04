#!/usr/bin/env python

import os
import libtcodpy as tcod

import game_map
import ui
import entity
import constant

MAIN_MENU_X = 5
MAIN_MENU_Y = 5
MAIN_MENU_WIDTH = 30 
MAIN_MENU_HEIGHT = 10 

tcod.console_set_custom_font(os.path.join('fonts', 'terminal10x10.png'),
                             tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

tcod.console_init_root(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, 'S.T.A.L.K.E.R RL', False)
ui_con   = tcod.console_new(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)
game_con = tcod.console_new(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)

tcod.sys_set_fps(constant.LIMIT_FPS)
tcod.console_set_keyboard_repeat(10, 50)

tcod.console_credits()

img = tcod.image_load(os.path.join('images', 'menu_background.png'))
tcod.image_blit_2x(img, game_con, 0, 0)
tcod.console_blit(game_con, 0, 0, constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, 0, 0, 0)
tcod.console_flush()

def update_camera(follow_x, follow_y, map_width, map_height):
    camera_x = follow_x - constant.SCREEN_WIDTH / 2
    if camera_x < 0:
        camera_x = 0
    elif camera_x > map_width - constant.SCREEN_WIDTH:
        camera_x = map_width - constant.SCREEN_WIDTH

    camera_y = follow_y - constant.SCREEN_HEIGHT / 2
    if camera_y < 0:
        camera_y = 0
    elif camera_y > map_height - constant.SCREEN_HEIGHT:
        camera_y = map_height - constant.SCREEN_HEIGHT

    return (camera_x, camera_y)


def play_arena():
    the_map = game_map.make_map(constant.SCREEN_WIDTH + 10, constant.SCREEN_HEIGHT + 10)
    player = entity.Entity(0, 0, "@", tcod.black)
    entity_list = [player]
    camera_x, camera_y = (0, 0)

    while True:
        (camera_x, camera_y) = update_camera(player.x, player.y,
                                             the_map.width, the_map.height)
        the_map.render(game_con, camera_x, camera_y)

        for _entity in entity_list:
            _entity.render(game_con, camera_x, camera_y)

        #tcod.console_print_right(game_con, constant.SCREEN_WIDTH - 1, 0, tcod.BKGND_NONE, tcod.sys_get_fps())

        tcod.console_blit(game_con, 0, 0, constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, 0, 0, 0)
        tcod.console_flush()

        key = tcod.console_check_for_keypress(tcod.KEY_PRESSED)
        if key.vk == tcod.KEY_LEFT:
            player.x -= 0 if player.x == 0 else 1
        elif key.vk == tcod.KEY_RIGHT:
            player.x += 0 if player.x == the_map.width else 1
        elif key.vk == tcod.KEY_UP:
            player.y -= 0 if player.y == 0 else 1
        elif key.vk == tcod.KEY_DOWN:
            player.y += 0 if player.y == the_map.height else 1
        elif key.vk == tcod.KEY_ESCAPE:
            break

while not tcod.console_is_window_closed():
    option = ui.menu(['New Game', 'Load Game', 'Highscores', 'Credits', 'Exit'], "S.T.A.L.K.E.R. RL",
                     MAIN_MENU_X, MAIN_MENU_Y, MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT, ui_con, game_con, 0.7)
    if option == 0:
        while True:
            new_game_option = ui.menu(['Arena'], "Game mode?", MAIN_MENU_X, MAIN_MENU_Y,
                                      MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT, ui_con, game_con, 0.7)
            if new_game_option == -1:
                break
            elif new_game_option == 0:
                play_arena()
                tcod.image_blit_2x(img, game_con, 0, 0)
    elif option == 1:
        pass
    elif option == 2:
        pass
    elif option == 3:
        pass
    elif option == 4:
        break
