# Pause Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI import menuItem
from libs.textglitcher import makeGlitched
import pygame


class pauseMenu(menu):

    def __init__(self, screen, keys, game, config, sounds):
        self.game = game
        self.logSectionName = "Glitch_Heaven.pauseMenu"
        super().__init__(screen, keys, config, sounds)

    def doAdditionalClosingOperations(self):
        self.game.running = False

    def unpause(self):
        self.modlogger.info("Game unPaused")
        self.running = False
        pygame.mouse.set_visible(False)
        self.modlogger.debug("Mouse cursor hidden")

    def makeResumeItem(self):
        self.resgameimg = self.font.render("Resume Game", False,
                                           (255, 255, 255)).convert_alpha()
        self.selectedimg = makeGlitched("Resume Game", self.font)
        self.resgame = menuItem.menuitem(self.resgameimg,
                                         self.selectedimg,
                                         (50, 240),
                                         lambda: self.editDesc(
                                             "Resume the paused Game"),
                                         lambda: self.unpause(),
                                         self.config,
                                         self.sounds)
        self.activeItems.append(self.resgame)
        self.items.append(self.resgame)

    def makeSaveGameItem(self):
        self.saveimg = self.font.render("Save Game", False,
                                        (255, 255, 255)).convert_alpha()
        self.saveselected = makeGlitched("Save Game", self.font)
        self.savegame = menuItem.menuitem(self.saveimg,
                                          self.saveselected,
                                          (50, 320),
                                          lambda: self.editDesc(
                                              "Save for safety"),
                                          lambda: self.game.saveGame(),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.savegame)
        self.items.append(self.savegame)

    def makeQuitItem(self):
        self.exitimg = self.font.render("Quit to Desktop",
                                        False, (255, 255, 255)).convert_alpha()
        self.exitselected = makeGlitched("Quit to Desktop", self.font)
        self.exit = menuItem.menuitem(self.exitimg,
                                      self.exitselected,
                                      (50, 560),
                                      lambda: self.editDesc(
                                          "Outta Here, NOW!!"),
                                      lambda: pygame.event.post(
                                        pygame.event.Event(pygame.QUIT)),
                                      self.config,
                                      self.sounds)
        self.activeItems.append(self.exit)
        self.items.append(self.exit)

    def makeMainMenuItem(self):
        self.menu = self.font.render("Main Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Main Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (50, 400),
                                          lambda: self.editDesc(
                                              "Get back to the main menu"),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.mainmenu)
        self.items.append(self.mainmenu)

    def makeMenuItems(self):
        self.makeResumeItem()
        self.makeSaveGameItem()
        self.makeMainMenuItem()
        self.makeQuitItem()
