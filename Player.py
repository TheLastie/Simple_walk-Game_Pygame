import math

import pygame as pg
from Main import circle_animation

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GRAY = 128, 128, 128
LIGHT_GRAY = 200, 200, 200
DARK_GRAY = 90, 90, 90
GREEN = 0, 255, 0
RED = 255, 0, 0
BLUE = 0, 0, 255


class Player(pg.sprite.Sprite):
    class Hit(pg.sprite.Sprite):
        def __init__(self, hits, coordinates, max_coordinates, screen, clock, mouse_coordinates):
            pg.sprite.Sprite.__init__(self)
            self.images = circle_animation("animations/player", "hit_1")
            self.lenght = 500
            self.mouse_coordinates = mouse_coordinates[0] * (max_coordinates[0] / screen[0]), \
                                     mouse_coordinates[1] * (max_coordinates[0] / screen[0])
            self.cord = [int(coordinates[0]), int(coordinates[1])]
            self.direction = 0

            if self.mouse_coordinates[0] > self.cord[0]:

                if self.mouse_coordinates[1] > self.cord[1]:
                    self.direction = "rightbottom"
                    self.yg = 90 - (math.atan(abs(self.mouse_coordinates[1] - self.cord[1]) / abs(
                        self.mouse_coordinates[0] - self.cord[0])) * (180 / math.pi))
                    self.yg1 = 90 / 180 * math.pi - (math.atan(abs(self.mouse_coordinates[1] - self.cord[1]) / abs(
                        self.mouse_coordinates[0] - self.cord[0])))
                    self.cord[0] = coordinates[0] + self.lenght * abs(math.sin(self.yg1))
                    self.cord[1] = coordinates[1] + self.lenght * abs(math.cos(self.yg1))

                if self.mouse_coordinates[1] < self.cord[1]:
                    self.direction = "righttop"
                    self.yg = 90 + (math.atan(abs(self.mouse_coordinates[1] - self.cord[1]) / abs(
                        self.mouse_coordinates[0] - self.cord[0])) * (180 / math.pi))
                    self.yg1 = 90 / 180 * math.pi - (math.atan(abs(self.mouse_coordinates[1] - self.cord[1]) / abs(
                        self.mouse_coordinates[0] - self.cord[0])))
                    self.cord[0] = coordinates[0] + self.lenght * abs(math.sin(self.yg1))
                    self.cord[1] = coordinates[1] - self.lenght * abs(math.cos(self.yg1))

            elif self.mouse_coordinates[0] < self.cord[0]:

                if self.mouse_coordinates[1] > self.cord[1]:
                    self.direction = "leftbottom"
                    self.yg = 270 + (math.atan(abs(self.mouse_coordinates[1] - self.cord[1]) / abs(
                        self.mouse_coordinates[0] - self.cord[0]))) * (180 / math.pi)
                    self.yg1 = 90 / 180 * math.pi - (math.atan(abs(self.mouse_coordinates[1] - self.cord[1]) / abs(
                        self.mouse_coordinates[0] - self.cord[0])))
                    self.cord[0] = coordinates[0] - self.lenght * abs(math.sin(self.yg1))
                    self.cord[1] = coordinates[1] + self.lenght * abs(math.cos(self.yg1))

                if self.mouse_coordinates[1] < self.cord[1]:
                    self.direction = "lefttop"
                    self.yg = 270 - (math.atan(abs(self.mouse_coordinates[1] - self.cord[1]) / abs(
                        self.mouse_coordinates[0] - self.cord[0])) * (180 / math.pi))
                    self.yg1 = 90 / 180 * math.pi - (math.atan(abs(self.mouse_coordinates[1] - self.cord[1]) / abs(
                        self.mouse_coordinates[0] - self.cord[0])))
                    self.cord[0] = coordinates[0] - self.lenght * abs(math.sin(self.yg1))
                    self.cord[1] = coordinates[1] - self.lenght * abs(math.cos(self.yg1))

            self.image = pg.transform.rotate(self.images[0][0], self.yg)
            self.rect = self.image.get_rect()
            self.rect.centerx = self.cord[0] / (max_coordinates[0] / screen[0])
            self.rect.centery = self.cord[1] / (max_coordinates[0] / screen[0])
            self.clock = clock
            self.coordinates = self.cord
            self.max_coordinates = max_coordinates
            self.screen = screen
            self.hits = hits
            self.i = 0
            hits.add(self)
            self.last_player_cord = coordinates

        def update(self, clock, coordinates):
            self.image = pg.transform.rotate(self.images[0][int(self.i % (self.images[1] - 1))], self.yg)
            self.i += 0.5
            if self.i > self.images[1] - 1:
                self.kill()

            if self.direction == "rightbottom":
                self.cord[0] = coordinates[0] + self.lenght * abs(math.sin(self.yg1))
                self.cord[1] = coordinates[1] + self.lenght * abs(math.cos(self.yg1))

            if self.direction == "righttop":
                self.cord[0] = coordinates[0] + self.lenght * abs(math.sin(self.yg1))
                self.cord[1] = coordinates[1] - self.lenght * abs(math.cos(self.yg1))

            if self.direction == "leftbottom":
                self.cord[0] = coordinates[0] - self.lenght * abs(math.sin(self.yg1))
                self.cord[1] = coordinates[1] + self.lenght * abs(math.cos(self.yg1))

            if self.direction == "lefttop":
                self.cord[0] = coordinates[0] - self.lenght * abs(math.sin(self.yg1))
                self.cord[1] = coordinates[1] - self.lenght * abs(math.cos(self.yg1))

            self.rect.centerx = self.cord[0] / (self.max_coordinates[0] / self.screen[0])
            self.rect.centery = self.cord[1] / (self.max_coordinates[0] / self.screen[0])

    def __init__(self, players, sprites, coordinates, max_coordinates, screen, clock, borders):
        pg.sprite.Sprite.__init__(self)
        self.image = circle_animation("animations/player", "poses_stay")
        self.image.fill(LIGHT_GRAY)
        self.rect = self.image.get_rect()
        self.cord = [int(coordinates[0]), int(coordinates[1])]
        self.rect.centerx = self.cord[0] / (max_coordinates[0] / screen[0])
        self.rect.centery = self.cord[1] / (max_coordinates[0] / screen[0])
        self.run_right = circle_animation("animations/player", "run_right")
        self.run_left = circle_animation("animations/player", "run_left")
        self.run_down = circle_animation("animations/player", "run_down")
        self.stay = circle_animation("animations/player", "poses_stay")
        self.anim_dash_right = circle_animation("animations/player", "dash_right")
        self.anim_dash_left = circle_animation("animations/player", "dash_left")
        self.sprites = sprites
        self.hits = pg.sprite.Group()

        self.speed = int
        self.d_speed = int
        self.d_slow = int

        self.max_coordinates = max_coordinates
        self.screen = screen
        self.clock = clock
        self.border = borders
        self.last_dash = clock
        self.last_hit = clock
        self.d_left = 0
        self.d_up = 0
        self.d_right = 0
        self.d_down = 0
        self.dash = 0
        self.dash_on = False
        self.move = False
        self.last_cord = self.cord
        self.i = 0

        sprites.add(self)
        players.add(self)

    def update(self, clock):
        self.clock = clock
        try:
            if self.dash > 0:
                if self.d_left and self.cord[0] > self.border:
                    self.cord[0] -= self.dash
                    self.image = self.anim_dash_left

                if self.d_right and self.cord[0] < self.max_coordinates[0] - self.border:
                    self.cord[0] += self.dash
                    self.image = self.anim_dash_right

                if self.d_up and self.cord[1] > self.border:
                    self.cord[1] -= self.dash

                if self.d_down and self.cord[1] < self.max_coordinates[1] - self.border:
                    self.cord[1] += self.dash

                self.dash -= self.d_slow
                self.move = True
                if self.d_right or self.d_left or self.d_down or self.d_up:
                    self.dash_on = True
            else:
                self.dash = 0
                self.dash_on = False
                self.d_right = False
                self.d_left = False
                self.d_up = False
                self.d_down = False
        except:
            pass
        if self.last_cord == self.cord and not (self.dash != 0 and self.move):
            self.move = False
            self.image = self.stay
        self.rect.centerx = self.cord[0] / (self.max_coordinates[0] / self.screen[0])
        self.rect.centery = self.cord[1] / (self.max_coordinates[0] / self.screen[0])
        self.last_cord = self.cord
        self.hits.update(clock, self.cord)

    def move_hor(self, value):
        if abs(value) > 0.005:
            if self.cord[0] < self.max_coordinates[0] - self.border and value > 0:
                self.cord[0] += self.speed * value
                self.move = True

            if self.cord[0] > self.border and value < 0:
                self.cord[0] += self.speed * value
                self.move = True

    def move_ver(self, value):
        if abs(value) > 0.005:
            if self.cord[1] > self.border and value < 0:
                self.cord[1] += self.speed * value
                self.move = True

            if self.cord[1] < self.max_coordinates[1] - self.border and value > 0:
                self.cord[1] += self.speed * value
                self.move = True

    def move_anim(self, value0, value1):
        if abs(value0) > 0.005 or abs(value1) > 0.005:
            if value0 > 0 and abs(value0) > abs(value1):
                self.i = abs((self.i + 0.2) % (self.run_right[1] - 1))
                self.image = self.run_right[0][int(self.i)]

            if value0 < 0 and abs(value0) > abs(value1):
                self.i = abs((self.i + 0.2) % (self.run_left[1] - 1))
                self.image = self.run_left[0][int(self.i)]

            if value1 > 0 and abs(value1) > abs(value0):
                self.i = abs((self.i + 0.2) % (self.run_down[1] - 1))
                self.image = self.run_down[0][int(self.i)]

            if value1 < 0 and abs(value1) > abs(value0):
                self.i = abs((self.i + 0.2) % (self.run_down[1] - 1))
                self.image = self.run_down[0][int(self.i)]
        else:
            self.image = self.stay

    def dash_right(self):
        self.dash_on = True
        self.dash = self.d_speed
        self.d_right = True
        self.image = self.anim_dash_right

    def dash_left(self):
        self.dash_on = True
        self.dash = self.d_speed
        self.d_left = True
        self.image = self.anim_dash_left

    def dash_up(self):
        self.dash_on = True
        self.dash = self.d_speed
        self.d_up = True

    def dash_down(self):
        self.dash_on = True
        self.dash = self.d_speed
        self.d_down = True

    def hit(self, mouse_coordinates):
        if self.clock - self.last_hit > 0:
            self.Hit(self.hits, self.cord, self.max_coordinates, self.screen, self.clock, mouse_coordinates)
            self.last_hit = self.clock

