# Button Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.triggerableItem import triggerableItem
from os.path import join as pjoin
import pygame


class button(triggerableItem):
    activerect = pygame.rect.Rect(0,0,32,32)
    inactiverect = pygame.rect.Rect(32,0,32,32)
    def __init__(self, location, identifier, pwd, *groups):
        self.btnimage = pygame.image.load(pjoin("resources",
                                                "sprites",
                                                "Trigger.png")).convert_alpha()
        self.inactive = self.btnimage.subsurface(self.inactiverect)
        self.active = self.btnimage.subsurface(self.activerect)
        super(button, self).__init__(location, pwd, self.inactive,
                                              self.active, *groups)
        self.id = identifier
