# Main Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
import os
from components.UI import menuItem
from optionsmenu import OptionsMenu
from newgamemenu import NewGameMenu
from credits import Credits
from loadSaves import loadSaveMenu
from libs.textglitcher import makeGlitched
from components.UI.textMenuItem import textMenuItem
from components.UI.menu import menu
from components.UI.comicreader import comicReader
from os.path import join as pjoin


class mainMenu(menu):
    """ Represents the main Game menu """

    def __init__(self, screen, keys, config, sounds, log):
        self.logSectionName = "mainMenu"
        super().__init__(screen, keys, config, sounds, log)
        self.dbtxt = makeGlitched(
                "Debug Mode Active, Keydebug Active: {0}".format(
                    config["Debug"]["keydebug"]), self.font)

    def quitFunction(self):
        IM = comicReader(pjoin("resources",
                               "intermissions",
                               "main",
                               "4"), self.screen,
                         self.keys["action"], self.mainLogger)
        IM.look()
        pygame.event.post(pygame.event.Event(pygame.QUIT))

    def onEscape(self):
        pass

    def newGame(self):
        self.update = True
        NewGameMenu(self.screen, self.keys, self.config, self.sounds,
                    self.mainLogger).mainLoop()

    def makeNewGameMenu(self):
        self.newgamemenu = textMenuItem("Start A New Game", (50, 180),
                                        lambda: self.editDesc(
                                                 "Start a new game,in any mode"
                                                 ),
                                        lambda: self.newGame(),
                                        self.config, self.sounds, self.font)
        self.activeItems.append(self.newgamemenu)
        self.items.append(self.newgamemenu)

    def makeCreditsMenu(self):
        self.credits = textMenuItem("Credits", (50, 360),
                                    lambda: self.editDesc(
                                             "Look at Names"),
                                    lambda: Credits(
                                             self.screen, self.keys,
                                             self.config, self.sounds,
                                             self.mainLogger).mainLoop(),
                                    self.config, self.sounds, self.font)
        self.activeItems.append(self.credits)
        self.items.append(self.credits)

    def makeHowToMenu(self):
        self.howTo = textMenuItem("How to Play", (50, 420),
                                  lambda: self.editDesc(
                                      "Learn how to play the game"),
                                  lambda: comicReader(pjoin("resources",
                                                         "howto"), self.screen,
                                                   self.keys["action"], self.mainLogger).look(),
                                  self.config, self.sounds, self.font)
        self.activeItems.append(self.howTo)
        self.items.append(self.howTo)

    def makeQuitMenu(self):
        self.exit = textMenuItem("Quit", (700, 560),
                                 lambda: self.editDesc("Quit the Game"),
                                 lambda: self.quitFunction(),
                                 self.config, self.sounds, self.font)
        self.activeItems.append(self.exit)
        self.items.append(self.exit)

    def loadSaveGame(self):
        self.update = True
        loadSaveMenu(self.screen, self.keys, self.config, self.sounds,
                     self.mainLogger).mainLoop()

    def makeLoadMenu(self):
        self.modlogger.debug("Checking Savegames Directory: " + str(
            os.path.join("savegames")))
        if not os.listdir(os.path.join("savegames")):
            self.modlogger.debug("No SaveFiles Found.")
            self.cont = self.font.render("Load Saved Game", False,
                                         (100, 100, 100)).convert_alpha()
            self.cgam = menuItem.menuitem(self.cont,
                                          self.cont,
                                          (50, 240),
                                          lambda: self.editDesc(None),
                                          lambda: None,
                                          self.config,
                                          self.sounds)
        else:
            self.modlogger.debug("SaveFiles Found, enabling load menu item.")
            self.cgam = textMenuItem("Load Saved Game", (50, 240),
                                     lambda: self.editDesc(
                                              "Load a previously saved Game"),
                                     lambda: self.loadSaveGame(),
                                     self.config, self.sounds, self.font)
            self.activeItems.append(self.cgam)
        self.items.append(self.cgam)
        self.update = False

    def makeOptionsMenu(self):
        self.options = textMenuItem("Options", (50, 300),
                                    lambda: self.editDesc(
                                             "Fiddle With Options"),
                                    lambda: OptionsMenu(
                                             self.screen, self.keys,
                                             self.config, self.sounds,
                                             self.mainLogger).mainLoop(),
                                    self.config, self.sounds, self.font)
        self.activeItems.append(self.options)
        self.items.append(self.options)

    def makeMenuItems(self):
        # New Game Menu menu element
        # v------------------------------------------------------------------v
        self.makeNewGameMenu()
        # ^------------------------------------------------------------------^
        # If there is a savefile, enable the continue game button
        # v------------------------------------------------------------------v
        self.makeLoadMenu()
        # ^------------------------------------------------------------------^
        # Insert an options button
        # v------------------------------------------------------------------v
        self.makeOptionsMenu()
        # ^------------------------------------------------------------------^
        # Credits menu element
        # v------------------------------------------------------------------v
        self.makeCreditsMenu()
        # ^------------------------------------------------------------------^
        self.makeHowToMenu()
        # Quit game menu element
        # v------------------------------------------------------------------v
        self.makeQuitMenu()
        # ^------------------------------------------------------------------^

    def doAdditionalBlits(self):
        if self.config["Debug"]["debugmode"]:
            self.screen.blit(self.dbtxt, (50, 560))

    def doMoreLoopOperations(self):
        if self.update:
            self.activeItems.clear()
            self.items.clear()
            self.makeMenuItems()
