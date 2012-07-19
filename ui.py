import libtcodpy as tcod
import constant

def draw_menu(console, header, items, x, y, width, height, alpha, selected_index):
    """Draws a menu and returns. Used in non-blocking menu loops"""

    truncated_items = []

    for item in items:
        if len(item) > width - 2:
            truncated_items.append(item[:width - len(constant.TRUNCATE_SUFFIX) + 2] + constant.TRUNCATE_SUFFIX)
        else:
            truncated_items.append(item)

    truncated_header = header if len(header) < width - 2 else header[:width - len(constant.TRUNCATE_SUFFIX) + 2] + constant.TRUNCATE_SUFFIX
    tcod.console_set_foreground_color(console, tcod.white)
    tcod.console_print_frame(console, 0, 0, width, height, False, tcod.BKGND_NONE, False) 

    if header:
        tcod.console_print_center(console, width / 2, 0, tcod.BKGND_NONE, truncated_header)

    for pos in xrange(len(truncated_items)):
        if pos == selected_index:
            tcod.console_set_foreground_color(console, tcod.white)
        else:
            tcod.console_set_foreground_color(console, tcod.grey)

        tcod.console_print_left(console, 1, pos + 1,
                                tcod.BKGND_NONE, truncated_items[pos])

    tcod.console_blit(console, 0, 0, width, height, 0, x, y, 1.0, alpha)

def handle_menu_input(key, index, num_options):
    """Handles input while in menus. Returns "ENTER" if enter pushed, "ESCAPE" if escape
    pushed, and the modified index otherwise
    """

    if key.vk == tcod.KEY_UP:
        index -= index and 1
    elif key.vk == tcod.KEY_DOWN:
        index += 0 if index == num_options - 1 else 1
    elif key.vk == tcod.KEY_ENTER:
        return "ENTER"
    elif key.vk == tcod.KEY_ESCAPE:
        return "ESCAPE"

    return index
