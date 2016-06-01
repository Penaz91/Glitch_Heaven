# New Game Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.textMenuItem import textMenuItem
from components.UI.menuItem import menuitem
from os.path import join as pathjoin
from libs.textglitcher import makeGlitched
from game import Game
from cfmenu import CFMenu
from components.UI.menu import menu
from loadcmpmenu import loadCmpMenu
from loadsinglefolds import loadSingleFoldMenu
from modmenu import modMenu


class NewGameMenu(menu):
    """ Represents a pause menu window"""

    def __init__(self, screen, keys, config, sounds, log):
        self.logSectionName = "newGameMenu"
        self.modifiers = {"chaos": False, "vflip": False,
                          "hflip": False, "moonwalk": False}
        super().__init__(screen, keys, config, sounds, log)

    def loadcustom(self):
        loadCmpMenu(self.screen, self.keys, self.config,
                    self.sounds, self.modifiers, self.mainLogger).mainLoop()

    def loadSingle(self):
        loadSingleFoldMenu(self.screen, self.keys, self.config,
                           self.sounds, self.modifiers, self.mainLogger
                           ).mainLoop()

    def newGame(self):
        self.running = False
        Game().main(self.screen, self.keys, "newgame",
                    pathjoin("data", "campaigns", "main.cmp"),
                    self.config, self.sounds, self.modifiers, self.mainLogger)

    def newSMGame(self):
        self.loadSingle()

    def makeCampaignMenu(self):
        self.newmaingame = textMenuItem("Start Main Campaign", (50, 180),
                                        lambda: self.editDesc(
                                            "Play the Main Game"),
                                        lambda: self.newGame(),
                                        self.config, self.sounds, self.font)
        self.activeItems.append(self.newmaingame)
        self.items.append(self.newmaingame)

    def makeCustomCampaignMenu(self):
        self.newcustomgame = textMenuItem("Start Custom Campaign", (50, 240),
                                          lambda: self.editDesc(
                                              "Load a custom Campaign"),
                                          lambda: self.loadcustom(),
                                          self.config, self.sounds, self.font)
        self.activeItems.append(self.newcustomgame)
        self.items.append(self.newcustomgame)

    def makeSpeedRunMenu(self):
        self.sr = textMenuItem("(File Corrupted)", (50, 300),
                               lambda: None, lambda: None,
                               self.config, self.sounds, self.font)
        self.items.append(self.sr)

    def makeNHMenu(self):
        if self.config["Unlockables"]["NHMode"]:
            self.nhimg = self.font.render("Start the Second Quest",
                                          False,
                                          (100, 100, 100)).convert_alpha()
        else:
            self.nhimg = self.font.render("(File Corrupted)", False,
                                          (100, 100, 100)).convert_alpha()
        self.nh = menuitem(self.nhimg,
                           self.nhimg,
                           (50, 360),
                           lambda: self.editDesc(None),
                           lambda: None,
                           self.config,
                           self.sounds)
        self.items.append(self.nh)

    def makeSDMenu(self):
        if self.config["Unlockables"]["CFMode"]:
            self.sdimg = self.font.render("Start 'Critical Failure' Mode",
                                          False,
                                          (255, 255, 255)).convert_alpha()
            self.sdselimg = makeGlitched("Start 'Critical Failure' Mode",
                                         self.font)
            self.sd = menuitem(self.sdimg,
                               self.sdselimg,
                               (50, 420),
                               lambda: self.editDesc(
                                   "Escape before the time runs out."
                                   ),
                               lambda: CFMenu(
                                       self.screen,
                                       self.keys,
                                       self.config,
                                       self.sounds,
                                       self.modifiers,
                                       self.mainLogger).mainLoop(),
                               self.config,
                               self.sounds)
            self.activeItems.append(self.sd)
        else:
            self.sdimg = self.font.render("(File Corrupted)", False,
                                          (100, 100, 100)).convert_alpha()
            self.sd = menuitem(self.sdimg,
                               self.sdimg,
                               (50, 420),
                               lambda: self.editDesc(None),
                               lambda: None,
                               self.config,
                               self.sounds)
        self.items.append(self.sd)

    def makeSMMenu(self):
        self.sm = textMenuItem("Play a Single Map", (50, 540),
                               lambda: self.editDesc("Load a single map"),
                               lambda: self.newSMGame(),
                               self.config, self.sounds, self.font)
        self.items.append(self.sm)
        self.activeItems.append(self.sm)

    def makeModifierMenuItem(self):
        if self.config["Unlockables"]["modifiers"]:
            self.chimg = self.font.render("Modifiers Menu",
                                          False,
                                          (255, 255, 255)).convert_alpha()
            self.chselimg = makeGlitched("Modifiers Menu",
                                         self.font)
            self.cb = menuitem(self.chimg,
                               self.chselimg,
                               (50, 480),
                               lambda: self.editDesc(
                                   "Access the mods menu"),
                               lambda: modMenu(self.screen,
                                               self.keys,
                                               self.config,
                                               self.sounds,
                                               self.modifiers,
                                               self.mainLogger
                                               ).mainLoop(),
                               self.config,
                               self.sounds)
            self.activeItems.append(self.cb)
        else:
            self.chimg = self.font.render("(File Corrupted)", False,
                                          (100, 100, 100)).convert_alpha()
            self.cb = menuitem(self.chimg,
                               self.chimg,
                               (50, 480),
                               lambda: self.editDesc(None),
                               lambda: None,
                               self.config,
                               self.sounds)
        self.items.append(self.cb)

    def makeMainMenuItem(self):

        self.mainmenu = textMenuItem("Previous Menu", (600, 560),
                                     lambda: self.editDesc(
                                         "Go to the main menu"),
                                     lambda: self.goToMenu(),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.mainmenu)
        self.items.append(self.mainmenu)

    def makeMenuItems(self):
        self.makeCampaignMenu()
        self.makeCustomCampaignMenu()
        self.makeSpeedRunMenu()
        self.makeNHMenu()
        self.makeSDMenu()
        self.makeModifierMenuItem()
        self.makeSMMenu()
        self.makeMainMenuItem()
