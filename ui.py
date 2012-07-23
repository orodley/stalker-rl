import libtcodpy as tcod
import constant

def draw_menu(console, header, items, width, height, selected_index):
    """Draws a menu and returns. Used in non-blocking menu loops
    Usually drawn to a temporary console and then blitted to wherever you need it
    """

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

def draw_rectangle(console, color, x, y, width, height=None, flags=tcod.BKGND_SET):
    """Draw a rectangle on target console. If height no provided, draw a square by default"""

    if height is None:
        height = width

    for _x in xrange(x, x + width):
        for _y in xrange(y, y + width):
            tcod.console_set_back(console, _x, _y, color, flags)

def draw_checkerboard(console, width, height, square_size, color1, color2):
    """Draws a checkerboard pattern on the specified console.
    Width and height are measured in squares in checkerboard, not cells
    """

    for y in xrange(0, height * square_size, square_size):
        for x in xrange(0, width * square_size, square_size):
            if x % 2 == y % 2:
                draw_rectangle(console, color1, x, y, square_size)
            else:
                draw_rectangle(console, color2, x, y, square_size)

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
