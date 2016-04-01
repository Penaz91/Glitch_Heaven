# Audio Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI import menuItem
from libs.textglitcher import makeGlitched
from components.UI import meter
import pygame


class AudioSettings(menu):

    def __init__(self, screen, keys, config, sounds):
        self.logSectionName = "Glitch_Heaven.AudioSettings"
        super().__init__(screen, keys, config, sounds)

    def makeMeters(self):
        self.menumeter = meter.Meter((320, 250), (200, 10),
                                     self.config, "menuvolume",
                                     self.sounds)
        self.menuwriting = self.font.render("Menu Volume: ", False,
                                            (255, 255, 255)).convert_alpha()
        self.sfxmeter = meter.Meter((320, 330), (200, 10),
                                    self.config, "sfxvolume",
                                    self.sounds)
        self.sfxwriting = self.font.render("SFX Volume: ", False,
                                           (255, 255, 255)).convert_alpha()
        self.musicmeter = meter.Meter((320, 410), (200, 10),
                                      self.config, "musicvolume",
                                      self.sounds)
        self.musicwriting = self.font.render("Music Volume: ", False,
                                             (255, 255, 255)).convert_alpha()
        self.meters = [self.menumeter, self.sfxmeter, self.musicmeter]

    def makePreviousMenuItem(self):
        self.menu = self.font.render("Apply and go back",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Apply and go back", self.font)
        self.prevmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (50, 560),
                                          lambda: None,
                                          lambda: self.goToMenu(),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.prevmenu)
        self.items.append(self.prevmenu)

    def makeMenuItems(self):
        self.makePreviousMenuItem()
        self.makeMeters()

    def doAdditionalMouseHandling(self):
        mousepos = pygame.mouse.get_pos()
        for item in self.meters:
            if item.rect.collidepoint(*mousepos):
                self.amount = item.set_quantity(mousepos)
                self.modlogger.debug("Meter set to: {0}"
                                     .format(str(self.amount)))

    def doAdditionalBlits(self):
        for item in self.meters:
            item.draw(self.screen)
        self.screen.blit(self.menuwriting, (190, 240))
        self.screen.blit(self.sfxwriting, (190, 320))
        self.screen.blit(self.musicwriting, (190, 400))

    def doAdditionalClosingOperations(self):
        for sound in self.sounds["menu"]:
            self.sounds["menu"][sound].set_volume((
                self.config.getfloat("Sound",
                                     "menuvolume"))/100)
        for sound in self.sounds["sfx"]:
            self.sounds["sfx"][sound].set_volume(
                    (self.config.getfloat("Sound",
                                          "sfxvolume"))/100)
        for sound in self.sounds["music"]:
            self.sounds["music"][sound].set_volume(
                    (self.config.getfloat("Sound",
                                          "musicvolume"))/100)
