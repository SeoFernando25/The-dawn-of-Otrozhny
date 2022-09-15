# Script used mainly to draw "otherEffects.py" on the screen
# eg: main menu's Sierpinski triangle
import pygame
import colors
import mathHelpers
import random


# The concept for this class was taken from
# this numberphile video
# https://www.youtube.com/watch?v=kbKtFN71Lfs
class ChaosObject(pygame.Surface):
    def __init__(self, center, size, n_sides):
        super().__init__((size, size))
        self.set_colorkey(colors.BLACK)
        self.points = mathHelpers.points_from_polygon_sides(
            n_sides, size/2, adjusted=True)
        self.color = colors.WHITE
        self.size = size
        self.center = center
        self.n_of_itterations = 0
        self.drawn_points = []
        self.current_point = self.points[0]
        self.drawn_points.append(self.current_point)
        self.updates_before_draw = 0

    def draw(self, screen):
        for x in range(self.updates_before_draw):
            point = self.drawn_points[len(self.drawn_points) - 1 - x]
            pygame.draw.circle(self, self.color, tuple(
                [int(x) for x in point]), 1)
        self.updates_before_draw = 0
        screen.blit(
            self, (self.center[0] - self.size//2, self.center[1] - self.size//2))

    def update(self):
        import random
        # I add updates before draw because I dont want to have to draw all
        # points from zero in case I have 235252 points, just the last
        # 62 ones :)
        self.updates_before_draw += 1
        self.n_of_itterations += 1
        rand_pos = random.randint(0, len(self.points)-1)
        newPx = mathHelpers.lerp(
            self.current_point[0], self.points[rand_pos][0], 0.5)
        newPy = mathHelpers.lerp(
            self.current_point[1], self.points[rand_pos][1], 0.5)
        self.current_point = (newPx, newPy)
        self.drawn_points.append(self.current_point)

# The same as the last class but the update function changes
# See: https://en.wikipedia.org/wiki/Chaos_game#/media/File:Chaos_Game_pentagon-EH-1.png


class ChaosSnowFlake(ChaosObject):
    def __init__(self, center, size):
        super().__init__(center, size, 5)
        self.previous = None

    def update(self):
        import random
        rand_pos = random.randint(0, len(self.points)-1)
        while rand_pos == self.previous:
            rand_pos = random.randint(0, len(self.points)-1)

        newPx = mathHelpers.lerp(
            self.current_point[0], self.points[rand_pos][0], 0.5)
        newPy = mathHelpers.lerp(
            self.current_point[1], self.points[rand_pos][1], 0.5)
        self.current_point = (newPx, newPy)
        self.drawn_points.append(self.current_point)
        self.previous = rand_pos


class StarField(pygame.Surface):
    class Star():
        def __init__(self, parent_width, parent_height):
            spread = 3
            self.x = random.randint(-parent_width//spread,
                                    parent_width//spread)
            self.y = random.randint(-parent_height //
                                    spread, parent_height//spread)
            self.z = random.randint(1, parent_width)
            self.lastZ = self.z

            self.screenX = 0
            self.screenY = 0

            self.screenLastX = 0
            self.screenLastY = 0

    def __init__(self, size):
        super().__init__(size)

        self.speed = random.randint(1, 5)
        self.width = self.get_width()
        self.height = self.get_height()

        self.stars = []
        for x in range(250):
            self.stars.append(StarField.Star(size[0], size[1]))

    def update(self, dt):

        for star in self.stars:

            if (star.screenX < -5
                    or star.screenX > self.width + 5
                    or star.screenY < -5
                    or star.screenY > self.height + 5):
                star.z = self.width

            star.lastZ = star.z
            star.z -= dt * 10 * self.speed

            if star.z == 0:
                star.z = -0.1

            star.screenX = mathHelpers.translate(
                star.x/star.z, 0, 1, 0, self.width)
            star.screenY = mathHelpers.translate(
                star.y/star.z, 0, 1, 0, self.height)
            star.screenX += self.width//2
            star.screenY += self.height//2

            star.screenLastX = mathHelpers.translate(
                star.x/star.lastZ, 0, 1, 0, self.width)
            star.screenLastY = mathHelpers.translate(
                star.y/star.lastZ, 0, 1, 0, self.height)
            star.screenLastX += self.width//2
            star.screenLastY += self.height//2

    def draw(self):
        self.fill((0, 0, 0))
        for star in self.stars:
            starSize = mathHelpers.translate(star.z, self.width, 0, 1, 4)
            if starSize > 8:
                star.z = self.width
            starSize = int(starSize)

            pygame.draw.line(self, (255, 255, 255), (star.screenX, star.screenY),
                             (star.screenLastX, star.screenLastY), starSize)

    def change_speed(self):
        import random
        num = random.randint(1, 10)
        while abs(self.speed - num) < 3:
            num = random.randint(1, 10)
        self.speed = num


# Just a demo
if __name__ == "__main__":
    import pygame

    TICK = 60
    pygame.init()

    SCREEN_WIDTH = 640
    SCREEN_HEIGHT = 480

    SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

    clock = pygame.time.Clock()
    done = False

    SCREEN = pygame.display.set_mode(SCREEN_SIZE)

    star_field = StarField(SCREEN_SIZE)
    star_field.draw()

    while not done:
        deltaTime = clock.get_time() / 1000
        events = pygame.event.get()
        star_field.update(deltaTime)
        SCREEN.fill((0, 0, 0))
        star_field.draw()
        SCREEN.blit(star_field, (0, 0))

        pygame.display.flip()
        clock.tick(TICK)
