# Keyboard Item Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menuItem import menuitem
from libs.textglitcher import makeGlitched
import pygame
import json


class KeyboardItem (menuitem):

    def __init__(self, unselected, selected,
                 location, onhover, function, config, sounds, log):
        self.mod_logger = log.getChild("keyboardItem")
        super().__init__(unselected, selected,
                         location, onhover, function, config, sounds)

    def KeySelect(self, font, key, config, keys):
        truth = True
        self.mod_logger.debug("Entering the keychange \
                event loop , Key is %s" % key)
        while truth:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.unselected = font.render(
                            (str(pygame.key.name(event.key))).upper(),
                            False, (255, 255, 255)).convert_alpha()
                    self.selected = makeGlitched(
                            (str(pygame.key.name(event.key))).upper(), font)
                    # config.set("Controls", str(key), str(event.key))
                    # with open("game.conf", "w") as conf:
                    #    config.write(conf)
                    config["Controls"][str(key)] = str(event.key)
                    with open("newconf.json", "w") as conf:
                        conf.write(json.dumps(config))
                    keys[key] = event.key
                    truth = False
                    self.mod_logger.debug("Key Changed to %s"
                                          % pygame.key.name(event.key))
