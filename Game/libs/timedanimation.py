# Timed Animation/Frame Generator Library
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from itertools import cycle
from os.path import join as pjoin
from os import listdir
from os.path import isfile


class TimedAnimation(object):
    def __init__(self, timings, framespath):
        x = [(pjoin(framespath, f))
             for f in listdir(framespath)
             if isfile(pjoin(framespath, f))]
        self.frames = cycle([pygame.image.load(y).convert_alpha()
                             for y in sorted(x)])
        self.timings = cycle(timings)
        self.currenttiming = next(self.timings)
        self.currentframe = next(self.frames)
        self.index = 0
        self.dt = 0

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
