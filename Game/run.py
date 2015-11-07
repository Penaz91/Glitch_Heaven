#!/usr/bin/env python3
# Bootstrapper
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
from mainmenu import menu
import configparser

if __name__ == "__main__":
    # Reads the game configuration
    # v-------------------------------------------------------------------v
    config = configparser.ConfigParser()
    config.read("game.conf")
    screensize = (int(config["Video"]["screenwidth"]),
                  int(config["Video"]["screenheight"]))
    fullscreen = config.getboolean("Video", "fullscreen")
    doublebuffer = config.getboolean("Video", "doublebuffer")
    flags = None
    # Reads the control keys
    # v-------------------------------v
    keys = dict(config["Controls"])
    for key in keys:
        keys[key] = int(keys[key])
    # ^-------------------------------^
    # 
    # Sets the screen flags
    # v-------------------------------v
    if fullscreen:
        if doublebuffer:
            flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        else:
            flags = pygame.FULLSCREEN | pygame.HWSURFACE
    else:
        flags = 0
    # ^-------------------------------^
    # ^-------------------------------------------------------------------^
    pygame.mixer.pre_init(48000, 16, 2, 4096)
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(screensize, flags)
    menu().main(screen, keys, config)
