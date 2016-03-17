# Modifiers Menu Component
# Part of the Glitch_Heaven Project
# Copyright 2015 Penaz <penazarea@altervista.org>
from components.UI.menu import menu
from libs.textglitcher import makeGlitched
from components.UI import menuItem

class modMenu(menu):

    def __init__(self, screen, keys, config, sounds, modifiers):
        self.logSectionName = "Glitch_Heaven.ModifiersMenu"
        self.modifiers = modifiers
        super().__init__(screen, keys, config, sounds)
        
    def toggleModifier(self, mod):
        self.modifiers[mod] = not self.modifiers[mod]
        self.modlogger.info("Toggled modifier {0}, current status {1}".format(
            mod, self.modifiers[mod]))
            
    def makeMainMenuItem(self):
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Previous Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Previous Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (600, 560),
                                          lambda: self.editDesc(
                                              "Go to the main menu"),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          self.sounds)
        self.activeItems.append(self.mainmenu)
        self.items.append(self.mainmenu)
        # ^------------------------------------------------------------------^
        
    def makeChaosToggle(self):
        self.chaosimg = self.font.render("Chaos Mode",
                                         False, (255, 255, 255)).convert_alpha()
        self.chaossel = makeGlitched("Chaos Mode", self.font)
        self.chaos = menuItem.menuitem(self.chaosimg,
                                       self.chaossel,
                                       (50, 180),
                                       lambda: self.editDesc("Current Status: {0}".format(
                                            self.modifiers["chaos"])),
                                       lambda: self.toggleModifier("chaos"),
                                       self.config,
                                       self.sounds)
        self.activeItems.append(self.chaos)
        self.items.append(self.chaos)
        
    def makeVFlipToggle(self):
        self.vflipimg = self.font.render("Vertical Flip Mode",
                                         False, (255, 255, 255)).convert_alpha()
        self.vflipsel = makeGlitched("Vertical Flip Mode", self.font)
        self.vflip = menuItem.menuitem(self.vflipimg,
                                       self.vflipsel,
                                       (50, 240),
                                       lambda: self.editDesc("Current Status: {0}".format(
                                            self.modifiers["vflip"])),
                                       lambda: self.toggleModifier("vflip"),
                                       self.config,
                                       self.sounds)
        self.activeItems.append(self.vflip)
        self.items.append(self.vflip)
        
    def makeHFlipToggle(self):
            self.hflipimg = self.font.render("Horizontal Flip Mode",
                                             False, (255, 255, 255)).convert_alpha()
            self.hflipsel = makeGlitched("Horizontal Flip Mode", self.font)
            self.hflip = menuItem.menuitem(self.hflipimg,
                                           self.hflipsel,
                                           (50, 300),
                                           lambda: self.editDesc("Current Status: {0}".format(
                                                self.modifiers["hflip"])),
                                           lambda: self.toggleModifier("hflip"),
                                           self.config,
                                           self.sounds)
            self.activeItems.append(self.hflip)
            self.items.append(self.hflip)

    def makeMenuItems(self):
        self.makeChaosToggle()
        self.makeVFlipToggle()
        self.makeHFlipToggle()
        self.makeMainMenuItem()