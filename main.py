#!/usr/bin/env python

import os
import libtcodpy as tcod
import game_map
import ui
import entity
import constant
import geometry
import fov

MAIN_MENU_WIDTH = 30  # Size of main menu
MAIN_MENU_HEIGHT = 10 
MAIN_MENU_X = (constant.SCREEN_WIDTH / 2)  - (MAIN_MENU_WIDTH / 2) # Co-ordinates to draw main menu at
MAIN_MENU_Y = (constant.SCREEN_HEIGHT / 2) - (MAIN_MENU_HEIGHT / 2)

INVENTORY_X = 2 # Position to draw inventory menu at
INVENTORY_Y = 2

VISION_RANGE = 40 # How far the player can see

tcod.console_set_custom_font(os.path.join('fonts', 'terminal8x8_aa_ro.png'),
                             tcod.FONT_LAYOUT_ASCII_INROW)

tcod.console_init_root(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, 'S.T.A.L.K.E.R RL', False)

# Console for any temporary UI elements (inventory, equipment, etc)
ui_con   = tcod.console_new(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)
# Main console that the map and constant UI elements are rendered to
game_con = tcod.console_new(constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT)

tcod.sys_set_fps(constant.LIMIT_FPS)
tcod.console_set_keyboard_repeat(10, 50)

tcod.console_credits()

img = tcod.image_load(os.path.join('images', 'menu_background.png'))
#img2 = tcod.image_load(os.path.join('images', 'test.png'))
#tcod.image_set_key_color(img2, tcod.pink)
tcod.image_blit_2x(img, game_con, 0, 0)
#tcod.image_blit(img2, game_con, 10, 10, tcod.BKGND_SET, 1, 1, 0)
tcod.console_blit(game_con, 0, 0, constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, 0, 0, 0)
tcod.console_flush()

