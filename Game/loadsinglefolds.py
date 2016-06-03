# Load Single Map (Folder part) Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.loadmenu import loadMenu
from components.UI import menuItem
from libs.textglitcher import makeGlitched
from os import listdir
from os.path import isdir
from os.path import join as pjoin
from loadsingleFiles import loadSingleFileMenu


class loadSingleFoldMenu(loadMenu):
    def __init__(self, screen, keys, config, sounds, modifiers, log):
        self.logSectionName = "loadSingleFoldMenu"
        self.modifiers = modifiers
        directory = pjoin("data", "maps")
        self.dirlist = sorted(
                [name for name in listdir(directory)
                    if isdir(pjoin(directory, name))])
        super().__init__(screen, keys, config, sounds, log)

    def makeLoadItem(self):
        self.load = self.font.render("Open",
                                     False, (255, 255, 255)).convert_alpha()
        self.loadsel = makeGlitched("Open", self.font)
        self.loadgame = menuItem.menuitem(self.load,
                                          self.loadsel,
                                          (250, 560),
                                          lambda: self.editDesc(
                                              "Explore this directory"),
                                          lambda: loadSingleFileMenu(
                                              self.screen, self.keys,
                                              self.config, self.sounds,
                                              self.modifiers, self.mainLogger,
                                              self.dirlist[self.id]
                                              ).mainLoop(),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.loadgame)
        self.items.append(self.loadgame)
