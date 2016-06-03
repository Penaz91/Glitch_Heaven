# Pause Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI.textMenuItem import textMenuItem
from saveGame import saveGameMenu
import pygame


class pauseMenu(menu):

    def __init__(self, screen, keys, game, config, sounds, log):
        self.game = game
        self.logSectionName = "pauseMenu"
        super().__init__(screen, keys, config, sounds, log)

    def onEscape(self):
        self.unpause()

    def doAdditionalClosingOperations(self):
        self.game.running = False

    def unpause(self):
        self.modlogger.info("Game unPaused")
        self.running = False
        pygame.mouse.set_visible(False)
        self.modlogger.debug("Mouse cursor hidden")

    def makeResumeItem(self):
        self.resgame = textMenuItem("Resume Game", (50, 240),
                                    lambda: self.editDesc(
                                             "Resume the paused Game"),
                                    lambda: self.unpause(),
                                    self.config, self.sounds, self.font)
        self.activeItems.append(self.resgame)
        self.items.append(self.resgame)

    def makeSaveGameItem(self):
        self.savegame = textMenuItem("Save Game", (50, 320),
                                     lambda: self.editDesc(
                                              "Save for safety"),
                                     lambda: saveGameMenu(
                                         self.screen, self.keys, self.config,
                                         self.sounds, self.mainLogger,
                                         self.game).mainLoop(),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.savegame)
        self.items.append(self.savegame)

    def makeQuitItem(self):
        self.exit = textMenuItem("Quit to Desktop", (50, 560),
                                 lambda: self.editDesc(
                                          "Outta Here, NOW!!"),
                                 lambda: pygame.event.post(
                                        pygame.event.Event(pygame.QUIT)),
                                 self.config, self.sounds, self.font)
        self.activeItems.append(self.exit)
        self.items.append(self.exit)

    def makeMainMenuItem(self):
        self.mainmenu = textMenuItem("Main Menu", (50, 400),
                                     lambda: self.editDesc(
                                              "Get back to the main menu"),
                                     lambda: self.goToMenu(),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.mainmenu)
        self.items.append(self.mainmenu)

    def makeMenuItems(self):
        self.makeResumeItem()
        self.makeSaveGameItem()
        self.makeMainMenuItem()
        self.makeQuitItem()
