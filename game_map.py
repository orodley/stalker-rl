import random
import libtcodpy as tcod
import tile_types
import constant
import fov

class Map:

    """Represents the game map

    data   -- Nested array of Tiles. self.data[y][x] gets a tile at any (x, y) position
    height -- Height of map
    width  -- Width of map
    """

    def __init__(self, data):
        self.data = data
        # Compute height and width for convenient access
        self.height = len(data)
        self.width = len(data[0])

    def render(self, screen, fov_map, camera_x, camera_y, player_x, player_y, mouse_x, mouse_y):
        """Renders the map onto a given console, using line of sight from the player"""
        tcod.console_clear(screen)

        for y in xrange(constant.SCREEN_HEIGHT):
            adj_y = y + camera_y

            for x in xrange(constant.SCREEN_WIDTH):
                adj_x = x + camera_x

                if fov.in_player_fov(adj_x, adj_y, player_x, player_y, mouse_x + camera_x,
                                     mouse_y + camera_y, fov_map):
                    self.data[adj_y][adj_x].explored = True
                    tcod.console_put_char_ex(screen, x, y,
                                             ord(self.data[adj_y][adj_x].char),
                                             self.data[adj_y][adj_x].fore_color,
                                             self.data[adj_y][adj_x].back_color)
                elif self.data[adj_y][adj_x].explored:
                    tcod.console_put_char_ex(screen, x, y,
                                             ord(self.data[adj_y][adj_x].char),
                                             self.data[adj_y][adj_x].explored_fore_color,
                                             self.data[adj_y][adj_x].explored_back_color)
                else:
                    tcod.console_set_back(screen, x, y, tcod.black)

def make_map(width, height):
    """Constructs a new Map"""

    return Map([[Tile("grass", True, True) for x in xrange(width)] for y in xrange(height)])

def copy_color(color):
    """Copies a tcod.Color object and returns the copy"""
    # Assigning directly creates references, not copies, but copy.deepcopy
    # is far too slow. This function is much faster
    r = color.r
    g = color.g
    b = color.b

    return tcod.Color(r, g, b)
            
class Tile:

    """Represents a tile on a map
    material            -- Type of tile. Used for lookup in tile_types
    char                -- Character displayed on empty tile
    is_transparent      -- Is the tile transparent?
    is_walkable         -- Can the tile be walked onto?
    fore_color          -- Color to draw char in. Retrieved from tile_types with variation applied
    back_color          -- Background color of the tile. Retrieved from tile_types with variation applied
    explored_fore_color -- Color to draw char in if previously seen but not currently visible. Darkened fore_color
    explored_back_color -- Background color if previously seen but not currently visible. Darkened back_color
    explored            -- Has the tile been seen before?
    """

    def __init__(self, material, is_transparent, is_walkable):
        self.material = material
        self.char =  random.choice(tile_types.data[material][0])
        self.back_color = copy_color(tile_types.data[material][1])
        self.fore_color = copy_color(tile_types.data[material][1])

        # Random variation should be applied, but should not wrap around
        # make sure that the maximum is <= 255 and the minimum is >= 0
        r_max = min(255, self.back_color.r + constant.COLOR_VARIATION)
        r_min = max(0, self.back_color.r - constant.COLOR_VARIATION)
        g_max = min(255, self.back_color.g + constant.COLOR_VARIATION)
        g_min = max(0, self.back_color.g - constant.COLOR_VARIATION)
        b_max = min(255, self.back_color.b + constant.COLOR_VARIATION)
        b_min = max(0, self.back_color.b - constant.COLOR_VARIATION)

        self.back_color.r = random.randrange(r_min, r_max + 1)
        self.back_color.g = random.randrange(g_min, g_max + 1)
        self.back_color.b = random.randrange(b_min, b_max + 1)

        self.fore_color.r = random.randrange(r_min, r_max + 1)
        self.fore_color.g = random.randrange(g_min, g_max + 1)
        self.fore_color.b = random.randrange(b_min, b_max + 1)

        # If the tile is explored it should be darker
        self.explored_fore_color = self.fore_color * constant.MEMORY_TINT
        self.explored_back_color = self.back_color * constant.MEMORY_TINT

        self.is_walkable = is_walkable
        self.is_transparent = is_transparent

        self.explored = False
