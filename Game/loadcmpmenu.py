# Load Campaign Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.loadmenu import loadMenu
from components.UI import menuItem
from libs.textglitcher import makeGlitched
from os import listdir
from os.path import join as pjoin
from game import Game


class loadCmpMenu(loadMenu):

    def __init__(self, screen, keys, config, sounds, modifiers, log):
        self.logSectionName = "loadCampaignMenu"
        self.modifiers = modifiers
        self.dirlist = sorted(listdir(pjoin("data", "campaigns")))
        super().__init__(screen, keys, config, sounds, log)

    def loadGame(self, name):
        Game().main(self.screen,
                    self.keys,
                    "newgame",
                    pjoin("data", "campaigns", name),
                    self.config,
                    self.sounds,
                    self.modifiers,
                    self.mainLogger)
        self.running = False

    def makeLoadItem(self):
        self.load = self.font.render("Load",
                                     False, (255, 255, 255)).convert_alpha()
        self.loadsel = makeGlitched("Load", self.font)
        self.loadgame = menuItem.menuitem(self.load,
                                          self.loadsel,
                                          (250, 560),
                                          lambda: self.editDesc(
                                              "Load the selected campaign"),
                                          lambda: self.loadGame(
                                              self.dirlist[self.id]
                                              ),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.loadgame)
        self.items.append(self.loadgame)
