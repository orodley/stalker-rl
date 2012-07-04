import random
import tile_types
import constant
import libtcodpy as tcod
import copy

class Map:
    def __init__(self, data):
        self.data = data
        self.height = len(data)
        self.width = len(data[0])

    def render(self, screen, camera_x, camera_y):
        for y in xrange(constant.SCREEN_HEIGHT):
            for x in xrange(constant.SCREEN_WIDTH):
                tcod.console_put_char_ex(screen, x, y, ord(self.data[y + camera_y][x + camera_x].char),
                     self.data[y + camera_y][x + camera_x].fore_color, self.data[y + camera_y][x + camera_x].back_color)

def make_map(width, height):
    return Map([[Tile("grass", False, False) for n in xrange(width)] for n in xrange(height)])
            
class Tile:
    def __init__(self, material, blocks_movement, blocks_light):
        self.material = material
        self.char =  random.choice(tile_types.char[material])

        self.back_color = copy.deepcopy(tile_types.color[material])
        self.fore_color = copy.deepcopy(tile_types.color[material])

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

        self.blocks_movement = blocks_movement
        self.blocks_light = blocks_light
