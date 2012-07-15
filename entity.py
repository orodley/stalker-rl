import constant
import libtcodpy as tcod

class Entity:

    """Represents a dynamic entity in the map

    x, y           -- Cartesian coordinates on the map
    char           -- Character used to display the entity on the screen
    fore_color     -- Color the character is displayed in
    is_transparent -- Is entity tile transparent?
    is_walkable    -- Can the entity be walked onto?
    item_component -- If the entity is a dropped item, this stores item information
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
        """Move entity by (dx, dy)"""
        self.x += dx
        self.y += dy

    def render(self, screen, camera_x, camera_y):
        """Renders the entity onto screen if it is in camera"""
        if (camera_x <= self.x < camera_x + constant.SCREEN_WIDTH and
            camera_y <= self.y < camera_y + constant.SCREEN_HEIGHT):
            tcod.console_set_foreground_color(screen, self.fore_color)
            tcod.console_put_char(screen, self.x - camera_x, self.y - camera_y, ord(self.char), tcod.BKGND_NONE)
