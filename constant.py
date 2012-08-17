from math import radians

SCREEN_WIDTH = 120       # Width  of window in tiles
SCREEN_HEIGHT = 79       # Height of window in tiles

INVENTORY_X = 2 # Position to draw inventory menu at
INVENTORY_Y = 2

FPS_CAP = 30

TRUNCATE_SUFFIX = "..."  # If a word cannot fit into a menu, it is truncated and this is appended

MEMORY_TINT = 0.2        # r, g, and b tint for previously, but not currently seen tiles

FOV_ANGLE = radians(120) # How wide the player can see, in radians
VISION_RANGE = 40        # How far the player can see

MAX_CONDITION = 10000    # Perfect condition for a weapon

CAMERA_DISTANCE = 0      # How far ahead of the player to center the camera

INENTORY_SIZE = (6, 5)   # Size of the inventory grid for the player in squares
WEIGHT_LIMIT = 35000     # Default weight limit for the player in grams
SQUARE_SIZE = 15         # How large each square in the grid is
