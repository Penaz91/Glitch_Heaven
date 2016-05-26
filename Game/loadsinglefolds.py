# Load Single Map (Folder part) Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>

# WILL BE DEPRECATED IN FAVOR OF A GENERIC + INHERITED VERSION
from components.UI.menu import menu
from components.UI import menuItem
from libs.textglitcher import makeGlitched
from os import listdir, isdir
from os.path import join as pjoin
import pygame
# from game import Game


class loadSingleFoldMenu(menu):
    white = (255, 255, 255)
    grey = (128, 128, 128)
    dgrey = (64, 64, 64)

    def __init__(self, screen, keys, config, sounds, modifiers, log):
        self.logSectionName = "loadSingleFoldMenu"
        self.modifiers = modifiers
        directory = pjoin("data", "maps")
        self.dirlist = sorted(
                [name for name in listdir(directory)
                    if isdir(pjoin(directory, name))])
        self.font = pygame.font.Font(pjoin(
                            "resources", "fonts",
                            "TranscendsGames.otf"), 24)
        self.id = 0
        self.time = .1
        self.n, self.nl1, self.nl2, self.np1, self.np2 = 5*[None]
        if self.dirlist is not None:
            self.updateOperation = self.update_yes
        else:
            self.updateOperation = self.update_no
        self.updateOperation()
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

    def makeLoadItem(self):
        self.load = self.font.render("Open",
                                     False, (255, 255, 255)).convert_alpha()
        self.loadsel = makeGlitched("Open", self.font)
        self.loadgame = menuItem.menuitem(self.load,
                                          self.loadsel,
                                          (250, 560),
                                          lambda: self.editDesc(
                                              "Explore this directory"),
                                          lambda: self.loadGame(
                                              self.dirlist[self.id]
                                              ),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.loadgame)
        self.items.append(self.loadgame)

    def addN(self):
        self.id = (self.id + 1) % len(self.dirlist)
        self.updateOperation = self.update_yes

    def lessN(self):
        self.id = (self.id - 1) % len(self.dirlist)
        self.updateOperation = self.update_yes

    def makeLeftArrow(self):
        self.leftimg = pygame.transform.flip(self.font.render("v", False,
                                             (255, 255, 255)).convert_alpha(),
                                             False, True)
        self.leftsel = pygame.transform.flip(makeGlitched("v", self.font),
                                             False, True)
        self.left = menuItem.menuitem(self.leftimg,
                                      self.leftsel,
                                      (50, 260),
                                      lambda: self.editDesc(
                                          "Previous savegame"),
                                      lambda: self.lessN(),
                                      self.config,
                                      self.sounds)
        self.items.append(self.left)
        self.activeItems.append(self.left)

    def makeRightArrow(self):
        self.rightimg = self.font.render("v", False,
                                         (255, 255, 255)).convert_alpha()
        self.rightsel = makeGlitched("v", self.font)
        self.right = menuItem.menuitem(self.rightimg,
                                       self.rightsel,
                                       (50, 380),
                                       lambda: self.editDesc(
                                           "Next savegame"),
                                       lambda: self.addN(),
                                       self.config,
                                       self.sounds)
        self.items.append(self.right)
        self.activeItems.append(self.right)

    def makeMenuItems(self):
        self.makeLeftArrow()
        self.makeRightArrow()
        self.makeLoadItem()
        self.makeMainMenuItem()

    def update_no(self):
        pass

    def update_yes(self):
        self.n = self.font.render(self.dirlist[self.id],
                                  False, self.white).convert_alpha()
        lun = len(self.dirlist)
        num1 = (self.id - 1) % lun
        num2 = (self.id - 2) % lun
        num3 = (self.id + 1) % lun
        num4 = (self.id + 2) % lun
        self.nl1 = self.font.render(self.dirlist[num1],
                                    False, self.grey).convert_alpha()
        self.nl2 = self.font.render(self.dirlist[num2],
                                    False, self.dgrey).convert_alpha()
        self.np1 = self.font.render(self.dirlist[num3],
                                    False, self.grey).convert_alpha()
        self.np2 = self.font.render(self.dirlist[num4],
                                    False, self.dgrey).convert_alpha()
        self.updateOperation = self.update_no

    def doMoreLoopOperations(self):
        keys = pygame.key.get_pressed()
        if self.time <= 0:
            if keys[pygame.K_LEFT]:
                self.lessN()
            if keys[pygame.K_RIGHT]:
                self.addN()
            self.time = .1

    def doAdditionalBlits(self):
        self.updateOperation()
        self.time -= self.dt
        if self.dirlist is not None:
            self.screen.blit(self.nl2, (150, 260))
            self.screen.blit(self.nl1, (150, 290))
            self.screen.blit(self.n, (150, 320))
            self.screen.blit(self.np1, (150, 350))
            self.screen.blit(self.np2, (150, 380))
