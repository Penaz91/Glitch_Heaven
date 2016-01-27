# Keyboard Item Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
from components.UI.menuItem import menuitem
from libs.textglitcher import makeGlitched
import pygame


class KeyboardItem (menuitem):
    
    def KeySelect (self, font, key, config, keys):
        print("Entering event loop")
        truth = True
        while truth:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    self.unselected = font.render((pygame.key.name(event.key)).upper(),
                                 False, (255, 255, 255)).convert_alpha()
                    self.selected = makeGlitched((pygame.key.name(event.key)).upper(), font)
                    config.set("Controls", str(key), str(event.key))
                    with open("game.conf", "w") as conf:
                        config.write(conf)
                    keys[key] = event.key
                    truth = False