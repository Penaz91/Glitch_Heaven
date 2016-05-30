# Credits Screen Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from libs.textglitcher import makeGlitched
from components.UI.textMenuItem import textMenuItem


class Credits(menu):

    def __init__(self, screen, keys, config, sounds, log):
        self.texts = []
        self.logSectionName = "creditsMenu"
        super(Credits, self).__init__(screen, keys, config, sounds, log)

    def makeMainMenuItem(self):
        self.mainmenu = textMenuItem("Previous Menu", (320, 560),
                                     lambda: self.editDesc(
                                              "Go to the previous menu"),
                                     lambda: self.goToMenu(),
                                     self.config, self.sounds, self.font)
        self.activeItems.append(self.mainmenu)
        self.items.append(self.mainmenu)

    def makeCreditText(self):
        self.texts = [
                ((self.font.render("Glitch_Heaven, a game by:",
                                   False,
                                   (255, 255, 255))).convert_alpha(),
                 (50, 100)),
                (makeGlitched("Penaz", self.font),
                    (50, 120)),
                ((self.font.render("Thanks to:",
                                   False,
                                   (255, 255, 255))).convert_alpha(),
                 (50, 150)),
                (makeGlitched("Dexter561, ScansPlays and AstralGemini",
                              self.font),
                    (50, 170)),
                ((self.font.render("--- Special Thanks ---",
                                   False,
                                   (255, 255, 255))).convert_alpha(),
                 (50, 220)),
                ((self.font.render("[Many names to be put here in the future]",
                                   False,
                                   (255, 255, 255))).convert_alpha(),
                 (50, 240))
                ]

    def makeMenuItems(self):
        self.modlogger.info("Creating Credits menu items")
        self.makeCreditText()
        self.makeMainMenuItem()

    def doAdditionalBlits(self):
        for text in self.texts:
            self.screen.blit(*text)
