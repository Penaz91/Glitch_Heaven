# Load Game Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.loadmenu import loadMenu
from os import listdir
from os.path import join as pjoin
from game import Game
from components.UI.textMenuItem import textMenuItem


class loadSaveMenu(loadMenu):

    def __init__(self, screen, keys, config, sounds, log):
        self.logSectionName = "loadGameMenu"
        self.dirlist = sorted(listdir(pjoin("savegames")))
        super().__init__(screen, keys, config, sounds, log)

    def loadGame(self, savegame):
        print(pjoin("savegames", savegame))
        Game().main(self.screen,
                    self.keys,
                    "load",
                    pjoin("savegames", savegame),
                    self.config,
                    self.sounds,
                    None,
                    self.mainLogger)
        self.running = False

    def makeLoadItem(self):
        self.loadgame = textMenuItem("Load", (250, 560),
                                     lambda: self.editDesc(
                                         "Load the selected savegame"),
                                     lambda: self.loadGame(
                                         self.dirlist[self.id]),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.loadgame)
        self.items.append(self.loadgame)
