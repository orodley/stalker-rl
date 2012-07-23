from math import radians

SCREEN_WIDTH = 80        # Width  of window in tiles
SCREEN_HEIGHT = 54       # Height of window in tiles
LIMIT_FPS = 30           # FPS cap

TRUNCATE_SUFFIX = "..."  # If a word cannot fit into a menu, it is truncated and this is appended

COLOR_VARIATION = 15     # r, g, and b variation to apply for tiles

MEMORY_TINT = 0.2        # r, g, and b tint for previously, but not currently seen tiles

FOV_ANGLE = radians(120) # How wide the player can see, in radians

MAX_CONDITION = 10000    # Perfect condition for a weapon

CAMERA_DISTANCE = 0      # How far ahead of the player to center the camera

INENTORY_SIZE = (9, 10)  # Size of the inventory grid for the player
SQUARE_SIZE = 5          # How large each square in the grid is
