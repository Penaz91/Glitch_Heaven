# Main Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
import pygame
from game import Game
import os
from components.UI import menuItem
from optionsmenu import OptionsMenu
from newgamemenu import NewGameMenu
from credits import Credits
from libs.textglitcher import makeGlitched
from components.UI.menu import menu


class mainMenu(menu):
    """ Represents the main Game menu """

    def __init__(self, screen, keys, config, sounds, log):
        self.logSectionName = "mainMenu"
        super().__init__(screen, keys, config, sounds, log)
        self.dbtxt = makeGlitched(
                "Debug Mode Active, Keydebug Active: {0}".format(
                    config["Debug"]["keydebug"]), self.font)

    def onEscape(self):
        pass

    def makeNewGameMenu(self):
        self.newgameimg = self.font.render("Start A New Game", False,
                                           (255, 255, 255)).convert_alpha()
        self.selectedgameimg = makeGlitched("Start A New Game", self.font)
        self.newgamemenu = menuItem.menuitem(self.newgameimg,
                                             self.selectedgameimg,
                                             (50, 180),
                                             lambda: self.editDesc(
                                                 "Start a new game,in any mode"
                                                 ),
                                             lambda: NewGameMenu(
                                                self.screen,
                                                self.keys,
                                                self.config,
                                                self.sounds,
                                                self.mainLogger).mainLoop(),
                                             self.config,
                                             self.sounds)
        self.activeItems.append(self.newgamemenu)
        self.items.append(self.newgamemenu)

    def makeCreditsMenu(self):
        self.creditsimg = self.font.render("Credits", False,
                                           (255, 255, 255)).convert_alpha()
        self.selectedcreditsimg = makeGlitched("Credits", self.font)
        self.credits = menuItem.menuitem(self.creditsimg,
                                         self.selectedcreditsimg,
                                         (50, 360),
                                         lambda: self.editDesc(
                                             "Look at Names"),
                                         lambda: Credits(
                                             self.screen,
                                             self.keys,
                                             self.config,
                                             self.sounds,
                                             self.mainLogger).mainLoop(),
                                         self.config,
                                         self.sounds)
        self.activeItems.append(self.credits)
        self.items.append(self.credits)

    def makeQuitMenu(self):
        self.exitimg = self.font.render("Quit", False,
                                        (255, 255, 255)).convert_alpha()
        self.exitselected = makeGlitched("Quit", self.font)
        self.exit = menuItem.menuitem(self.exitimg,
                                      self.exitselected,
                                      (700, 560),
                                      lambda: self.editDesc("Quit the Game"),
                                      lambda: pygame.event.post(
                                          pygame.event.Event(pygame.QUIT)),
                                      self.config,
                                      self.sounds)
        self.activeItems.append(self.exit)
        self.items.append(self.exit)

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
            self.cont = self.font.render("Load Saved Game", False,
                                         (255, 255, 255)).convert_alpha()
            self.contsel = makeGlitched("Load Saved Game", self.font)
            self.cgam = menuItem.menuitem(self.cont,
                                          self.contsel,
                                          (50, 240),
                                          lambda: self.editDesc(
                                              "Load a previously saved Game"),
                                          lambda: Game().main(self.screen,
                                                              self.keys,
                                                              "load",
                                                              None,
                                                              self.config,
                                                              self.sounds,
                                                              None,
                                                              self.mainLogger),
                                          self.config,
                                          self.sounds)
            self.activeItems.append(self.cgam)
        self.items.append(self.cgam)
        self.update = False

    def makeOptionsMenu(self):
        self.optimg = self.font.render("Options", False,
                                       (255, 255, 255)).convert_alpha()
        self.optsel = makeGlitched("Options", self.font)
        self.options = menuItem.menuitem(self.optimg,
                                         self.optsel,
                                         (50, 300),
                                         lambda: self.editDesc(
                                             "Fiddle With Options"),
                                         lambda: OptionsMenu(
                                             self.screen, self.keys,
                                             self.config,
                                             self.sounds,
                                             self.mainLogger).mainLoop(),
                                         self.config,
                                         self.sounds)
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
        # Quit game menu element
        # v------------------------------------------------------------------v
        self.makeQuitMenu()
        # ^------------------------------------------------------------------^

    def doAdditionalBlits(self):
        if self.config["Debug"]["Debugmode"]:
            self.screen.blit(self.dbtxt, (50, 560))

    def doMoreLoopOperations(self):
        if self.update:
            self.makeMenuItems()
