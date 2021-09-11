import math
import levelData
import colors, entities
import pygame
import enum
import renderer
import mathHelpers


class WallDirection(enum.Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


def generate_distance_table(entity):
    # Calculate Walls
    entity.rayDistanceTable = {}
    entity.entitiesInSight = []

    w = 0
    ray_dir_x = 0
    ray_dir_y = 0

    fov_depth = entity.FOVDepth
    degrees = math.ceil(math.degrees(entity.FOV))
    entity_dir_x = entity.dirX
    enity_dir_y = entity.dirY

    entity_plane_x = entity.planeX
    enity_plane_y = entity.planeY
    cam_x = 0

    entity_px = entity.px
    entity_py = entity.py

    for w in range(degrees):
        cam_x = ((2 * w) / math.ceil(math.degrees(entity.FOV))) - 1

        entity_plane_x = entity.planeX
        entity_py = entity.py

        ray_dir_x = entity_dir_x + entity_plane_x * cam_x
        ray_dir_y = enity_dir_y + enity_plane_y * cam_x

        if ray_dir_y == 0:
            ray_dir_y = 0.1
        if ray_dir_x == 0:
            ray_dir_x = 0.1

        ray_angle = math.atan2(ray_dir_x, ray_dir_y)

        map_x = int(entity_px)
        map_y = int(entity_py)

        side_dist_x = 0
        side_dist_y = 0
        perp_wall_dist = 0

        delta_dist_x = abs(1.0 / ray_dir_x)
        delta_dist_y = abs(1.0 / ray_dir_y)

        step_x = 0
        step_y = 0

        if (ray_dir_x < 0):
            step_x = -1
            side_dist_x = (entity_px - map_x) * delta_dist_x
        else:
            step_x = 1
            side_dist_x = (map_x + 1.0 - entity_px) * delta_dist_x
        if (ray_dir_y < 0):
            step_y = -1
            side_dist_y = (entity_py - map_y) * delta_dist_y
        else:
            step_y = 1
            side_dist_y = (map_y + 1.0 - entity_py) * delta_dist_y

        hit_wall = False
        steps = 0
        while not hit_wall and steps <= fov_depth:
            if (side_dist_x < side_dist_y):
                side_dist_x += delta_dist_x
                map_x += step_x
                steps += 1
                side = 0  # Looking North or South
            else:
                side_dist_y += delta_dist_y
                steps += 1
                map_y += step_y
                side = 1  # Looking east or west

            point_x = map_x
            point_y = map_y

            if (point_x < 0
                    or point_x >= levelData.Level.currentMap.level_width
                    or point_y < 0
                    or point_y >= levelData.Level.currentMap.level_height
                    or steps >= fov_depth):

                entity.rayDistanceTable[ray_angle] = None
            else:
                if levelData.Level.currentMap.grid[int(point_x)][int(point_y)]:
                    hit_wall = True
                    wall_col = levelData.Level.currentMap.grid[int(point_x)][
                        int(point_y)]
                    if (side == 0):
                        wallDistance = (map_x - entity_px +
                                        (1.0 - step_x) / 2.0) / ray_dir_x
                    else:
                        wallDistance = (map_y - entity_py +
                                        (1.0 - step_y) / 2.0) / ray_dir_y

                    if side and ray_dir_y < 0:
                        wall_dir = WallDirection.EAST
                    elif side:
                        wall_dir = WallDirection.WEST
                    elif ray_dir_x < 0:
                        wall_dir = WallDirection.SOUTH
                    else:
                        wall_dir = WallDirection.NORTH

                    entity.rayDistanceTable[ray_angle] = (wallDistance,
                                                          ray_dir_x, ray_dir_y,
                                                          ray_angle, wall_col,
                                                          wall_dir)

    _calculate_entities_in_sight(entity)


def _calculate_entities_in_sight(entity):

    fov_polygons = calculate_fov_polygon(entity)
    for e in levelData.Level.currentMap.grid_entities:
        if e != entity:
            collided = polygonPointCollision(fov_polygons, e.get_pos())
            if collided:
                ent_list = ((entity.px - e.px) * (entity.px - e.px) +
                            (entity.py - e.py) * (entity.py - e.py))
                entity.entitiesInSight.append((e, ent_list))


def polygonPointCollision(vertices, p):
    # I used the even odd rule for polygon collision
    # see: https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule
    collision = False
    nextP = 0
    vc = [0, 0]
    vn = [0, 0]
    point = [0, 0]
    point[0] = p[0]
    point[1] = p[1]
    vert_len = len(vertices)

    for current in range(vert_len):
        nextP += 1

        if (nextP == vert_len):
            nextP = 0

        vc = list(vertices[current])
        vn = list(vertices[nextP])

        if (((vc[1] > point[1] and vn[1] < point[1]) or
             (vc[1] < point[1] and vn[1] > point[1]))
                and (point[0] < (vn[0] - vc[0]) * (point[1] - vc[1]) /
                     (vn[1] - vc[1]) + vc[0])):
            collision = not collision
    return collision


def calculate_fov_polygon(entity):
    px = entity.px
    py = entity.py
    w = 0
    entityFovPoints = [(px, py)]

    for ray in entity.rayDistanceTable.items():
        if ray[1] == None:
            continue
        table_step, tableDirX, tableDirY, tableAng, table_type, table_wallDir = ray[
            1]
        pointX = px + tableDirX * table_step
        pointY = py + tableDirY * table_step
        entityFovPoints.append((pointX, pointY))

    if len(entityFovPoints) > 2:
        return entityFovPoints
    else:
        return [(px, py)] * 3


def _calculate_fov_points(scale_x, scale_y):

    all_fovs = []
    for enemy in levelData.Level.currentMap.grid_entities:
        if issubclass(type(enemy), entities.Enemy):
            enemy_fov = calculate_fov_polygon(enemy)
            enemy_fov = translate_to_map(enemy_fov, scale_x, scale_y)

            color = colors.ALMOST_BLACK
            if enemy.canSeePlayer:
                color = colors.RED
            all_fovs.append((color, enemy_fov))
    return all_fovs


def translate_to_map(coordList, scaleX, scaleY):
    newCoordList = []
    for x, y in coordList:
        newCoordList.append((y * scaleX, x * scaleY))
    return newCoordList


def render_map(screen, entity):
    # IMPORTANT !
    # Position X and Y are flippped to match the grid
    # eg: draw(x * scaleX, y * scaleY) should be
    # written as draw(y * scaleX, x * scaleY)
    # screen.fill(colors.GRAY)
    # Get the grid Scale
    scale_x = screen.get_width() / levelData.Level.currentMap.level_width
    scale_y = screen.get_height() / levelData.Level.currentMap.level_height

    # region Calculate MiniMap Shadows
    # Calculate Player FOV points
    fov_points = calculate_fov_polygon(entity)
    fov_points = translate_to_map(fov_points, scale_x, scale_y)

    # Calculate Enemy FOV points
    all_fovs = _calculate_fov_points(scale_x, scale_y)

    # endregion

    # region Draw MiniMap
    [
        pygame.draw.rect(
            screen, colors.GRAY_VARIATION_3 if
            levelData.Level.currentMap.grid[x][y] != 0 else colors.DARK_GRAY,
            [scale_x * y, scale_y * x, scale_x + 1, scale_y + 1])
        for x in range(levelData.Level.currentMap.level_width)
        for y in range(levelData.Level.currentMap.level_height)
    ]

    # Draw Player FOV
    if len(fov_points) > 2:
        pygame.draw.polygon(screen, colors.WHITE, fov_points)

    # Draw Enemy FOV
    # for c, points in all_fovs:
    #     pygame.draw.polygon(screen, c, points)

    for enemy in levelData.Level.currentMap.grid_entities:
        px = int(enemy.px * scale_y)
        py = int(enemy.py * scale_x)
        if issubclass(type(enemy), entities.Enemy):
            pygame.draw.circle(screen, colors.RED, [py, px], 2)
        if issubclass(type(enemy), entities.Collectible) and enemy.collected:
            pygame.draw.circle(screen, colors.YELLOW_WHITE, [py, px], 2)

    pygame.draw.circle(screen, colors.WHITE,
                       [int(entity.py * scale_x),
                        int(entity.px * scale_y)], 2)

    # Draw Map

    [pygame.draw.polygon(screen, c, points) for c, points in all_fovs]

    color = colors.DARK_GRAY
    for e in levelData.Level.currentMap.grid_entities:
        if issubclass(type(e), entities.Gate) and not e.open:
            pygame.draw.rect(screen, color, [
                scale_x * math.floor(e.py), scale_y * math.floor(e.px),
                scale_x + 1, scale_y + 1
            ])


def _get_wall_color(table_side):
    wall_color = colors.RED
    if table_side == WallDirection.NORTH:
        wall_color = list(colors.GRAY_VARIATION_1)
    if table_side == WallDirection.SOUTH:
        wall_color = list(colors.GRAY_VARIATION_2)
    if table_side == WallDirection.EAST:
        wall_color = list(colors.GRAY_VARIATION_3)
    if table_side == WallDirection.WEST:
        wall_color = list(colors.GRAY_VARIATION_4)
    return wall_color


def render_walls(screen, entity):

    obj_to_draw = {}
    if len(entity.rayDistanceTable) <= 1:
        return
    thickness = screen.get_width() / (len(entity.rayDistanceTable) - 1)
    w = 0
    for ray in entity.rayDistanceTable.items():
        if ray[1] == None:
            w += 1
            continue
        table_step, table_dirx, table_dir_y, table_angle, table_type, table_side = ray[
            1]
        wall_projection_distance = table_step
        line_height = abs(screen.get_height() / wall_projection_distance)
        ceiling = -line_height + (screen.get_height() / 2) + entity.angleY
        floor = line_height + (screen.get_height() / 2) + entity.angleY

        wall_color = _get_wall_color(table_side)

        obj_to_draw[(abs(wall_projection_distance), w)] = (w, ceiling, floor,
                                                           wall_color)
        w += renderer.RAY_ANGLE_STEP

    entity.entitiesInSight.sort(key=lambda x: x[1])
    for enemy, dist in entity.entitiesInSight:
        if issubclass(type(enemy), entities.SpriteEntity) and enemy != entity:
            dx, dy = mathHelpers.slope(entity.get_pos(), enemy.get_pos())

            projection_disit = (entity.planeX * entity.dirY -
                                entity.dirX * entity.planeY)

            inverse_projection_dist = 1 / projection_disit

            new_x = inverse_projection_dist * \
                (entity.dirY * dx - entity.dirX * dy)
            new_y = inverse_projection_dist * \
                (-entity.planeY * dx + entity.planeX * dy)

            new_pos_x = (entity.FOV / 2) * (1 + new_x / new_y)

            line_height = abs(screen.get_height() / new_y)
            middle = screen.get_height() / 2

            ceiling = -line_height + middle + entity.angleY
            floor = line_height + middle + entity.angleY
            obj_to_draw[(abs(new_y) - 2,
                         math.degrees(new_pos_x))] = (math.degrees(new_pos_x),
                                                      ceiling, floor, enemy)

    # Sort Obj To Draw To allow a "z-ish" buffer
    sorted_objs = list(obj_to_draw.items())
    sorted_objs.sort(key=lambda x: x[0][0], reverse=True)

    for info in sorted_objs:

        dist, vals = info
        w, ceiling, floor, data = vals
        scaled_width = w * (thickness / 1)
        ceiling = int(ceiling)
        floor = int(floor)
        if isinstance(data, list):
            pygame.draw.line(
                screen, data,
                [int(scaled_width), int(ceiling)],
                [int(scaled_width), int(floor)], math.ceil(thickness))
        if isinstance(data, entities.SpriteEntity):
            scale_multiplier = abs(
                mathHelpers.translate(floor - ceiling, 0,
                                      renderer.VIEWPORT_HEIGHT, 0, 4))
            sprite = data.get_sprite(entity)
            if sprite is not None:
                scaled_sprite = pygame.transform.scale(
                    sprite,
                    ((50 * sprite.get_height()) // sprite.get_width(), 50))

                img = pygame.transform.scale(
                    scaled_sprite,
                    (int(scaled_sprite.get_width() * scale_multiplier),
                     int(scaled_sprite.get_height() * scale_multiplier)))

                screen.blit(img, [
                    int(scaled_width - int(img.get_width() / 1.5)),
                    int(floor - img.get_rect().height)
                ])
