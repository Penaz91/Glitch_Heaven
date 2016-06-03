# Load Single Map (File part) Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.loadmenu import loadMenu
from components.UI import menuItem
from libs.textglitcher import makeGlitched
from os import listdir
from os.path import join as pjoin
from game import Game


class loadSingleFileMenu(loadMenu):

    def __init__(self, screen, keys, config, sounds, modifiers, log, fold):
        self.logSectionName = "loadSingleFoldMenu"
        self.modifiers = modifiers
        self.directory = pjoin("data", "maps", fold)
        self.dirlist = sorted(listdir(self.directory))
        self.dirlist = [fi for fi in self.dirlist if fi.endswith(".tmx")]
        super().__init__(screen, keys, config, sounds, log)

    def openMap(self, name):
            self.running = False
            Game().main(self.screen, self.keys, "singlemap",
                        pjoin(self.directory, name), self.config, self.sounds,
                        self.modifiers, self.mainLogger)

    def makeLoadItem(self):
        self.load = self.font.render("Open",
                                     False, (255, 255, 255)).convert_alpha()
        self.loadsel = makeGlitched("Open", self.font)
        self.loadgame = menuItem.menuitem(self.load,
                                          self.loadsel,
                                          (250, 560),
                                          lambda: self.editDesc(
                                              "Open This map"),
                                          lambda: self.openMap(
                                              self.dirlist[self.id][:-4]),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.loadgame)
        self.items.append(self.loadgame)
