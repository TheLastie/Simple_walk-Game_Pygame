import math
import pygame as pg
import random
import os

from ctypes import windll


def circle_animation(folder, name):
    name_folder = name.split("_")
    anim_folder = folder
    for i in name_folder:
        anim_folder += '/' + i
    anim_folder += '/'
    number_of_slides = len(os.listdir(anim_folder))
    if number_of_slides == 1:
        slides = pg.image.load('{0}{1}.png'.format(anim_folder, name))
        return slides
    else:
        slides = []
        for i in range(1, number_of_slides):
            slides.append(pg.image.load('{0}{1} {2}.png'.format(anim_folder, name, i)))
        return slides, number_of_slides


def main():
    from Player import Player
    from Enemy import Enemy_1

    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    GRAY = 128, 128, 128
    LIGHT_GRAY = 200, 200, 200
    DARK_GRAY = 90, 90, 90
    GREEN = 0, 255, 0
    RED = 255, 0, 0
    BLUE = 0, 0, 255
    pg.init()
    pg.joystick.init()

    class Main:
        def __init__(self):
            self.w_HEIGHT = 10800
            self.w_WIDTH = 10800
            self.screen = (windll.user32.GetSystemMetrics(1) - 66, windll.user32.GetSystemMetrics(1) - 66)
            self.FPS = 60
            self.window = pg.display.set_mode((self.screen[0], self.screen[1]))
            self.running = True
            self.clock = pg.time.Clock()
            self.sprites = pg.sprite.Group()
            self.players = pg.sprite.Group()
            clock = 0
            self.border = 1000
            self.player = Player(self.players, self.sprites, (2000, 5000), (self.w_WIDTH, self.w_HEIGHT),
                                 self.screen, clock, self.border)
            self.hits = self.player.hits
            self.player.speed = 40
            self.player.d_speed = 280
            self.player.d_slow = 40
            self.i = 0
            self.joysticks = [pg.joystick.Joystick(x) for x in range(pg.joystick.get_count())]

        def main(self):
            clock = 0
            while self.running:
                clock += 1
                keystate = pg.key.get_pressed()
                self.clock.tick(self.FPS)
                self.sprites.update(clock)
                self.window.fill(BLACK)

                for event in pg.event.get():

                    if event.type == pg.QUIT:
                        self.running = False

                    if keystate[pg.K_ESCAPE]:
                        self.running = False
                        pg.display.quit()

                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_SPACE:
                            if clock - self.player.last_dash >= 50:

                                if keystate[pg.K_LEFT] or keystate[pg.K_a]:
                                    self.player.dash_left()
                                    self.player.last_dash = clock

                                if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
                                    self.player.dash_right()
                                    self.player.last_dash = clock

                                if keystate[pg.K_UP] or keystate[pg.K_w]:
                                    self.player.dash_up()
                                    self.player.last_dash = clock

                                if keystate[pg.K_DOWN] or keystate[pg.K_s]:
                                    self.player.dash_down()
                                    self.player.last_dash = clock
                    if event.type == pg.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            self.player.hit(event.pos)
                if len(self.joysticks) > 0:
                    self.player.move_hor(self.joysticks[0].get_axis(0))
                    self.player.move_ver(self.joysticks[0].get_axis(1))
                    self.player.move_anim(self.joysticks[0].get_axis(0), self.joysticks[0].get_axis(1))

                if not ((keystate[pg.K_LEFT] or keystate[pg.K_a]) and (keystate[pg.K_RIGHT or keystate[pg.K_d]])):
                    if keystate[pg.K_LEFT] or keystate[pg.K_a]:
                        if not self.player.dash_on:
                            self.i = abs((self.i + 0.15) % (self.player.run_left[1] - 1))
                            self.player.move_hor(-1)
                            self.player.image = self.player.run_left[0][int(self.i)]

                    if keystate[pg.K_RIGHT] or keystate[pg.K_d]:
                        if not self.player.dash_on:
                            self.i = abs((self.i + 0.15) % (self.player.run_right[1] - 1))
                            self.player.move_hor(1)
                            self.player.image = self.player.run_right[0][int(self.i)]

                if not ((keystate[pg.K_DOWN] or keystate[pg.K_s]) and (keystate[pg.K_UP] or keystate[pg.K_w])):
                    if keystate[pg.K_UP] or keystate[pg.K_w]:
                        if not self.player.dash_on:
                            self.i = abs((self.i + 0.15) % (self.player.run_down[1] - 1))
                            self.player.move_ver(-1)
                            self.player.image = self.player.run_down[0][int(self.i)]

                    if keystate[pg.K_DOWN] or keystate[pg.K_s]:
                        if not self.player.dash_on:
                            self.i = abs((self.i + 0.15) % (self.player.run_down[1] - 1))
                            self.player.move_ver(1)
                            self.player.image = self.player.run_down[0][int(self.i)]

                self.sprites.draw(self.window)
                self.player.hits.draw(self.window)
                self.players.draw(self.window)
                pg.display.flip()

    Main().main()


if __name__ == "__main__":
    main()
