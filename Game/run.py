#!/usr/bin/env python3
# Bootstrapper
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
from mainmenu import menu
import configparser
import logging
from logging import handlers as loghandler
from os.path import join as pathjoin
if __name__ == "__main__":
    try:
        config = configparser.ConfigParser()
        config.read("game.conf")
    except IOError:
        print("There has been an error while loading the " +
              "configuration file. Exiting")
    fh = loghandler.TimedRotatingFileHandler(pathjoin("logs", "Game.log"),
                                             "midnight", 1)
    loglist = {"DEBUG": 10,
               "INFO": 20,
               "WARNING": 30,
               "ERROR": 40,
               "CRITICAL": 50}
    logkey = loglist[config["Debug"]["loggerlevel"]]
    logging.basicConfig(level=logkey,
                        format='[%(asctime)s] (%(name)s) -'
                        ' %(levelname)s --- %(message)s')
    logging.info("-----------------Initialising logging-----------------")
    logger = logging.getLogger("Glitch_Heaven.Bootstrapper")
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                                  ' %(levelname)s --- %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)
    logger.addHandler(ch)
    logger.addHandler(fh)
    logger.info("----------Logger initialised----------")
    try:
        # Reads the game configuration
        # v-------------------------------------------------------------------v
        logger.info("Parsing configuration file")
        screensize = (int(config["Video"]["screenwidth"]),
                      int(config["Video"]["screenheight"]))
        logger.debug("Screensize set to: " + str(screensize))
        fullscreen = config.getboolean("Video", "fullscreen")
        logger.debug("Fullscreen Flag Set to: "+str(fullscreen))
        doublebuffer = config.getboolean("Video", "doublebuffer")
        logger.debug("Doublebuffer Flag set to: " +
                     str(doublebuffer))
        flags = None
        # Reads the control keys
        # v-------------------------------v
        logger.info("Zipping key dictionary")
        keys = dict(config["Controls"])
        for key in keys:
            keys[key] = int(keys[key])
        logger.debug("Key Dictionary is:" + str(keys))
        # ^-------------------------------^
        # Sets the screen flags
        # v-------------------------------v
        logger.info("Setting screen flags")
        if fullscreen:
            if doublebuffer:
                flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
            else:
                flags = pygame.FULLSCREEN | pygame.HWSURFACE
        else:
            flags = 0
        # ^-------------------------------^
        # ^-------------------------------------------------------------------^
        logger.info("Pre-initialising Mixer")
        pygame.mixer.pre_init(48000, 16, 2, 4096)
        logger.info("Initialising Pygame")
        pygame.init()
        logger.info("Initialising Mixer")
        pygame.mixer.init()
        logger.info("Loading sounds")
        sounds = {
                "sfx": {
                    "jump": pygame.mixer.Sound(pathjoin("resources",
                                                        "sounds",
                                                        "jump.wav")),
                    "death": pygame.mixer.Sound(pathjoin("resources",
                                                         "sounds",
                                                         "death.wav")),
                    "bounce": pygame.mixer.Sound(pathjoin("resources",
                                                          "sounds",
                                                          "bounce.wav"))
                    },
                "menu": {
                    "test": pygame.mixer.Sound(pathjoin("resources",
                                                        "sounds",
                                                        "testSound.wav")),
                    "select": pygame.mixer.Sound(pathjoin("resources",
                                                          "sounds",
                                                          "menuSelect.wav")),
                    "confirm": pygame.mixer.Sound(pathjoin("resources",
                                                           "sounds",
                                                           "select.wav"))
                    },
                "music": {}}
        for sound in sounds["menu"]:
            sounds["menu"][sound].set_volume((
                config.getfloat("Sound",
                                "menuvolume"))/100)
        for sound in sounds["sfx"]:
            sounds["sfx"][sound].set_volume((config.getfloat("Sound",
                                                             "sfxvolume"))/100)
        logger.info("Setting up the Screen")
        screen = pygame.display.set_mode(screensize, flags)
        logger.info("Opening the menu")
        menu().main(screen, keys, config, sounds)
        logger.info("Quitting")
        pygame.quit()
        quit()
    except SystemExit:
        logger.info("Game has exited correctly")
        logging.shutdown()
    except:
        logger.critical("There has been an exception, printing traceback",
                        exc_info=True)
