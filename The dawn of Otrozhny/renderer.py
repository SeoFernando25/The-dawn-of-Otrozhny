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
import cy_renderer

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









def generate_distance_table(entity):
    
    cy_renderer.generate_distance_table(entity)
  

def _calculate_entities_in_sight(entity):
    cy_renderer._calculate_entities_in_sight(entity)

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
    cy_renderer.render_walls(screen, entity)
    # Draw Weapon
    # todo  <= I won't. Tts a stealth game!




def draw_map_preview(screen, map):
    screen.fill(colors.GRAY)
    scale_x = screen.get_width()/map.level_width
    scale_y = screen.get_height()/map.level_height
    for x in range(map.level_width):
        for y in range(map.level_height):
            color = None
            if map.grid[x][y] != 0:
                color = colors.GRAY_VARIATION_3

            if color is not None:
                pygame.draw.rect(screen,
                                 color,
                                 [scale_x * y,
                                  scale_y * x,
                                  scale_x + 1,
                                  scale_y + 1])
    color = colors.DARK_GRAY
    for e in map.grid_entities:
        if issubclass(type(e), entities.Gate):
            pygame.draw.rect(screen,
                             color,
                             [scale_x * math.floor(e.py),
                              scale_y * math.floor(e.px),
                              scale_x + 1,
                              scale_y + 1])
        if issubclass(type(e), entities.Player):
            pygame.draw.rect(screen,
                             colors.WHITE,
                             [scale_x * math.floor(e.py),
                              scale_y * math.floor(e.px),
                              scale_x + 1,
                              scale_y + 1])


def generate_hud_surfaces(hud_surface):
    from ui import HudButton
    hud_cell_surfaces = []
    cell_height = hud_surface.get_height() - renderer.VIEWPORT_Y_OFFSET//2
    cell_width = (hud_surface.get_width() -
                  (HUD_CELL_OFFSET + 1) * HUD_NUM_OF_CELLS)
    cell_width /= HUD_NUM_OF_CELLS
    surf_count = 0
    while surf_count < HUD_NUM_OF_CELLS:
        surf_count += 1
        window = HudButton(
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
