# Keyboard Item Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
from components.UI.menuItem import menuitem
from libs.textglitcher import makeGlitched
import pygame
import logging
import os
from logging import handlers as loghandler

mod_logger = logging.getLogger("Glitch_Heaven.KeyboardItem")
fh = loghandler.TimedRotatingFileHandler(os.path.join("logs", "Game.log"),
                                         "midnight", 1)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                              ' %(levelname)s --- %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
mod_logger.addHandler(fh)
mod_logger.addHandler(ch)


class KeyboardItem (menuitem):

    def KeySelect(self, font, key, config, keys):
        truth = True
        mod_logger.debug("Entering the keychange event loop , Key is %s" % key)
        while truth:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.unselected = font.render(
                            (str(pygame.key.name(event.key))).upper(),
                            False, (255, 255, 255)).convert_alpha()
                    self.selected = makeGlitched(
                            (str(pygame.key.name(event.key))).upper(), font)
                    config.set("Controls", str(key), str(event.key))
                    with open("game.conf", "w") as conf:
                        config.write(conf)
                    keys[key] = event.key
                    truth = False
                    mod_logger.debug("Key Changed to %s"
                                     % pygame.key.name(event.key))
