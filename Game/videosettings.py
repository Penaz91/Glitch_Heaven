# Video Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI.textMenuItem import textMenuItem
from pygame import FULLSCREEN, HWSURFACE, DOUBLEBUF
from pygame.display import set_mode
import json


class VideoSettings(menu):

    def __init__(self, screen, keys, config, sounds, log):
        self.logSectionName = "videoSettings"
        super().__init__(screen, keys, config, sounds, log)

    def toggle(self, option):
        self.config["Video"][option] = not self.config["Video"][option]
        with open("config.json", "w") as conf:
            conf.write(json.dumps(self.config, indent=4))
            
    def fullscreenDirectChange(self):
        self.toggle("fullscreen")
        self.modlogger.info("Parsing configuration file")
        screensize = (int(self.config["Video"]["screenwidth"]),
                      int(self.config["Video"]["screenheight"]))
        self.modlogger.debug("Screensize set to: " + str(screensize))
        fullscreen = self.config["Video"]["fullscreen"]
        self.modlogger.debug("Fullscreen Flag Set to: "+str(fullscreen))
        doublebuffer = self.config["Video"]["fullscreen"]
        self.modlogger.debug("Doublebuffer Flag set to: " +
                     str(doublebuffer))
        flags = None
        self.modlogger.info("Setting screen flags")
        if fullscreen:
            if doublebuffer:
                flags = FULLSCREEN | HWSURFACE | DOUBLEBUF
            else:
                flags = FULLSCREEN | HWSURFACE
        else:
            flags = 0
        self.screen = set_mode(screensize, flags)

    def makePlayerParticlesItem(self):
        self.partitem = textMenuItem("Player Particles", (50, 180),
                                     lambda: self.editDesc(
                                        "Current Status: {0}".format(
                                         self.config["Video"][
                                             "playerparticles"])),
                                     lambda: self.toggle("playerparticles"),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.partitem)
        self.items.append(self.partitem)

    def makeDeathCounterItem(self):
        self.DCitem = textMenuItem("Death Counter Visible", (50, 240),
                                   lambda: self.editDesc(
                                        "Current Status: {0}".format(
                                         self.config["Video"][
                                             "deathcounter"])),
                                   lambda: self.toggle("deathcounter"),
                                   self.config, self.sounds, self.font)
        self.activeItems.append(self.DCitem)
        self.items.append(self.DCitem)

    def makeFullscreenItem(self):
        self.FSitem = textMenuItem("Full Screen", (50, 300),
                                   lambda: self.editDesc(
                                        "Current Status: {0}".format(
                                         self.config["Video"][
                                             "fullscreen"])),
                                   lambda: self.fullscreenDirectChange(),
                                   self.config, self.sounds, self.font)
        self.activeItems.append(self.FSitem)
        self.items.append(self.FSitem)
        
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
        self.makeFullscreenItem()
        self.makeMainMenuItem()
