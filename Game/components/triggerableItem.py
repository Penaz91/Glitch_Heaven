# Triggerable Item Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from os.path import join as pjoin


class triggerableItem(pygame.sprite.Sprite):
    def __init__(self, location, pwd, inactive, active, *groups):
        super(triggerableItem, self).__init__(*groups)
        self.inactive = inactive
        self.active = active
        self.image = self.inactive
        self.used = False
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = location[0], location[1]
        self.password = pwd

    def activate(self):
        if not self.used:
            self.image = self.active
            self.used = True

    def deactivate(self):
        if self.used:
            self.image = self.inactive
            self.used = False
