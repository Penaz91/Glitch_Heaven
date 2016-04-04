# Custom-timing Spritesheet Animation Library
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
from libs.spritesheetanimation import SpritesheetAnimation
from itertools import cycle


class TimedSpritesheetAnimation(SpritesheetAnimation):
    def __init__(self, frametime, spritesheetpath, squaresize=32):
        super().__init__(frametime, spritesheetpath, squaresize)
        self.frametime = cycle(frametime)
        self.currenttiming = next(self.frametime)
        self.index = 0

    def next(self, dt):
        self.time += dt
        if self.time >= self.currenttiming[0]:
            self.currentframe = next(self.frames)
            self.time = 0
            self.index += 1
            if self.index == self.currenttiming[1]:
                self.currenttiming = next(self.frametime)
                self.index = 0
        return self.currentframe
