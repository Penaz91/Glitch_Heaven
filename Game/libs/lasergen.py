# Laser Generator Library
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>

import pygame
from os.path import join as pjoin


def generate(size, vertical=False, image=None):
    if image is None:
        graphics = pygame.image.load(pjoin("laser.png")).convert_alpha()
    else:
        graphics = image
    if vertical:
        plat = pygame.surface.Surface((32, size), pygame.SRCALPHA, 32)
        graphics = pygame.transform.rotate(graphics, 90)
        for i in range(0, size, 32):
            plat.blit(graphics, (0, i))
    else:
        plat = pygame.surface.Surface((size, 32), pygame.SRCALPHA, 32)
        for i in range(0, size, 32):
            plat.blit(graphics, (i, 0))
    return plat.convert_alpha()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    platform = generate(160, True)
    while True:
        screen.blit(platform, (50, 50))
        pygame.display.update()
