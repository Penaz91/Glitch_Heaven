# New Game Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI import menuItem
from os.path import join as pathjoin
from os.path import splitext
from libs.textglitcher import makeGlitched
from tkinter import Tk
from tkinter import filedialog
from game import Game
from cfmenu import CFMenu
from components.UI.menu import menu
from modmenu import modMenu


class NewGameMenu(menu):
    """ Represents a pause menu window"""

    def __init__(self, screen, keys, config, sounds, log):
        self.logSectionName = "newGameMenu"
        self.modifiers = {"chaos": False, "vflip": False,
                          "hflip": False, "moonwalk": False}
        super().__init__(screen, keys, config, sounds, log)

    def loadcustom(self):
        """
        Loads a custom campaign from a open file dialog
        """
        try:
            Tk().withdraw()
            formats = [("Glitch_Heaven Campaign", "*.cmp")]
            self.camp = filedialog.askopenfilename(
                    filetypes=formats,
                    initialdir=pathjoin("data",
                                        "campaigns"))
            if self.camp:
                self.running = False
                Game().main(self.screen, self.keys, "newgame",
                            self.camp, self.config, self.sounds,
                            self.modifiers, self.mainLogger)
        except FileNotFoundError:
            self.modlogger.info("No File selected, "
                                "Loading of campaign aborted")

    def newGame(self, keys, gameconfig, screen, sounds):
        self.running = False
        Game().main(screen, keys,
                    "newgame",
                    pathjoin("data",
                             "campaigns",
                             "main.cmp"),
                    self.config,
                    sounds,
                    self.modifiers,
                    self.mainLogger)

    def newSMGame(self):
        try:
            Tk().withdraw()
            formats = [("Glitch_Heaven Level", "*.tmx")]
            self.lvl = filedialog.askopenfilename(
                    filetypes=formats,
                    initialdir=pathjoin("data",
                                        "maps"))
            self.lvl = splitext(self.lvl)[0]
            if self.lvl:
                self.running = False
                Game().main(self.screen, self.keys, "singlemap",
                            self.lvl, self.config, self.sounds,
                            self.modifiers, self.mainLogger)
        except FileNotFoundError:
            self.modlogger.info("No File selected, "
                                "Loading of level aborted")

    def makeCampaignMenu(self):
        self.newmainimg = self.font.render("Start Main Campaign", False,
                                           (255, 255, 255)).convert_alpha()
        self.selectedmainimg = makeGlitched("Start Main Campaign", self.font)
        self.newmaingame = menuItem.menuitem(self.newmainimg,
                                             self.selectedmainimg,
                                             (50, 180),
                                             lambda: self.editDesc(
                                                 "Play the Main Game"),
                                             lambda: self.newGame(
                                                self.keys,
                                                self.config,
                                                self.screen,
                                                self.sounds
                                                ),
                                             self.config,
                                             self.sounds
                                             )
        self.activeItems.append(self.newmaingame)
        self.items.append(self.newmaingame)

    def makeCustomCampaignMenu(self):
        self.newcustomimg = self.font.render("Start Custom Campaign", False,
                                             (255, 255, 255)).convert_alpha()
        self.selectedcustomimg = makeGlitched("Start Custom Campaign",
                                              self.font)
        self.newcustomgame = menuItem.menuitem(self.newcustomimg,
                                               self.selectedcustomimg,
                                               (50, 240),
                                               lambda: self.editDesc(
                                                   "Load a custom Campaign"),
                                               lambda: self.loadcustom(),
                                               self.config,
                                               self.sounds
                                               )
        self.activeItems.append(self.newcustomgame)
        self.items.append(self.newcustomgame)

    def makeSpeedRunMenu(self):
        self.srimg = self.font.render("SpeedRun Mode", False,
                                      (100, 100, 100)).convert_alpha()
        self.sr = menuItem.menuitem(self.srimg,
                                    self.srimg,
                                    (50, 300),
                                    lambda: self.editDesc(None),
                                    lambda: None,
                                    self.config,
                                    self.sounds)
        self.items.append(self.sr)

    def makeNHMenu(self):
        # if self.config.getboolean("Unlockables", "NHMode"):
        if self.config["Unlockables"]["NHMode"]:
            self.nhimg = self.font.render("Start the Second Quest",
                                          False,
                                          (100, 100, 100)).convert_alpha()
        else:
            self.nhimg = self.font.render("(File Corrupted)", False,
                                          (100, 100, 100)).convert_alpha()
        self.nh = menuItem.menuitem(self.nhimg,
                                    self.nhimg,
                                    (50, 360),
                                    lambda: self.editDesc(None),
                                    lambda: None,
                                    self.config,
                                    self.sounds)
        self.items.append(self.nh)

    def makeSDMenu(self):
        # if self.config.getboolean("Unlockables", "CFMode"):
        if self.config["Unlockables"]["CFMode"]:
            self.sdimg = self.font.render("Start 'Critical Failure' Mode",
                                          False,
                                          (255, 255, 255)).convert_alpha()
            self.sdselimg = makeGlitched("Start 'Critical Failure' Mode",
                                         self.font)
            self.sd = menuItem.menuitem(self.sdimg,
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
            self.sd = menuItem.menuitem(self.sdimg,
                                        self.sdimg,
                                        (50, 420),
                                        lambda: self.editDesc(None),
                                        lambda: None,
                                        self.config,
                                        self.sounds)
        self.items.append(self.sd)

    def makeSMMenu(self):
        self.smimg = self.font.render("Play a Single Map", False,
                                      (255, 255, 255)).convert_alpha()
        self.smsel = makeGlitched("Play a Single Map",
                                  self.font)
        self.sm = menuItem.menuitem(self.smimg,
                                    self.smsel,
                                    (50, 540),
                                    lambda: self.editDesc("Load a single map"),
                                    lambda: self.newSMGame(),
                                    self.config,
                                    self.sounds)
        self.items.append(self.sm)
        self.activeItems.append(self.sm)

    def makeModifierMenuItem(self):
        # if self.config.getboolean("Unlockables", "modifiers"):
        if self.config["Unlockables"]["modifiers"]:
            self.chimg = self.font.render("Modifiers Menu",
                                          False,
                                          (255, 255, 255)).convert_alpha()
            self.chselimg = makeGlitched("Modifiers Menu",
                                         self.font)
            self.cb = menuItem.menuitem(self.chimg,
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
            self.cb = menuItem.menuitem(self.chimg,
                                        self.chimg,
                                        (50, 480),
                                        lambda: self.editDesc(None),
                                        lambda: None,
                                        self.config,
                                        self.sounds)
        self.items.append(self.cb)

    def makeMainMenuItem(self):
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Previous Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Previous Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (600, 560),
                                          lambda: self.editDesc(
                                              "Go to the main menu"),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.mainmenu)
        self.items.append(self.mainmenu)
        # ^------------------------------------------------------------------^

    def makeMenuItems(self):
        # Main campaign menu element
        # v------------------------------------------------------------------v
        self.makeCampaignMenu()
        # Custom campaign menu element
        # v------------------------------------------------------------------v
        self.makeCustomCampaignMenu()
        # Insert a speedrun mode button
        # v------------------------------------------------------------------v
        self.makeSpeedRunMenu()
        # Insert a Hard mode button
        # v------------------------------------------------------------------v
        self.makeNHMenu()
        # Insert a sudden death mode button
        # v------------------------------------------------------------------v
        self.makeSDMenu()
        # Insert a modifiermenu button
        # v------------------------------------------------------------------v
        self.makeModifierMenuItem()
        # Insert a single map mode button
        # v------------------------------------------------------------------v
        self.makeSMMenu()
        # ^------------------------------------------------------------------^
        self.makeMainMenuItem()
