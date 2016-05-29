# New Game Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI import menuItem
from os.path import join as pathjoin
from libs.textglitcher import makeGlitched
from components.UI.textMenuItem import textMenuItem
from game import Game
from components.UI.menu import menu


class CFMenu(menu):
    """ Represents the critical failure menu"""

    def __init__(self, screen, keys, config, sounds, modifiers, log):
        self.logSectionName = "CFMenu"
        self.modifiers = modifiers
        super().__init__(screen, keys, config, sounds, log)

    def newCFGame(self):
        self.running = False
        self.modlogger.info("Starting" + pathjoin("data",
                             "campaigns",
                             "main.cmp"))

        Game().main(self.screen, self.keys,
                    "criticalfailure",
                    pathjoin("data",
                             "campaigns",
                             "main.cmp"),
                    self.config,
                    self.sounds,
                    self.modifiers,
                    self.mainLogger)

    def newCFSGame(self):
        self.running = False
        Game().main(self.screen, self.keys,
                    "cfsingle",
                    pathjoin("data",
                             "campaigns",
                             "main.cmp"),
                    self.config,
                    self.sounds,
                    self.modifiers,
                    self.mainLogger)

    def makeCFMenu(self):
        self.sd = textMenuItem("Start Shared Time Mode", (50, 180),
                               lambda: self.editDesc(
                                    "All Rooms share the same timer."),
                                    lambda: self.newCFGame(),
                                    self.config, self.sounds, self.font)
        self.items.append(self.sd)
        self.activeItems.append(self.sd)

    def makeCFSMenu(self):
        self.sds = textMenuItem("Start Separated Times Mode", (50, 240),
                                lambda: self.editDesc(
                                         "Each room has its timer."),
                                lambda: self.newCFSGame(),
                                self.config, self.sounds, self.font)
        self.items.append(self.sds)
        self.activeItems.append(self.sds)

    def makeMainMenuItem(self):
        self.mainmenu = textMenuItem("Previous Menu", (50, 560),
                                     lambda: self.editDesc(
                                              "Go to the previous menu"),
                                     lambda: self.goToMenu(),
                                     self.config, self.sounds, self.font)
        self.items.append(self.mainmenu)
        self.activeItems.append(self.mainmenu)

    def makeMenuItems(self):
        self.makeCFMenu()
        self.makeCFSMenu()
        self.makeMainMenuItem()