from math import radians

SCREEN_WIDTH = 80        # Width  of window in tiles
SCREEN_HEIGHT = 54       # Height of window in tiles
LIMIT_FPS = 30           # FPS cap

TRUNCATE_SUFFIX = "..."  # If a word cannot fit into a menu, it is truncated and this is appended

COLOR_VARIATION = 15     # r, g, and b variation to apply for tiles

MEMORY_TINT = 0.2        # r, g, and b tint for previously, but not currently seen tiles

FOV_ANGLE = radians(120) # How wide can the player see, in radians

MAX_CONDITION = 10000    # Perfect condition for a weapon
