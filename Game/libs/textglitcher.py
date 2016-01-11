# Glitched Text Real-Time builder library
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame


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
