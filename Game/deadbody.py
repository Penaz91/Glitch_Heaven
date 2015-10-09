#!/usr/bin/env python3
import pygame
import os


class DeadBody(pygame.sprite.Sprite):
    size = (32, 32)
    playerspeed = 300

    def __init__(self, x, y, *groups):
        super(DeadBody, self).__init__(*groups)
        self.image = pygame.image.load(os.path.join("resources",
                                                    "sprites",
                                                    "player.png"))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, dt, game):
        pass
