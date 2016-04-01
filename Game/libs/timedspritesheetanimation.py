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

"""#------TESTING AREA----------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    ani = TimedSpritesheetAnimation([(1, 1), (0.25, 7)],
                               pathj("Sprites.png"))
    clock = pygame.time.Clock()
    while 1:
        dt = clock.tick(30) / 1000.
        screen.fill((0, 0, 0))
        screen.blit(ani.next(dt), (32, 32))
        pygame.display.update()
"""
