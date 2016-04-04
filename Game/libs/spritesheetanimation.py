# Constant-timing Spritesheet Animation Library
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from itertools import cycle
from random import choice as RChoice


class SpritesheetAnimation(object):
    def __init__(self, frametime, spritesheetpath, squaresize=32):
        super()
        self.frametime = frametime
        self.squaresize = squaresize
        self.spritesheet = pygame.image.load(spritesheetpath).convert_alpha()
        self.framesframework = [self.spritesheet.subsurface(
            pygame.rect.Rect(i, 0, self.squaresize, self.squaresize))
                for i in range(
                    0, self.spritesheet.get_size()[0], self.squaresize)]
        self.frames = cycle(self.framesframework)
        self.time = 0
        self.currentframe = next(self.frames)

    def next(self, dt):
        self.time += dt
        if self.time >= self.frametime:
            self.time = 0
            self.currentframe = next(self.frames)
        return self.currentframe

    def rand_next(self, dt):
        self.time += dt
        if self.time >= self.frametime:
            self.time = 0
            self.currentframe = RChoice(self.framesframework)
        return self.currentframe
