# Load Save Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI import menuItem
from libs.textglitcher import makeGlitched
from dirlist import dirList
from os.path import join as pjoin
from game import Game


class loadMenu(menu):

    def __init__(self, screen, keys, config, sounds, log):
        self.logSectionName = "loadGameMenu"
        self.dirlist = dirList(pjoin("savegames"), False, config, sounds)
        self.dirlist.location = (50, 150)
        super().__init__(screen, keys, config, sounds, log)

    def doAdditionalMotionHandling(self):
        self.dirlist.checkMouseHover()

    def doExternalClickHandling(self):
        self.dirlist.checkMouseClick()

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

    def loadGame(self, savegame):
        Game().main(self.screen,
                    self.keys,
                    "load",
                    pjoin("savegames", savegame),
                    self.config,
                    self.sounds,
                    None,
                    self.mainLogger),

    def makeLoadItem(self):
        self.load = self.font.render("Load",
                                     False, (255, 255, 255)).convert_alpha()
        self.loadsel = makeGlitched("Load", self.font)
        self.loadgame = menuItem.menuitem(self.load,
                                          self.loadsel,
                                          (150, 560),
                                          lambda: self.editDesc(
                                              "Load the selected savegame"),
                                          lambda: self.loadGame(
                                              self.dirlist.selectedItem.special
                                              ),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.loadgame)
        self.items.append(self.loadgame)

    def makeMenuItems(self):
        self.makeLoadItem()
        self.makeMainMenuItem()

    def doAdditionalBlits(self):
        self.dirlist.update()
        print(self.dirlist.selectedItem)
        self.screen.blit(self.dirlist.surface, self.dirlist.location)
