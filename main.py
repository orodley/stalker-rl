import os
import libtcodpy as tcod
import game_map
import ui
import entity
import constant
import geometry
import fov
import item
import item_types

def play_arena(game_con, ui_con):
    map_size = (constant.SCREEN_WIDTH * 1, constant.SCREEN_HEIGHT * 1)
    the_map = game_map.make_map(*map_size)
    fov_map = tcod.map_new(*map_size)

    player = entity.Entity(map_size[0] / 2, map_size[1] / 2, "@", tcod.black)
    player.inventory_component = item.Inventory(player, constant.INENTORY_SIZE[0],
                                constant.INENTORY_SIZE[1], constant.WEIGHT_LIMIT)


    blah = "Makarov PM"
    test_makarov = item.Item(blah, item_types.firearms[blah][-1])
    test_makarov.gun_component = item.Gun(test_makarov, *item_types.firearms[blah][:-1])
    makarov_entity = entity.Entity(map_size[0] / 2 + 1, map_size[1] / 2 + 1, "]",
                                   tcod.dark_grey, item_component=test_makarov,
                                   is_walkable=True)

    entity_list = [player, makarov_entity]

    camera_x, camera_y = (player.x, player.y)

    fov_map = fov.update_fov_map(the_map, fov_map)
    tcod.map_compute_fov(fov_map, player.x, player.y, constant.VISION_RANGE, True, tcod.FOV_BASIC)
    fov_recompute = True

    in_menu = False
    selected_inv_square = None

    test = tcod.image_load(os.path.join("images", "weapons", "Makarov PM.png"))
    tcod.image_set_key_color(test, tcod.pink)

    # Set initial values for key and mouse event; required to pass into sys_check_for_event
    key = tcod.console_check_for_keypress(tcod.KEY_PRESSED)
    mouse_status = tcod.mouse_get_status()
    
    while True:
        # Get input
        tcod.sys_check_for_event(tcod.EVENT_KEY_PRESS | tcod.EVENT_MOUSE, key, mouse_status)

        if not in_menu:
            # Update camera. This must be done before rendering
            (center_x, center_y) = geometry.get_point_ahead(player.x, player.y, mouse_status.cx + camera_x,
                                                   mouse_status.cy + camera_y, constant.CAMERA_DISTANCE)
            (camera_x, camera_y) = geometry.update_camera(center_x, center_y, the_map.width, the_map.height)
            player_facing_point = (mouse_status.cx, mouse_status.cy)

        # Update FOV
        if fov_recompute:
            tcod.map_compute_fov(fov_map, player.x, player.y, constant.VISION_RANGE, True, tcod.FOV_BASIC)
        fov.update_entity_fov(entity_list, the_map, fov_map)

        # Render the map and entities
        the_map.render(game_con, fov_map, camera_x, camera_y, player.x, player.y, *player_facing_point)
        
        # Only entities in the player's line of sight should be drawn
        for _entity in reversed(entity_list):
            if fov.in_player_fov(_entity.x, _entity.y, player.x, player.y, mouse_status.cx + camera_x,
                                 mouse_status.cy + camera_y, fov_map):
                _entity.render(game_con, camera_x, camera_y)

        # fps display
        tcod.console_print_ex(game_con, constant.SCREEN_WIDTH - 1, 0, tcod.BKGND_NONE, tcod.RIGHT, str(tcod.sys_get_fps()))
        
        # Finally, blit the console
        tcod.console_blit(game_con, 0, 0, 0, 0, 0, 0, 0)

        # If in inventory, draw inventory grid
        if in_menu == "inventory":
            tcod.mouse_show_cursor(True)
            tcod.console_clear(ui_con)
            ui.draw_checkerboard(ui_con, constant.INENTORY_SIZE[0], constant.INENTORY_SIZE[1],
                                 constant.SQUARE_SIZE, tcod.grey, tcod.dark_grey)
            ui.draw_inventory_items(ui_con, player.inventory_component)
            if selected_inv_square is not None:
                tcod.console_print_frame(ui_con, selected_inv_square[0] * constant.SQUARE_SIZE,
                                                 selected_inv_square[1] * constant.SQUARE_SIZE,
                                                 constant.SQUARE_SIZE, constant.SQUARE_SIZE, False, tcod.BKGND_NONE, False)
            tcod.console_blit(ui_con, 0, 0, constant.INENTORY_SIZE[0] * constant.SQUARE_SIZE,
                              constant.INENTORY_SIZE[1] * constant.SQUARE_SIZE, 0, constant.INVENTORY_X, constant.INVENTORY_Y)

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
            elif key.c == ord(","):
                for _entity in entity_list:
                    if (_entity.item_component is not None and
                            _entity.x == player.x and
                            _entity.y == player.y):
                        player.inventory_component.add(_entity.item_component)
                        entity_list.remove(_entity)
                        
                                                              
            elif key.vk == tcod.KEY_ESCAPE: # Quit back to main menu
                break
        elif in_menu == "inventory":
            if mouse_status.lbutton_pressed:
                prev_square = selected_inv_square
                selected_inv_square = ((mouse_status.cx - constant.INVENTORY_X) / constant.SQUARE_SIZE,
                                       (mouse_status.cy - constant.INVENTORY_Y) / constant.SQUARE_SIZE)
                if selected_inv_square == prev_square:
                    selected_inv_square = None
                elif not ((0 <= selected_inv_square[0] < constant.INENTORY_SIZE[0]) and
                          (0 <= selected_inv_square[1] < constant.INENTORY_SIZE[1])):
                    selected_inv_square = prev_square
            elif key.c == ord("i"):
                tcod.mouse_show_cursor(False)
                in_menu = ""
