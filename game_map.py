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

    def render(self, console_buffer, fov_map, camera_x, camera_y, player_x, player_y, mouse_x, mouse_y):
        """Renders the map onto a given console, using line of sight from the player"""

        for y in xrange(constant.SCREEN_HEIGHT):
            adj_y = y + camera_y

            for x in xrange(constant.SCREEN_WIDTH):
                adj_x = x + camera_x
                char = self.data[adj_y][adj_x].char

                if fov.in_player_fov(adj_x, adj_y, player_x, player_y, mouse_x + camera_x,
                                     mouse_y + camera_y, fov_map):
                    f_color = self.data[adj_y][adj_x].fore_color
                    b_color = self.data[adj_y][adj_x].back_color
                    self.data[adj_y][adj_x].explored = True
                    console_buffer.set(x, y, b_color.r, b_color.g, b_color.b,
                                             f_color.r, f_color.g, f_color.b, char)

                elif self.data[adj_y][adj_x].explored:
                    f_color = self.data[adj_y][adj_x].explored_fore_color
                    b_color = self.data[adj_y][adj_x].explored_back_color

                    console_buffer.set(x, y, b_color.r, b_color.g, b_color.b,
                                             f_color.r, f_color.g, f_color.b, char)
                else:
                    console_buffer.set_back(x, y, 0, 0, 0)

def make_map(width, height):
    """Constructs a new Map"""

    BSP_DEPTH = 3

    HOUSE_WIDTH = 30
    HOUSE_HEIGHT = 20

    MIN_ROOM_WIDTH = 5
    MIN_ROOM_HEIGHT = 5

    MAX_H_RATIO = 1.5
    MAX_V_RATIO = 1.5

    HURST = 0.5
    LACNULARITY = 2.0
    THRESHOLD = 0.99

    def make_house():
        bsp_tree = tcod.bsp_new_with_size(0, 0, HOUSE_WIDTH - 1, HOUSE_HEIGHT - 1)
        tcod.bsp_split_recursive(bsp_tree, 0, BSP_DEPTH, MIN_ROOM_WIDTH, MIN_ROOM_HEIGHT,
                                 MAX_H_RATIO, MAX_V_RATIO)

        tcod.bsp_traverse_inverted_level_order(bsp_tree, handle_node)
        house_array[-1][-1] = Tile("wall", True, True)

        noise = tcod.noise_new(2, HURST, LACNULARITY)
        for x in xrange(HOUSE_WIDTH):
            for y in xrange(HOUSE_HEIGHT):
                if tcod.noise_get_turbulence(noise, [x, y], 32.0, tcod.NOISE_SIMPLEX) > THRESHOLD:
                    house_array[y][x] = Tile("floor", True, True)

    def handle_node(node, user_data):
        if tcod.bsp_is_leaf(node):
            rectangle(node.x, node.y, node.w + 1, node.h + 1, house_array)
            return True
        else:
            return False

    def rectangle(x, y, w, h, array):
        for n in xrange(w):
            array[y][x + n] = Tile("wall", False, False)
            array[y + h - 1][x + n] = Tile("wall", False, False)
        for n in xrange(h):
            array[y + n][x] = Tile("wall", False, False)
            array[y + n][x + w - 1] = Tile("wall", False, False)

    the_map =  Map([[Tile("grass", True, True) for x in xrange(width)] for y in xrange(height)])

    """
    (t_x, t_y) = (width / 2, height / 2)
    # A
    rectangle(t_x, t_y, 1, 10, the_map.data)
    rectangle(t_x, t_y, 5, 1, the_map.data)
    rectangle(t_x + 5, t_y, 1, 10, the_map.data)
    rectangle(t_x, t_y + 5, 5, 1, the_map.data)
    t_x += 7
    # G
    rectangle(t_x, t_y, 1, 10, the_map.data)
    rectangle(t_x, t_y, 5, 1, the_map.data)
    rectangle(t_x, t_y + 9, 5, 1, the_map.data)
    rectangle(t_x + 4, t_y + 5, 1, 5, the_map.data)
    rectangle(t_x + 2, t_y + 5, 3, 1, the_map.data)
    t_x += 7
    # D
    rectangle(t_x, t_y, 1, 10, the_map.data)
    rectangle(t_x, t_y, 4, 1, the_map.data)
    rectangle(t_x + 4, t_y + 1, 1, 9, the_map.data)
    rectangle(t_x, t_y + 9, 5, 1, the_map.data)
    t_x += 7
    # G
    rectangle(t_x, t_y, 1, 10, the_map.data)
    rectangle(t_x, t_y, 5, 1, the_map.data)
    rectangle(t_x, t_y + 9, 5, 1, the_map.data)
    rectangle(t_x + 4, t_y + 5, 1, 5, the_map.data)
    rectangle(t_x + 2, t_y + 5, 3, 1, the_map.data)
    """

    house_array = [[Tile("floor", True, True) for x in xrange(HOUSE_WIDTH)] for y in xrange(HOUSE_HEIGHT)]
    make_house()

    for x in xrange(len(house_array[0])):
        for y in xrange(len(house_array)):
            the_map.data[y + constant.SCREEN_HEIGHT / 2 + 2][x + constant.SCREEN_WIDTH / 2 + 2] = house_array[y][x]

    return the_map

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
        variation = tile_types.data[material][2]

        # Random variation should be applied, but should not wrap around
        # make sure that the maximum is <= 255 and the minimum is >= 0
        r_max = min(255, self.back_color.r + variation)
        r_min = max(0, self.back_color.r - variation)
        g_max = min(255, self.back_color.g + variation)
        g_min = max(0, self.back_color.g - variation)
        b_max = min(255, self.back_color.b + variation)
        b_min = max(0, self.back_color.b - variation)

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
