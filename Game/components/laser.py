# Laser component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from libs.lasergen import generate


class Laser(pygame.sprite.Sprite):

    def __init__(self, size, vertical, time, number, location, *groups):
        super(Laser, self).__init__(*groups)
        self.activeimage = generate(size, vertical)
        self.inactiveimage = pygame.surface.Surface((0, 0))
        self.image = self.activeimage
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location
        self.id = number
        self.time = 0.
        self.triggertime = time
        self.active = time == 0
        self.update = self.update_timed
        if time == 0:
            self.update = self.update_static

    def update_timed(self, dt, game):
        self.time += dt
        if (self.time >= self.triggertime):
            self.time = 0
            self.active = not self.active
        if self.active:
            self.image = self.activeimage
        else:
            self.image = self.inactiveimage

    def update_static(self, dt, game):
        pass
