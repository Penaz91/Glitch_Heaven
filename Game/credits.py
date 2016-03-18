# Credits Screen Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from components.UI import menuItem
from libs.textglitcher import makeGlitched


class Credits(menu):

    def __init__(self, screen, keys, config, sounds):
        self.texts = []
        self.logSectionName = "Glitch_Heaven.CreditsMenu"
        super(Credits, self).__init__(screen, keys, config, sounds)

    def makeMainMenuItem(self):
        self.menu = self.font.render("Main Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Main Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (320, 560),
                                          lambda: self.editDesc(
                                              "Go to the main menu"),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          self.sounds)
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
                (makeGlitched("Dexter561, ScansPlays and AstralGemini", self.font),
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
