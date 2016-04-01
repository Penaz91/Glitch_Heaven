# Video Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI import menuItem
from libs.textglitcher import makeGlitched


class VideoSettings(menu):

    def __init__(self, screen, keys, config, sounds):
        self.logSectionName = "Glitch_Heaven.VideoSettings"
        super().__init__(screen, keys, config, sounds)

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

    def makeMenuItems(self):
        self.line = self.font.render("Video settings are not" +
                                     " available in this version",
                                     False,
                                     (255, 255, 255))
        self.makeMainMenuItem()

    def doAdditionalBlits(self):
        self.screen.blit(self.line, (100, 200))
