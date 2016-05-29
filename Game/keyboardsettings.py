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
        self.writings = []
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
        self.drawer.append((txt, btn, location))
        return btn

    def makeLeftKeyItem(self):
        self.left = self.makeItem("Move Left:", "left", (50, 180))
        self.activeItems.append(self.left)
        self.items.append(self.left)

    def makeRightKeyItem(self):
        self.right = self.makeItem("Move Right:", "right", (50, 240))
        self.activeItems.append(self.right)
        self.items.append(self.right)

    def makeJumpKeyItem(self):
        self.jump = self.makeItem("Jump: ", "jump", (50, 300))
        self.activeItems.append(self.jump)
        self.items.append(self.jump)

    def makeRunKeyItem(self):
        self.run = self.makeItem("Run: ", "run", (50, 360))
        self.activeItems.append(self.run)
        self.items.append(self.run)

    def makeActionKeyItem(self):
        self.act = self.makeItem("Action/Interact: ", "action", (50, 420))
        self.activeItems.append(self.act)
        self.items.append(self.act)

    def makeRestartKeyItem(self):
        self.rest = self.makeItem("Restart Level: ", "restart", (50, 480))
        self.activeItems.append(self.rest)
        self.items.append(self.rest)

    def makeMainMenuItem(self):
        self.mainmenu = textMenuItem("Previous Menu", (50, 560),
                                     lambda: None,
                                     lambda: self.goToMenu(),
                                     self.config, self.sounds, self.font)

        self.items.append(self.mainmenu)
        self.activeItems.append(self.mainmenu)

    def makeMenuItems(self):
        self.makeLeftKeyItem()
        self.makeRightKeyItem()
        self.makeJumpKeyItem()
        self.makeRunKeyItem()
        self.makeActionKeyItem()
        self.makeRestartKeyItem()
        self.makeMainMenuItem()

    def doAdditionalBlits(self):
        for item in self.drawer:
            self.screen.blit(item[0], item[2])
