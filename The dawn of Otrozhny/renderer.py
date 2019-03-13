# Making this file was a nightmare to write
# it's a little bit messy but I hope you
# can handle it
# The most used function is at
# line 337 render_first_person
import pygame
import mathHelpers
import colors
import math
import renderer
import entities
import levelData
import enum


SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# If your system supports it. Toggle this comment
# it may also cause some graphical artifacts
FLAGS = pygame.DOUBLEBUF | pygame.HWSURFACE

SCREEN = pygame.display.set_mode(SCREEN_SIZE, FLAGS)
SCREEN.set_alpha(None)

VIEWPORT_HEIGHT = 320
VIEWPORT_X_OFFSET = 10
VIEWPORT_Y_OFFSET = 30

DEPTH = 40

RAY_ANGLE_STEP = 1

MAP_SCALE = 4

HUD_NUM_OF_CELLS = 5
HUD_CELL_SIZE = 100
HUD_CELL_OFFSET = 10
HUD_CELL_TITLE_OFFSET = 10
HUD_CELL_TITLE_FONT_SIZE = 12
HUD_CELL_OTHER_FONT_SIZE = 12


class WallDirection(enum.Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


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
        table_step, tableDirX, tableDirY, tableAng, table_type, table_side = ray[1]
        wall_projection_distance = table_step
        lineHeight = abs(screen.get_height() / wall_projection_distance)
        ceiling = -lineHeight + (screen.get_height() / 2) + entity.angleY
        floor = lineHeight + (screen.get_height() / 2) + entity.angleY

        wall_color = colors.RED

        if table_side == WallDirection.NORTH:
            wall_color = list(colors.GRAY_VARIATION_1)
        if table_side == WallDirection.SOUTH:
            wall_color = list(colors.GRAY_VARIATION_2)
        if table_side == WallDirection.EAST:
            wall_color = list(colors.GRAY_VARIATION_3)
        if table_side == WallDirection.WEST:
            wall_color = list(colors.GRAY_VARIATION_4)

        obj_to_draw[(abs(wall_projection_distance), w)] = (
            w, ceiling, floor, wall_color)
        w += renderer.RAY_ANGLE_STEP

    entity.entitiesInSight.sort(key=lambda x: x[1])
    for enemy, dist in entity.entitiesInSight:
        if issubclass(type(enemy), entities.SpriteEntity) and enemy != entity:
            dx, dy = mathHelpers.slope(entity.get_pos(), enemy.get_pos())

            projection_disit = (entity.planeX * entity.dirY -
                                entity.dirX * entity.planeY)

            inverse_projection_dist = 1 / projection_disit

            newX = inverse_projection_dist * \
                (entity.dirY * dx - entity.dirX * dy)
            newY = inverse_projection_dist * \
                (-entity.planeY * dx + entity.planeX * dy)

            newPosX = (entity.FOV/2) * (1 + newX/newY)

            enemy_distance = math.hypot(dx, dy)

            lineHeight = abs(screen.get_height() / newY)
            #lineHeight = abs(screen.get_height() / enemy_distance)
            middle = screen.get_height() / 2

            ceiling = -lineHeight + middle + entity.angleY
            floor = lineHeight + middle + entity.angleY
            obj_to_draw[(abs(newY)-2, math.degrees(newPosX))
                        ] = (math.degrees(newPosX), ceiling, floor, enemy)

    # Sort Obj To Draw To allow a "z-ish" buffer
    sorted_objs = list(obj_to_draw.items())
    sorted_objs.sort(key=lambda x: x[0][0], reverse=True)

    for info in sorted_objs:

        dist, vals = info
        w, ceiling, floor, data = vals
        scaledW = w * (thickness / 1)
        ceiling = int(ceiling)
        floor = int(floor)
        if isinstance(data, list):
            pygame.draw.line(screen, data, [int(scaledW), int(ceiling)], [
                int(scaledW), int(floor)], math.ceil(thickness))
        if isinstance(data, entities.SpriteEntity):
            scaleMultiplier = abs(mathHelpers.translate(
                floor-ceiling, 0, VIEWPORT_HEIGHT, 0, 4))
            sprite = data.get_sprite(entity)
            if sprite is not None:
                scaledSprite = pygame.transform.scale(
                    sprite, ((50*sprite.get_height())//sprite.get_width(), 50))

                img = pygame.transform.scale(scaledSprite,
                                             (int(scaledSprite.get_width() * scaleMultiplier),  int(scaledSprite.get_height() * scaleMultiplier)))

                screen.blit(
                    img, [int(scaledW - int(img.get_width()/1.5)), int(floor - img.get_rect().height)])


def generate_distance_table(entity):
    # Calculate Walls
    entity.rayDistanceTable = {}
    entity.entitiesInSight = []

    for w in range(math.ceil(math.degrees(entity.FOV))):
        cameraX = ((2 *  w) / math.ceil(math.degrees(entity.FOV))) - 1
        
        rayDirX = entity.dirX + entity.planeX * cameraX
        rayDirY = entity.dirY + entity.planeY * cameraX
        
        if rayDirY == 0:
            rayDirY = 0.1
        if rayDirX == 0:
            rayDirX = 0.1
            
        rayAngle = math.atan2(rayDirX, rayDirY)

        mapX = int(entity.px)
        mapY = int(entity.py)

        sideDistX = 0
        sideDistY = 0
        perpWallDist = 0

        
        deltaDistX = abs(1.0 / rayDirX)
        deltaDistY = abs(1.0 / rayDirY)

        stepX = 0
        stepY = 0

        if (rayDirX < 0):
            stepX = -1
            sideDistX = (entity.px - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - entity.px) * deltaDistX
        if (rayDirY < 0):
            stepY = -1
            sideDistY = (entity.py - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - entity.py) * deltaDistY

        hitWall = False
        steps = 0
        while not hitWall and steps <= entity.FOVDepth:
            if (sideDistX < sideDistY):
                sideDistX += deltaDistX
                mapX += stepX
                steps += 1.0
                side = 0  # Looking North or South
            else:
                sideDistY += deltaDistY
                steps += 1.0
                mapY += stepY
                side = 1  # Looking east or west

            pointX = mapX
            pointY = mapY

            if (pointX < 0 or
                pointX >= levelData.Level.currentMap.level_width or
                pointY < 0 or
                pointY >= levelData.Level.currentMap.level_height or
                    steps >= entity.FOVDepth):

                entity.rayDistanceTable[rayAngle] = None
            else:
                if levelData.Level.currentMap.grid[int(pointX)][
                        int(pointY)]:
                    hitWall = True
                    wall_col = levelData.Level.currentMap.grid[int(pointX)][
                        int(pointY)]
                    if (side == 0):
                        wallDistance = (mapX - entity.px +
                                        (1.0 - stepX) / 2.0) / rayDirX
                    else:
                        wallDistance = (mapY - entity.py +
                                        (1.0 - stepY) / 2.0) / rayDirY

                    if side and rayDirY < 0:
                        wallDir = WallDirection.EAST
                    elif side:
                        wallDir = WallDirection.WEST
                    elif rayDirX < 0:
                        wallDir = WallDirection.SOUTH
                    else:
                        wallDir = WallDirection.NORTH

                    entity.rayDistanceTable[rayAngle] = (
                        wallDistance, rayDirX, rayDirY, rayAngle, wall_col, wallDir)

    import collisionDetection
    w = 0
    fovPolygons = renderer.calculate_fov_polygon(entity)
    for e in levelData.Level.currentMap.grid_entities:
        if e != entity:
            collided = collisionDetection.polygonPointCollision(
                fovPolygons, e.get_pos())
            if collided:
                entDist = ((entity.px - e.px) * (entity.px - e.px) +
                           (entity.py - e.py) * (entity.py - e.py))
                entity.entitiesInSight.append((e, entDist))


def render_floor(screen, entity):
    if entity.angleY > screen.get_height()/2:
        return
    screen.fill(colors.DARK_GRAY, [(0, (screen.get_height(
    )//2) + entity.angleY), (screen.get_width(), screen.get_height())])


cached_first_person_canvas = None
def render_first_person_canvas(entity):
    global cached_first_person_canvas
    if cached_first_person_canvas is not None:
        render_first_person(cached_first_person_canvas, entity)
        return cached_first_person_canvas
    else:
        cached_first_person_canvas = pygame.Surface(
            [renderer.SCREEN_WIDTH - renderer.VIEWPORT_X_OFFSET * 2,
             renderer.VIEWPORT_HEIGHT]).convert()
        return render_first_person_canvas(entity)


def render_first_person(screen, entity):
    # Render 3d view
        # Clear Screen
    screen.fill(colors.ALMOST_BLACK)
    # Draw Floor/ Ceiling
    renderer.render_floor(screen, entity)
    # Draw Walls
    renderer.render_walls(screen, entity)
    # Draw Weapon
    # todo  <= I won't. Tts a stealth game!


def calculate_fov_polygon(entity):
    px = entity.px
    py = entity.py
    w = 0
    entityFovPoints = [(px, py)]
    
    for ray in entity.rayDistanceTable.items():
        if ray[1] == None:
            continue
        table_step, tableDirX, tableDirY, tableAng, table_type, table_wallDir = ray[1]
        pointX = px + tableDirX * table_step 
        pointY = py + tableDirY * table_step 
        entityFovPoints.append((pointX, pointY))


    if len(entityFovPoints) > 2:
        return entityFovPoints
    else:
        return [(px, py)] * 3


def translate_to_map(coordList, scaleX, scaleY):
    newCoordList = []
    for x, y in coordList:
        newCoordList.append((y * scaleX, x * scaleY))
    return newCoordList


def render_map(screen, entity):
    # IMPORTANT
    # Position X and Y are flippped to match the grid
    # eg: draw(x * scaleX, y * scaleY) should be
    # written as draw(y * scaleX, x * scaleY)
    screen.fill(colors.GRAY)
    # Get the grid Scale
    scaleX = screen.get_width()/levelData.Level.currentMap.level_width
    scaleY = screen.get_height()/levelData.Level.currentMap.level_height

    # region Calculate MiniMap Shadows
    # Calculate Player FOV points
    playerFovPoints = calculate_fov_polygon(entity)
    playerFovPoints = translate_to_map(playerFovPoints, scaleX, scaleY)

    # Calculate Enemy FOV points
    allEnemiesFov = []
    for enemy in levelData.Level.currentMap.grid_entities:
        if issubclass(type(enemy), entities.Enemy):
            enemyFovPoints = calculate_fov_polygon(enemy)
            enemyFovPoints = translate_to_map(enemyFovPoints, scaleX, scaleY)

            color = colors.ALMOST_BLACK
            if enemy.canSeePlayer:
                color = colors.RED
            allEnemiesFov.append((color, enemyFovPoints))

    # endregion

    # region Draw MiniMap

    # Draw Player FOV
    if len(playerFovPoints) > 2:
        pygame.draw.polygon(screen, colors.DARK_GRAY, playerFovPoints)

    # Draw Enemy FOV
    for c, points in allEnemiesFov:
        pygame.draw.polygon(screen, c, points)

    for enemy in levelData.Level.currentMap.grid_entities:
        if issubclass(type(enemy), entities.Enemy):
            pygame.draw.circle(screen, colors.RED, [int(
                enemy.py * scaleX), int(enemy.px * scaleY)], 2)
        if issubclass(type(enemy), entities.Collectible):
            if enemy.collected:
                pygame.draw.circle(screen, colors.YELLOW_WHITE, [int(
                    enemy.py * scaleX), int(enemy.px * scaleY)], 2)

    pygame.draw.circle(screen, colors.WHITE, [int(
        entity.py * scaleX), int(entity.px * scaleY)], 2)

    # Draw Map
    for x in range(levelData.Level.currentMap.level_width):
        for y in range(levelData.Level.currentMap.level_height):
            color = None
            if levelData.Level.currentMap.grid[x][y] != 0:
                color = colors.GRAY_VARIATION_3

            if color is not None:
                pygame.draw.rect(screen,
                                 color,
                                 [scaleX * y,
                                  scaleY * x,
                                  scaleX + 1,
                                  scaleY + 1])
    color = colors.DARK_GRAY
    for e in levelData.Level.currentMap.grid_entities:
        if issubclass(type(e), entities.Gate):
            if not e.open:
                pygame.draw.rect(screen,
                                    color,
                                    [scaleX * math.floor(e.py),
                                    scaleY * math.floor(e.px),
                                    scaleX + 1,
                                    scaleY + 1])
       
    # endregion

def draw_map_preview(screen, map):
    screen.fill(colors.GRAY)
    scaleX = screen.get_width()/map.level_width
    scaleY = screen.get_height()/map.level_height
    for x in range(map.level_width):
        for y in range(map.level_height):
            color = None
            if map.grid[x][y] != 0:
                color = colors.GRAY_VARIATION_3

            if color is not None:
                pygame.draw.rect(screen,
                                 color,
                                 [scaleX * y,
                                  scaleY * x,
                                  scaleX + 1,
                                  scaleY + 1])
    color = colors.DARK_GRAY
    for e in map.grid_entities:
        if issubclass(type(e), entities.Gate):
            pygame.draw.rect(screen,
                                 color,
                                 [scaleX * math.floor(e.py),
                                  scaleY * math.floor(e.px),
                                  scaleX + 1,
                                  scaleY + 1])
        if issubclass(type(e), entities.Player):
            pygame.draw.rect(screen,
                                 colors.WHITE,
                                 [scaleX * math.floor(e.py),
                                  scaleY * math.floor(e.px),
                                  scaleX + 1,
                                  scaleY + 1])

def generate_hud_surfaces(hud_surface):
    import ui
    hud_cell_surfaces = []
    cell_height = hud_surface.get_height() - renderer.VIEWPORT_Y_OFFSET//2
    cell_width = (hud_surface.get_width() -
                  (HUD_CELL_OFFSET + 1) * HUD_NUM_OF_CELLS)
    cell_width /= HUD_NUM_OF_CELLS
    surf_count = 0
    while surf_count < HUD_NUM_OF_CELLS:
        surf_count += 1
        window = ui.HudButton(
            cell_width, cell_height)
        window.fill(colors.NAVY_BLUE)
        hud_cell_surfaces.append(window)
    return hud_cell_surfaces


def generate_hud_viewport():
    hud_width = renderer.SCREEN_WIDTH - renderer.VIEWPORT_X_OFFSET * 2
    hud_height = (renderer.SCREEN_HEIGHT -
                  renderer.VIEWPORT_HEIGHT -
                  renderer.VIEWPORT_Y_OFFSET * 2)

    hud_viewport = pygame.Surface([hud_width, hud_height]).convert()
    hud_viewport.fill(colors.BLUE)
    return hud_viewport

