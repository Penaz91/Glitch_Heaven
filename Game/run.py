#!/usr/bin/env python3
# Bootstrapper
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
# from game import Game
from mainmenu import menu
import configparser
if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read("game.conf")
    screensize = (int(config["Screen"]["screenwidth"]),
                  int(config["Screen"]["screenheight"]))
    fullscreen = config.getboolean("Screen", "fullscreen")
    doublebuffer = config.getboolean("Screen", "doublebuffer")
    flags = None
    keys = dict(config["Controls"])
    for key in keys:
        keys[key] = int(keys[key])
    if fullscreen:
        if doublebuffer:
            flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        else:
            flags = pygame.FULLSCREEN | pygame.HWSURFACE
    else:
        flags = 0
    pygame.mixer.pre_init(44100, 16, 2, 4096)
    pygame.init()
    screen = pygame.display.set_mode(screensize, flags)
    menu().main(screen, keys)
    # Game().main(screen, keys)
