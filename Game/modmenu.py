# Modifiers Menu Component
# Part of the Glitch_Heaven Project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI.textMenuItem import textMenuItem


class modMenu(menu):

    def __init__(self, screen, keys, config, sounds, modifiers, log):
        self.logSectionName = "modifiersMenu"
        self.modifiers = modifiers
        super().__init__(screen, keys, config, sounds, log)

    def toggleModifier(self, mod):
        self.modifiers[mod] = not self.modifiers[mod]
        self.modlogger.info("Toggled modifier {0}, current status {1}".format(
            mod, self.modifiers[mod]))

    def makeMainMenuItem(self):
        self.mainmenu = textMenuItem("Previous Menu", (600, 560),
                                     lambda: self.editDesc(
                                              "Go to the main menu"),
                                     lambda: self.goToMenu(),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.mainmenu)
        self.items.append(self.mainmenu)

    def makeChaosToggle(self):
        self.chaos = textMenuItem("Chaos Mode", (50, 180),
                                  lambda: self.editDesc(
                                           "Current Status: {0}".format(
                                            self.modifiers["chaos"])),
                                  lambda: self.toggleModifier("chaos"),
                                  self.config, self.sounds, self.font)
        self.activeItems.append(self.chaos)
        self.items.append(self.chaos)

    def makeVFlipToggle(self):
        self.vflip = textMenuItem("Vertical Flip Mode", (50, 240),
                                  lambda: self.editDesc(
                                           "Current Status: {0}".format(
                                            self.modifiers["vflip"])),
                                  lambda: self.toggleModifier("vflip"),
                                  self.config, self.sounds, self.font)
        self.activeItems.append(self.vflip)
        self.items.append(self.vflip)

    def makeHFlipToggle(self):
        self.hflip = textMenuItem("Horizontal Flip Mode", (50, 300),
                                  lambda: self.editDesc(
                                               "Current Status: {0}".format(
                                                self.modifiers["hflip"])),
                                  lambda: self.toggleModifier(
                                     "hflip"),
                                  self.config, self.sounds, self.font)
        self.activeItems.append(self.hflip)
        self.items.append(self.hflip)

    def makeMWToggle(self):
        self.mw = textMenuItem("MoonWalk Mode", (50, 360),
                               lambda: self.editDesc(
                                        "Current Status: {0}".format(
                                         self.modifiers["moonwalk"])),
                               lambda: self.toggleModifier(
                                        "moonwalk"),
                               self.config, self.sounds, self.font)
        self.activeItems.append(self.mw)
        self.items.append(self.mw)

    def makeMenuItems(self):
        self.makeChaosToggle()
        self.makeVFlipToggle()
        self.makeHFlipToggle()
        self.makeMWToggle()
        self.makeMainMenuItem()
