import math
import constant

def update_camera(follow_x, follow_y, map_width, map_height):
    """Returns (camera_x, camera_y) centered on (follow_x, follow_y)"""
    camera_x = follow_x - constant.SCREEN_WIDTH / 2
    if camera_x < 0:
        camera_x = 0
    elif camera_x > map_width - constant.SCREEN_WIDTH:
        camera_x = map_width - constant.SCREEN_WIDTH

    camera_y = follow_y - constant.SCREEN_HEIGHT / 2
    if camera_y < 0:
        camera_y = 0
    elif camera_y > map_height - constant.SCREEN_HEIGHT:
        camera_y = map_height - constant.SCREEN_HEIGHT

    return (camera_x, camera_y)

def get_point_ahead(player_x, player_y, mouse_x, mouse_y, distance):
    """Returns the co-ordinates of a point "distance" ahead of the player"""
    if player_x == mouse_x and player_y == mouse_y:
        return (player_x, player_y) # Avoid division by zero

    # What proportion of the player-mouse distance the target point is at
    proportion = distance / math.sqrt((player_x - mouse_x) ** 2 + (player_y - mouse_y) ** 2)

    point_x = int(round(player_x - (proportion * (player_x - mouse_x))))
    point_y = int(round(player_y - (proportion * (player_y - mouse_y))))

    return (point_x, point_y)