def play_arena():
    map_size = (constant.SCREEN_WIDTH * 4, constant.SCREEN_HEIGHT * 4)
    the_map = game_map.make_map(*map_size)
    fov_map = tcod.map_new(*map_size)
    player = entity.Entity(map_size[0] / 2, map_size[1] / 2, "@", tcod.black)

    entity_list = [player]

    camera_x, camera_y = (player.x, player.y)

    fov_map = fov.update_fov_map(the_map, fov_map)
    tcod.map_compute_fov(fov_map, player.x, player.y, VISION_RANGE, True, tcod.FOV_BASIC)
    fov_recompute = True

    in_menu = False
    menu_index = 0
    selected_inv_square = None

    test = tcod.image_load(os.path.join("images", "weapons", "Makarov PM.png"))
    tcod.image_set_key_color(test, tcod.pink)

    mouse_status = tcod.mouse_get_status()
    
    while True:
        # Get input
        key = tcod.console_check_for_keypress(tcod.KEY_PRESSED)
        mouse_status = tcod.mouse_get_status()

        if not in_menu:
            # Update camera. This must be done before rendering
            (center_x, center_y) = geometry.get_point_ahead(player.x, player.y, mouse_status.cx + camera_x,
                                                   mouse_status.cy + camera_y, constant.CAMERA_DISTANCE)
            (camera_x, camera_y) = geometry.update_camera(center_x, center_y, the_map.width, the_map.height)
            player_facing_point = (mouse_status.cx, mouse_status.cy)

        # Update FOV
        if fov_recompute:
            tcod.map_compute_fov(fov_map, player.x, player.y, VISION_RANGE, True, tcod.FOV_BASIC)
        fov.update_entity_fov(entity_list, the_map, fov_map)

        # Render the map and entities
        the_map.render(game_con, fov_map, camera_x, camera_y, player.x, player.y, *player_facing_point)
        
        # Only entities in the player's line of sight should be drawn
        for _entity in entity_list:
            if fov.in_player_fov(_entity.x, _entity.y, player.x, player.y, mouse_status.cx + camera_x,
                                 mouse_status.cy + camera_y, fov_map):
                _entity.render(game_con, camera_x, camera_y)

        # fps display
        tcod.console_print_right(game_con, constant.SCREEN_WIDTH - 1, 0, tcod.BKGND_NONE, str(tcod.sys_get_fps()))
        
        # Finally, blit the console
        tcod.console_blit(game_con, 0, 0, constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, 0, 0, 0)

        # If in inventory, draw inventory grid
        if in_menu == "inventory":
            tcod.console_clear(ui_con)
            ui.draw_checkerboard(ui_con, constant.INENTORY_SIZE[0], constant.INENTORY_SIZE[1],
                                 constant.SQUARE_SIZE, tcod.grey, tcod.dark_grey)
            tcod.image_blit_2x(test, ui_con, 0, 0, 0, 0, -1, -1)
            if selected_inv_square is not None:
                tcod.console_print_frame(ui_con, selected_inv_square[0] * constant.SQUARE_SIZE,
                                                 selected_inv_square[1] * constant.SQUARE_SIZE,
                                                 constant.SQUARE_SIZE, constant.SQUARE_SIZE, False, tcod.BKGND_NONE, False)
            tcod.console_blit(ui_con, 0, 0, constant.INENTORY_SIZE[0] * constant.SQUARE_SIZE,
                              constant.INENTORY_SIZE[1] * constant.SQUARE_SIZE, 0, INVENTORY_X, INVENTORY_Y)

        tcod.console_flush()
        fov_recompute = False

        # Handle input
        if not in_menu:
            if key.vk == tcod.KEY_LEFT: # Move left
                if not entity.check_collision(player.x - 1, player.y, the_map, entity_list):
                    player.x -= 0 if player.x == 0 else 1
                    fov_recompute = True
            elif key.vk == tcod.KEY_RIGHT: # Move right
                if not entity.check_collision(player.x + 1, player.y, the_map, entity_list):
                    player.x += 0 if player.x == the_map.width else 1
                    fov_recompute = True
            elif key.vk == tcod.KEY_UP: # Move up
                if not entity.check_collision(player.x, player.y - 1, the_map, entity_list):
                    player.y -= 0 if player.y == 0 else 1
                    fov_recompute = True
            elif key.vk == tcod.KEY_DOWN: # Move down
                if not entity.check_collision(player.x, player.y + 1, the_map, entity_list):
                    player.y += 0 if player.y == the_map.height else 1
                    fov_recompute = True
            elif key.c == ord("i"):
                in_menu = "inventory"
            elif key.vk == tcod.KEY_ESCAPE: # Quit back to main menu
                break
        elif in_menu == "inventory":
            if mouse_status.lbutton_pressed:
                prev_square = selected_inv_square
                selected_inv_square = ((mouse_status.cx - INVENTORY_X) / constant.SQUARE_SIZE,
                                       (mouse_status.cy - INVENTORY_Y) / constant.SQUARE_SIZE)
                if selected_inv_square == prev_square:
                    selected_inv_square = None
                elif not ((0 <= selected_inv_square[0] < constant.INENTORY_SIZE[0]) and
                          (0 <= selected_inv_square[1] < constant.INENTORY_SIZE[1])):
                    selected_inv_square = prev_square
                print (mouse_status.cx, mouse_status.cy), selected_inv_square
            elif key.c == ord("i"):
                in_menu = ""

main_menu_index = 0
while not tcod.console_is_window_closed():
    tcod.image_blit_2x(img, game_con, 0, 0)
    #tcod.image_blit(img2, game_con, 10, 10, tcod.BKGND_SET, 1, 1, 0)
    tcod.console_blit(game_con, 0, 0, constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, 0, 0, 0)
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
                tcod.console_blit(game_con, 0, 0, constant.SCREEN_WIDTH, constant.SCREEN_HEIGHT, 0, 0, 0)
                tcod.console_clear(ui_con)
                ui.draw_menu(ui_con, "Select game mode", ['Arena'], MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT, main_menu_index)
                tcod.console_blit(ui_con, 0, 0, MAIN_MENU_WIDTH, MAIN_MENU_HEIGHT, 0, MAIN_MENU_X, MAIN_MENU_Y, 1.0, 0.7)
                tcod.console_flush()

                option = ui.handle_menu_input(tcod.console_wait_for_keypress(True), gamemode_menu_index, 1)

                if option == "ENTER":
                    if gamemode_menu_index == 0:
                        play_arena()
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
