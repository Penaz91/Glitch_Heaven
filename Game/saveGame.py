# Load Game Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.loadmenu import loadMenu
from os import listdir
from os.path import join as pjoin
from components.UI.textMenuItem import textMenuItem
from components.UI.textinput import textInput
import json


class saveGameMenu(loadMenu):

    def __init__(self, screen, keys, config, sounds, log, game):
        self.logSectionName = "saveGameMenu"
        self.gameInstance = game
        self.dirlist = sorted(listdir(pjoin("savegames")))
        super().__init__(screen, keys, config, sounds, log)

    def saveGame(self, savegame):
        path = pjoin("savegames", savegame)
        if not (self.gameInstance.gameStatus["mode"] in ["criticalfailure",
                                                         "cfsingle"]):
            self.gameInstance.gameStatus["cftime"] = 0
            self.gameInstance.gameStatus["time"] = 0
            self.gameInstance.gameStatus["mode"] = "newgame"
        self.modlogger.debug("Saved with data: {0}"
                             % self.gameInstance.gameStatus)
        with open(path, "w") as savefile:
            savefile.write(json.dumps(self.gameInstance.gameStatus))
            self.modlogger.info("Game saved on the file: \
                    %(savefile)s" % locals())
        self.running = False

    def makeNewSave(self):
        name = textInput(self.screen, self.font,
                         "Write the name of the new Save").get_input()
        if name is not None:
            name += ".dat"
            self.saveGame(name)

    def makeSaveItem(self):
        self.savegame = textMenuItem("Overwrite", (250, 560),
                                     lambda: self.editDesc(
                                         "Overwrite the selected savegame"),
                                     lambda: self.saveGame(
                                         self.dirlist[self.id]),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.savegame)
        self.items.append(self.savegame)

    def makeNewSaveItem(self):
        self.newsavegame = textMenuItem("Create New", (400, 560),
                                        lambda: self.editDesc(
                                         "Create a new SaveGame"),
                                        lambda: self.makeNewSave(),
                                        self.config, self.sounds, self.font)
        self.activeItems.append(self.newsavegame)
        self.items.append(self.newsavegame)

    def makeMenuItems(self):
        self.makeLeftArrow()
        self.makeRightArrow()
        self.makeSaveItem()
        self.makeNewSaveItem()
        self.makeMainMenuItem()
