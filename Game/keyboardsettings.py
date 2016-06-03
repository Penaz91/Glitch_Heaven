# Keyboard Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI.textMenuItem import textMenuItem
from components.UI.textKeyboardItem import textKeyboardItem
import pygame


class KeyboardSettings(menu):
    white = (255, 255, 255)

    def __init__(self, screen, keys, config, sounds, log):
        self.drawer = []
        self.logSectionName = "keyboardSettings"
        super().__init__(screen, keys, config, sounds, log)

    def makeItem(self, text, key, location):
        txt = self.font.render(text, False, self.white).convert_alpha()
        btn = textKeyboardItem(pygame.key.name(
                                    self.config["Controls"][key]).upper(),
                               (txt.get_rect().width + location[0] + 30,
                                   location[1]),
                               lambda: None,
                               lambda: btn.KeySelect(self.font, key,
                                                     self.config, self.keys),
                               self.config, self.sounds, self.modlogger,
                               self.font)
        self.drawer.append((txt, location))
        self.activeItems.append(btn)
        self.items.append(btn)

    def makeMainMenuItem(self):
        self.mainmenu = textMenuItem("Previous Menu", (50, 560),
                                     lambda: None,
                                     lambda: self.goToMenu(),
                                     self.config, self.sounds, self.font)
        self.items.append(self.mainmenu)
        self.activeItems.append(self.mainmenu)

    def makeMenuItems(self):
        self.makeItem("Move Left:", "left", (50, 180))
        self.makeItem("Move Right:", "right", (50, 240))
        self.makeItem("Jump: ", "jump", (50, 300))
        self.makeItem("Run: ", "run", (50, 360))
        self.makeItem("Action/Interact: ", "action", (50, 420))
        self.makeItem("Restart Level: ", "restart", (50, 480))
        self.makeMainMenuItem()

    def doAdditionalBlits(self):
        for item in self.drawer:
            self.screen.blit(item[0], item[1])
