# CheckPoint Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.triggerableItem import triggerableItem
from os.path import join as pjoin
import pygame


class checkPoint(triggerableItem):
    activerect = pygame.rect.Rect(0,0,32,32)
    inactiverect = pygame.rect.Rect(32,0,32,32)
    def __init__(self, location, *groups):
        self.chkimage = pygame.image.load(pjoin("resources",
                                                "sprites",
                                                "CheckPoint.png")).convert_alpha()
        self.inactive = self.chkimage.subsurface(self.inactiverect)
        self.active = self.chkimage.subsurface(self.activerect)
        self.used = False
        super(checkPoint, self).__init__(location, None, self.inactive,
                                              self.active, *groups)
