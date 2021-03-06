# Platform Generator Library
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>

import pygame
from os.path import join as pjoin


def generate(size, plattype, image=None):
    if image is None:
        graphics = pygame.image.load(pjoin("resources",
                                           "tiles",
                                           "Plats.png")).convert_alpha()
    else:
        graphics = image
    lcorner = (0, plattype, 32, 32)
    center = (32, plattype, 32, 32)
    rcorner = (64, plattype, 32, 32)
    loner = (96, plattype, 32, 32)
    plat = pygame.surface.Surface((32*size, 32), pygame.SRCALPHA, 32)
    if size == 1:
        plat.blit(graphics, (0, 0), loner)
    else:
        centrals = size - 2
        plat.blit(graphics, (0, 0), lcorner)
        for i in range(centrals):
            i += 1
            plat.blit(graphics, (32*i, 0), center)
        plat.blit(graphics, (32*(size-1), 0), rcorner)
    return plat.convert_alpha()
