#!/usr/bin/env python3
import pygame
from components.mobileplatform import MobilePlatform
import os


class DeadBody(MobilePlatform):
    size = (32, 32)
    playerspeed = 300

    def __init__(self, x, y, *groups, game):
        self.img = pygame.image.load(os.path.join("resources",
                                                  "sprites",
                                                  "player.png"))
        MobilePlatform.__init__(self, x, y, *groups, game=game,
                                surface=self.img)

    def update(self, dt, game):
        pass
