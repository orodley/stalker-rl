import constant
import libtcodpy as tcod

class Entity:

    """ Represents a dynamic entity in the map

    x, y       -- cartesian coordinates on the map
    char       -- character used to display the entity on the screen
    fore_color -- color the character is displayed in
    """

    def __init__(self, x, y, char, fore_color, is_transparent=True, is_walkable=True,
                    item_component=None):
        self.x = x
        self.y = y
        self.char = char
        self.fore_color = fore_color
        self.is_transparent = is_transparent
        self.is_walkable = is_walkable

        if item_component:
            self.item_component = item_component

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def render(self, screen, camera_x, camera_y):
        if (camera_x <= self.x < camera_x + constant.SCREEN_WIDTH and
            camera_y <= self.y < camera_y + constant.SCREEN_HEIGHT):
            tcod.console_set_foreground_color(screen, self.fore_color)
            tcod.console_put_char(screen, self.x - camera_x, self.y - camera_y, ord(self.char), tcod.BKGND_NONE)
