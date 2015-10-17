#!/usr/bin/env python3
import pygame
from components.mobileplatform import MobilePlatform


class Help(MobilePlatform):

    def __init__(self, centerx, lowy, *groups, game, Text):
        self.font = pygame.font.SysFont(None, 32)
        self.img = self.font.render(Text, True, (255, 0, 0),
                                    (0, 0, 0))
        self.size = self.img.get_rect()
        self.x= centerx - (self.size.width/2)
        self.y= lowy - (self.size.height*game.gravity)
        MobilePlatform.__init__(self, self.x, self.y, *groups, game=game,
                                surface=self.img)
        game.helptxts.add(self)
        self.age = 300

    def update(self, dt, game):
        self.age -= 1
        if self.age == 0:
            self.kill()
            game.setHelpFlag(False)
