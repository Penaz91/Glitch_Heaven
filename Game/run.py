#!/usr/bin/env python3
import pygame
from game import Game
import configparser
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("game.conf")
    screensize = (int(config["Screen"]["screenwidth"]),
                  int(config["Screen"]["screenheight"]))
    fullscreen = config.getboolean("Screen", "fullscreen")
    flags = None
    if fullscreen:
        flags = pygame.FULLSCREEN | pygame.HWACCEL
    else:
        flags = 0
    pygame.init()
    screen = pygame.display.set_mode(screensize, flags)
    Game().main(screen)
