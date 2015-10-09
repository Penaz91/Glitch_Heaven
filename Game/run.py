#!/usr/bin/env python3
import pygame
from game import Game
if __name__ == "__main__":
    pygame.init()
    screensize = (800, 600)
    screen = pygame.display.set_mode(screensize)
    Game().main(screen)
