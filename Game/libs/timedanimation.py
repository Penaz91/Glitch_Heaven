# Timed Animation/Frame Generator Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
from itertools import cycle
import os
from os.path import join as pjoin


class TimedAnimation(object):
    def __init__(self, timings, framespath):
        x =[(os.path.join(framespath, f))
               for f in os.listdir(framespath)
                  if os.path.isfile(os.path.join(framespath, f))]
        self.frames = cycle([pygame.image.load(y).convert_alpha() for y in sorted(x)])
        self.timings = cycle(timings)
        self.currenttiming = next(self.timings)
        self.currentframe = next(self.frames)
        self.index = 0
        self.dt = 0;
        
    def next(self, dt):
        self.dt += dt
        if self.dt >= self.currenttiming[0]:
            self.currentframe = next(self.frames)
            self.dt = 0
            self.index += 1
            if self.index == self.currenttiming[1]:
                self.currenttiming = next(self.timings)
                self.index = 0
        return self.currentframe
        
"""if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()
    ani = TimedAnimation([(1, 1), (0.2, 18), (1, 1), (0.2, 4)],
                         pjoin("AnimatedTitle"))
    while 1:
        screen.fill((0, 0, 0))
        dt = clock.tick(30) / 1000.
        screen.blit(ani.next(dt), (10, 10))
        pygame.display.update()"""
