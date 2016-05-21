# Load Game Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI import menuItem
from libs.textglitcher import makeGlitched
from os import listdir
from os.path import join as pjoin
import json
import pygame


class loadMenu(menu):

    def __init__(self, screen, keys, config, sounds, log):
        self.logSectionName = "loadGameMenu"
        self.dirlist = sorted(listdir(pjoin("savegames")))
        self.font = pygame.font.Font(pjoin(
                            "resources", "fonts",
                            "TranscendsGames.otf"), 24)
        self.id = 0
        self.oldid = -1
        super().__init__(screen, keys, config, sounds, log)

    def makeMainMenuItem(self):
        self.menu = self.font.render("Main Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Main Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (50, 560),
                                          lambda: self.editDesc(
                                              "Go to the main menu"),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.mainmenu)
        self.items.append(self.mainmenu)

    def makeMenuItems(self):
        self.makeMainMenuItem()
        
    def doMoreLoopOperations(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.id = (self.id - 1) % len(self.dirlist)
        if keys[pygame.K_RIGHT]:
            self.id = (self.id + 1) % len(self.dirlist)

    def doAdditionalBlits(self):
        if self.oldid != self.id and self.dirlist is not None:
            self.n = self.font.render(self.dirlist[self.id], False, (255, 255, 255)).convert_alpha()
            self.nl1 = self.font.render(self.dirlist[(self.id - 1) % len(self.dirlist)], False, (128, 128, 128)).convert_alpha()
            self.nl2 = self.font.render(self.dirlist[(self.id - 2) % len(self.dirlist)], False, (64, 64, 64)).convert_alpha()
            self.np1 = self.font.render(self.dirlist[(self.id + 1) % len(self.dirlist)], False, (128, 128, 128)).convert_alpha()
            self.np2 = self.font.render(self.dirlist[(self.id + 2) % len(self.dirlist)], False, (64, 64, 64)).convert_alpha()
            self.oldid = self.id
        if self.dirlist is not None:
            self.screen.blit(self.nl2, (50, 260))
            self.screen.blit(self.nl1, (50, 290))
            self.screen.blit(self.n, (50, 320))
            self.screen.blit(self.np1, (50, 350))
            self.screen.blit(self.np2, (50, 380))
