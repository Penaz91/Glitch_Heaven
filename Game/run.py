#!/usr/bin/env python3
# Bootstrapper
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from mainmenu import mainMenu
# import configparser
import json
import logging
import sys
from logging.handlers import TimedRotatingFileHandler
from os.path import join as pathjoin
from os import getcwd as pwd
from os.path import dirname, realpath
from os import chdir
if __name__ == "__main__":
    # Changed directory for non-console execution
    # v---------------------------------------------------------------v
    if getattr(sys, 'frozen', False):
        wd = dirname(sys.executable)
    elif __file__:
        wd = dirname(realpath(__file__))
    chdir(wd)
    # ^---------------------------------------------------------------^
    try:
        # config = configparser.ConfigParser()
        # config.read("game.conf")
        config = None
        with open(pathjoin("config.json")) as conf:
            config = json.loads(conf.read())
    except IOError:
        print("There has been an error while loading the " +
              "configuration file. Exiting")
    fh = TimedRotatingFileHandler(pathjoin("logs", "Game.log"),
                                  "midnight", 1)
    loglist = {"DEBUG": logging.DEBUG,
               "INFO": logging.INFO,
               "WARNING": logging.WARNING,
               "ERROR": logging.ERROR,
               "CRITICAL": logging.CRITICAL}
    logkey = loglist[config["Debug"]["loggerlevel"]]
    logging.info("-----------------Initialising logging-----------------")
    logger = logging.getLogger("Glitch_Heaven")
    logger.setLevel(logkey)
    fh.setLevel(logkey)
    formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                                  ' %(levelname)s --- %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    logger.info("----------Logger initialised----------")
    logger.debug("Current Working directory is: " + str(pwd()))
    try:
        # Reads the game configuration
        # v-------------------------------------------------------------------v
        logger.info("Parsing configuration file")
        screensize = (int(config["Video"]["screenwidth"]),
                      int(config["Video"]["screenheight"]))
        logger.debug("Screensize set to: " + str(screensize))
        # fullscreen = config.getboolean("Video", "fullscreen")
        fullscreen = config["Video"]["fullscreen"]
        logger.debug("Fullscreen Flag Set to: "+str(fullscreen))
        # doublebuffer = config.getboolean("Video", "doublebuffer")
        doublebuffer = config["Video"]["fullscreen"]
        logger.debug("Doublebuffer Flag set to: " +
                     str(doublebuffer))
        flags = None
        # Reads the control keys
        # v-------------------------------v
        logger.info("Loading key dictionary")
        # keys = dict(config["Controls"])
        # for key in keys:
        #    keys[key] = int(keys[key])
        # logger.debug("Key Dictionary is:" + str(keys))
        keys = config["Controls"]
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
        if config["Sound"]["mixer_preinit"]:
            logger.info("Pre-initialising Mixer")
            try:
                pygame.mixer.pre_init(48000, 16, 2, 4096)
            except:
                logger.error("Mixer pre-init failed, continuing")
        logger.info("Initialising Display")
        pygame.display.init()
        logger.info("Initialising Fonts")
        pygame.font.init()
        logger.info("Initialising Mixer")
        pygame.mixer.init()
        # Sound Loading
        # v-------------------------------------------------------------------v
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
                                                          "bounce.wav")),
                    "static": pygame.mixer.Sound(pathjoin("resources",
                                                          "sounds",
                                                          "static.wav"))
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
            sounds["menu"][sound].set_volume(
                # config.getfloat("Sound",
                #                 "menuvolume"))/100)
                config["Sound"]["menuvolume"]/100.)
        for sound in sounds["sfx"]:
            sounds["sfx"][sound].set_volume(
                # (config.getfloat("Sound",
                #                  "sfxvolume"))/100)
                config["Sound"]["sfxvolume"]/100.)
        for sound in sounds["music"]:
            sounds["music"][sound].set_volume(
                    # (config.getfloat("Sound",
                    #                  "musicvolume"))/100)
                    config["Sound"]["musicvolume"]/100.)
        # ^-------------------------------------------------------------------^
        logger.info("Setting up the Screen")
        screen = pygame.display.set_mode(screensize, flags)
        logger.info("Opening the menu")
        mainMenu(screen, keys, config, sounds, logger).mainLoop()
        logger.info("Quitting")
        pygame.quit()
        quit()
    except SystemExit:
        logger.info("Game has exited correctly")
    except:
        logger.critical("There has been an exception, printing traceback",
                        exc_info=True)
    finally:
        logging.shutdown()
