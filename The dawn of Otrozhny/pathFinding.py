import pygame
import levelData

import renderer
import colors
import math
import mathHelpers

# See: http://www.sfu.ca/~arashr/warren.pdf


def go_to(start, target):
    openSet = []
    closedSet = []

    cameFrom = {}
    gScore = {}
    gScore[start] = 0
    fScore = {}
    fScore[start] = get_heuristic(start, target)
    openSet.append(start)

    while len(openSet) > 0:
        winner = openSet[0]
        for coord in openSet:
            if fScore[coord] < fScore[winner]:
                winner = coord

        current = winner
        if current == target:
            found = True
            return reconstruct_path(cameFrom, current)
        else:
            openSet.remove(current)
            closedSet.append(current)

            for neighbor in get_neighbors(current, levelData.Level.currentMap.grid):
                if neighbor in closedSet:
                    continue

                tentative_gScore = gScore[current] + 1
                if neighbor in openSet:
                    if tentative_gScore < gScore[neighbor]:
                        gScore[neighbor] = tentative_gScore
                else:
                    gScore[neighbor] = tentative_gScore
                    openSet.append(neighbor)

                cameFrom[neighbor] = current
                gScore[neighbor] = tentative_gScore
                fScore[neighbor] = gScore[neighbor] + \
                    get_heuristic(neighbor, target)

# Get NSEW neighboors if possible


def get_neighbors(coord, grid):
    map_w = len(grid[0])
    map_h = len(grid)
    coord = (int(coord[0]), int(coord[1]))
    if 0 < coord[0] - 1 < map_w:
        if grid[coord[0] - 1][coord[1]] == 0:
            yield (coord[0] - 1, coord[1])
    if 0 < coord[0] + 1 < map_w:
        if grid[coord[0] + 1][coord[1]] == 0:
            yield (coord[0] + 1, coord[1])

    if 0 < coord[1] + 1 < map_h:
        if grid[coord[0]][coord[1] + 1] == 0:
            yield (coord[0], coord[1] + 1)
    if 0 < coord[1] - 1 < map_h:
        if grid[coord[0]][coord[1] - 1] == 0:
            yield (coord[0], coord[1] - 1)


def get_heuristic(coord, end):
    dx = abs(coord[0] - end[0])
    dy = abs(coord[1] - end[1])
    return dx + dy


def reconstruct_path(cameFrom, current):
    result = [current]
    while current in cameFrom.keys():
        current = cameFrom[current]
        result.append(current)
    result = list(reversed(result))
    return result


if __name__ == "__main__":
    print("Pathfinding Example")
    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480

    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    SCREEN = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()
    done = False

    start = (2, 2)
    target = (14, 14)

    cached_result = go_to(start, target)

    temp_result = cached_result.copy()
    temp_result_temp = temp_result.copy()
    w = SCREEN_WIDTH / len(levelData.worldMap[0])
    h = SCREEN_HEIGHT / len(levelData.worldMap)

    while not done:
        deltaTime = clock.get_time() / 1000
        fps = clock.get_fps()
        mouse = pygame.mouse.get_pos()
        events = pygame.event.get()
        kb = pygame.key.get_pressed()
        for event in events:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                start = (int(mouse[0]//w), int(mouse[1]//h))
                cached_result = go_to(start, target)
                temp_result = cached_result.copy()
                temp_result_temp = temp_result.copy()

        if len(temp_result) > 0:
            nextStep = temp_result[0]
            newX = mathHelpers.lerp(start[0], nextStep[0], deltaTime * 10)
            newY = mathHelpers.lerp(start[1], nextStep[1], deltaTime * 10)
            if (round(newX), round(newY)) == nextStep:
                temp_result.pop(0)
            start = (newX, newY)
        else:
            temp_result = temp_result_temp.copy()
            start = temp_result_temp[0]

        SCREEN.fill(colors.WHITE)

        for x in range(len(levelData.worldMap[0])):
            for y in range(len(levelData.worldMap)):

                color_flag = levelData.worldMap[x][y]

                if color_flag == 0:
                    wall_color = colors.WHITE
                else:
                    wall_color = colors.BLACK

                pygame.draw.rect(SCREEN, wall_color, [(x*w), (y*h), w-1, h-1])

        for x, y in cached_result:
            pygame.draw.rect(SCREEN, colors.GREEN, [
                             int(x*w), int(y*h), w-1, h-1])

        pygame.draw.circle(SCREEN, colors.BLUE, [int(
            start[0] * w + w/2), int(start[1] * h + h/2)], 10)
        pygame.draw.circle(SCREEN, colors.RED, [int(
            target[0] * w + (w/2)), int(target[1] * h + (h/2))], 10)

        pygame.display.update()
        clock.tick(60)
