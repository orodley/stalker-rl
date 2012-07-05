import libtcodpy as tcod
import constant

def menu(items, header, x, y, width, height, target_console, background_console, alpha):
    """ Draw a menu, and return the selected meny index
    Returns only once the player has selected a menu item or pressed escape,
    which returns -1. Items are truncated and an ellipsis added if they
    do not fit within the menu rectangle

    items              -- list of strings to use as the menu entries
    header             -- string to print in the top of the window
    x, y               -- position to draw the menu
    width, height      -- width and height of the menu
    target_console     -- console to draw the menu onto (should be ui_con)
    background_console -- console to use as background (for transparency)
    alpha              -- alpha level at which to blit the menu
    """

    def draw_menu():
        tcod.console_set_foreground_color(target_console, tcod.white)
        tcod.console_print_frame(target_console, 0, 0, width, height, False, tcod.BKGND_NONE, False) 

        if header:
            tcod.console_print_center(target_console, width / 2, 0, tcod.BKGND_NONE, truncated_header)

        for pos in xrange(len(truncated_items)):
            if pos == selected_index:
                tcod.console_set_foreground_color(target_console, tcod.white)
            else:
                tcod.console_set_foreground_color(target_console, tcod.grey)

            tcod.console_print_left(target_console, 1, pos + 1,
                                    tcod.BKGND_NONE, truncated_items[pos])

        tcod.console_blit(background_console, 0, 0, constant.SCREEN_WIDTH,
                          constant.SCREEN_HEIGHT, 0, 0, 0, 1, 1)
        tcod.console_blit(target_console, 0, 0, width, height, 0, x, y, 1.0, alpha)
        tcod.console_flush()

    truncated_items = []
    selected_index = 0

    tcod.console_clear(target_console)

    for item in items:
        if len(item) > width - 2:
            truncated_items.append(item[:width - len(TRUNCATE_SUFFIX) + 2] + constant.TRUNCATE_SUFFIX)
        else:
            truncated_items.append(item)

    truncated_header = header if len(header) < width - 2 else header[:width - len(TRUNCATE_SUFFIX) + 2] + constant.TRUNCATE_SUFFIX
    
    draw_menu()

    while True:
        key = tcod.console_wait_for_keypress(True)

        if key.vk == tcod.KEY_ESCAPE:
            return -1
        elif key.vk == tcod.KEY_UP:
            selected_index += selected_index and -1
            draw_menu()
        elif key.vk == tcod.KEY_DOWN:
            selected_index += 0 if selected_index == len(truncated_items) - 1 else 1
            draw_menu()
        elif key.vk == tcod.KEY_ENTER:
            return selected_index
