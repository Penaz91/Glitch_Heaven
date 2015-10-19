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
    doublebuffer = config.getboolean("Screen", "doublebuffer")
    flags = None
    keys=dict(config["Controls"])
    for key in keys:
        keys[key]=int(keys[key])
    
    if fullscreen:
        if doublebuffer:
            flags = pygame.FULLSCREEN | pygame.HWACCEL | pygame.DOUBLEBUF
        else:
            flags = pygame.FULLSCREEN | pygame.HWACCEL
    else:
        flags = 0
    pygame.init()
    screen = pygame.display.set_mode(screensize, flags)
    Game().main(screen,keys)
