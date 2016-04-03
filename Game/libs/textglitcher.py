# Glitched Text Real-Time builder library
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from random import randint, choice


def makeGlitched(text, font):
    purple = font.render(text,
                         False,
                         (236, 0, 200)).convert_alpha()
    green = font.render(text,
                        False,
                        (0, 236, 5)).convert_alpha()
    white = font.render(text,
                        False,
                        (255, 255, 255)).convert_alpha()
    entire = pygame.surface.Surface((purple.get_width() + 5,
                                    purple.get_height()),
                                    pygame.SRCALPHA,
                                    32)
    entire.blit(purple, (0, 0))
    entire.blit(green, (4, 0))
    entire.blit(white, (2, 0))
    return entire


def makeMoreGlitched(text, chanceperc):
    chance = randint(0, 100)
    txt = text
    d = list(txt)
    symlist = ["@", "#", "!", "%", "&", ")", "(", "^"]
    if chance <= chanceperc:
        rnd = randint(1, len(text)//2)
        for i in range(rnd):
            rnd2 = randint(0, len(text)-1)
            d[rnd2] = choice(symlist)
    return "".join(d)
