#!/usr/bin/env python

import libtcodpy as tcod
import constant
import ui
import main
import os

MAIN_MENU_WIDTH = 30  # Size of main menu
MAIN_MENU_HEIGHT = 10 
MAIN_MENU_X = (constant.SCREEN_WIDTH / 2)  - (MAIN_MENU_WIDTH / 2) # Co-ordinates to draw main menu at
MAIN_MENU_Y = (constant.SCREEN_HEIGHT / 2) - (MAIN_MENU_HEIGHT / 2)

tcod.console_set_custom_font(os.path.join('fonts', 'terminal8x8_aa_ro.png'),
                             tcod.FONT_LAYOUT_ASCII_INROW)

tcod.console_init_root(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, 'S.T.A.L.K.E.R RL', False)

# Console for any temporary UI elements (inventory, equipment, etc)
ui_con   = tcod.console_new(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)
# Main console that the map and constant UI elements are rendered to
game_con = tcod.console_new(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)

tcod.sys_set_fps(constant.FPS_CAP)
tcod.console_set_keyboard_repeat(10, 50)
tcod.mouse_show_cursor(False)

tcod.console_credits()

img = tcod.image_load(os.path.join('images', 'menu_background.png'))
tcod.image_blit_2x(img, game_con, 0, 0)
tcod.console_blit(game_con, 0, 0, 0, 0, 0, 0, 0)
tcod.console_flush()

main_menu_index = 0
while not tcod.console_is_window_closed():
    tcod.image_blit_2x(img, game_con, 0, 0)
    #tcod.image_blit(img2, game_con, 10, 10, tcod.BKGND_SET, 1, 1, 0)
    tcod.console_blit(game_con, 0, 0, 0, 0, 0, 0, 0)
    tcod.console_clear(ui_con)
    ui.draw_menu(ui_con, "S.T.A.L.K.E.R. RL", ['New Game', 'Load Game', 'Highscores', 'Exit'],
                 MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT, main_menu_index)
    tcod.console_blit(ui_con, 0, 0, MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT, 0, MAIN_MENU_X, MAIN_MENU_Y, 1.0, 0.7)
    tcod.console_flush()

    option = ui.handle_menu_input(tcod.console_wait_for_keypress(True), main_menu_index, 4)

    if option == "ENTER":
        if main_menu_index == 0:
            gamemode_menu_index = 0
            while True:
                tcod.image_blit_2x(img, game_con, 0, 0)
                tcod.console_blit(game_con, 0, 0, 0, 0, 0, 0, 0)
                tcod.console_clear(ui_con)
                ui.draw_menu(ui_con, "Select game mode", ['Arena'], MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT, main_menu_index)
                tcod.console_blit(ui_con, 0, 0, MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT, 0, MAIN_MENU_X, MAIN_MENU_Y, 1.0, 0.7)
                tcod.console_flush()

                option = ui.handle_menu_input(tcod.console_wait_for_keypress(True), gamemode_menu_index, 1)

                if option == "ENTER":
                    if gamemode_menu_index == 0:
                        main.play_arena(game_con, ui_con)
                        tcod.image_blit_2x(img, game_con, 0, 0)
                elif option == "ESCAPE":
                    break
                else:
                    gamemode_menu_index = option
        elif main_menu_index == 1:
            pass
        elif main_menu_index == 2:
            pass
        elif main_menu_index == 3:
            break
    elif option != "ESCAPE":
        main_menu_index = option
