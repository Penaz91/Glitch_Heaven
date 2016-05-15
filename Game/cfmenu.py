# New Game Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI import menuItem
from os.path import join as pathjoin
from libs.textglitcher import makeGlitched
from game import Game
from components.UI.menu import menu


class CFMenu(menu):
    """ Represents a pause menu window"""

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
        self.sdimg = self.font.render("Start Shared Time mode", False,
                                      (255, 255, 255)).convert_alpha()
        self.sdselimg = makeGlitched("Start Shared Time mode", self.font)
        self.sd = menuItem.menuitem(self.sdimg,
                                    self.sdselimg,
                                    (50, 180),
                                    lambda: self.editDesc(
                                        "All rooms share the same timer."),
                                    lambda: self.newCFGame(),
                                    self.config,
                                    self.sounds
                                    )
        self.items.append(self.sd)
        self.activeItems.append(self.sd)

    def makeCFSMenu(self):
        self.sdsimg = self.font.render("Start Separated Times mode", False,
                                       (255, 255, 255)).convert_alpha()
        self.sdsselimg = makeGlitched("Start Separated Times mode", self.font)
        self.sds = menuItem.menuitem(self.sdsimg,
                                     self.sdsselimg,
                                     (50, 240),
                                     lambda: self.editDesc(
                                         "Each room has its timer."),
                                     lambda: self.newCFSGame(),
                                     self.config,
                                     self.sounds
                                     )
        self.items.append(self.sds)
        self.activeItems.append(self.sds)

    def makeMainMenuItem(self):
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Previous Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Previous Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (50, 560),
                                          lambda: self.editDesc(
                                              "Go to the previous menu"),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          self.sounds)
        self.items.append(self.mainmenu)
        self.activeItems.append(self.mainmenu)
        # ^------------------------------------------------------------------^

    def makeMenuItems(self):
        self.makeCFMenu()
        self.makeCFSMenu()
        self.makeMainMenuItem()
