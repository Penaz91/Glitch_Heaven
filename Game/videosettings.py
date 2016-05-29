# Video Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI import menuItem
from libs.textglitcher import makeGlitched
from components.UI.textMenuItem import textMenuItem
import json


class VideoSettings(menu):

    def __init__(self, screen, keys, config, sounds, log):
        self.logSectionName = "videoSettings"
        super().__init__(screen, keys, config, sounds, log)

    def toggle(self, option):
        self.config["Video"][option] = not self.config["Video"][option]
        with open("config.json", "w") as conf:
            conf.write(json.dumps(self.config, indent=4))

    def makePlayerParticlesItem(self):
        self.partitem = textMenuItem("Player Particles", (50, 180),
                                     lambda: self.editDesc(
                                        "Current Status: {0}".format(
                                         self.config["Video"]["playerparticles"])),
                                     lambda: self.toggle("playerparticles"),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.partitem)
        self.items.append(self.partitem)

    def makeDeathCounterItem(self):
        self.DCitem = textMenuItem("Death Counter Visible", (50, 240),
                                   lambda: self.editDesc(
                                        "Current Status: {0}".format(
                                         self.config["Video"]["deathcounter"])),
                                     lambda: self.toggle("deathcounter"),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.DCitem)
        self.items.append(self.DCitem)

    def makeMainMenuItem(self):
        self.mainmenu = textMenuItem("Main Menu", (50, 560),
                                     lambda: self.editDesc(
                                        "Go to the main menu"),
                                     lambda: self.goToMenu(),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.mainmenu)
        self.items.append(self.mainmenu)

    def makeMenuItems(self):
        self.makePlayerParticlesItem()
        self.makeDeathCounterItem()
        self.makeMainMenuItem()