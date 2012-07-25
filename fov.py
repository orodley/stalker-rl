import math
import libtcodpy as tcod
import constant

def update_fov_map(a_map, fov_map):
    """Updates the fov map with all map information in a_map"""
    for y in xrange(a_map.height):
        for x in xrange(a_map.width):
            tcod.map_set_properties(fov_map, x, y, a_map.data[y][x].is_transparent,
                                                   a_map.data[y][x].is_walkable)
    return fov_map

def update_entity_fov(entity_list, a_map, fov_map):
    """Update fov_map for all entities in entity_list"""
    for _entity in entity_list:
        tcod.map_set_properties(fov_map, _entity.x, _entity.y,
                                _entity.is_transparent and a_map.data[_entity.y][_entity.x].is_transparent,
                                _entity.is_walkable and a_map.data[_entity.y][_entity.x].is_walkable)
    return fov_map

def in_player_fov(x, y, player_x, player_y, mouse_x, mouse_y, fov_map):
    #   # S   <- (x, y)                cosine rule used to find P; angle between
    #   |\ m                           s and m. If this angle is > FOV_ANGLE / 2,
    # p | # P <- (player_x, player_y)  the square s is out of vision
    #   |/ s
    #   # M   <- (mouse_x, mouse_y)
    p = math.sqrt((x        - mouse_x)  ** 2 + (y        - mouse_y)  ** 2)
    s = math.sqrt((player_x - mouse_x)  ** 2 + (player_y - mouse_y)  ** 2)
    m = math.sqrt((x        - player_x) ** 2 + (y        - player_y) ** 2)

    if p != 0 and s != 0 and m != 0:
        # Rearranged cosine rule formula
        angle = math.acos(round((p ** 2 - s ** 2 - m ** 2) / (-2 * s * m), 10))
    else:
        angle = 0

    if (tcod.map_is_in_fov(fov_map, x, y) and
        angle < constant.FOV_ANGLE / 2):
        return True
    else: 
        return False
