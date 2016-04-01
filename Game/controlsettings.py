# Control Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI import menuItem
from libs.textglitcher import makeGlitched
from keyboardsettings import KeyboardSettings
from components.UI.menu import menu


class ControlSettings(menu):
    """ Represents a pause menu window"""

    def __init__(self, screen, keys, config, sounds):
        self.logSectionName = "Glitch_Heaven.ControlSettings"
        super().__init__(screen, keys, config, sounds)

    def makeKeyboardMenu(self):
        self.keybimg = self.font.render("Keyboard Settings", False,
                                        (255, 255, 255)).convert_alpha()
        self.keybselimg = makeGlitched("Keyboard Settings", self.font)
        self.keyboard = menuItem.menuitem(self.keybimg,
                                          self.keybselimg,
                                          (50, 240),
                                          lambda: self.editDesc(
                                              "Edit Keyboard assignments"),
                                          lambda: KeyboardSettings(
                                              self.screen,
                                              self.keys,
                                              self.config,
                                              self.sounds).mainLoop(),
                                          self.config,
                                          self.sounds
                                          )
        self.activeItems.append(self.keyboard)
        self.items.append(self.keyboard)

    def makeJoypadMenu(self):
        self.joyimg = self.font.render("Joypad Settings", False,
                                       (255, 255, 255)).convert_alpha()
        self.joyselimg = makeGlitched("Joypad Settings", self.font)
        self.joypad = menuItem.menuitem(self.joyimg,
                                        self.joyselimg,
                                        (50, 380),
                                        lambda: self.editDesc(
                                            "Edit Joypad Assignments"),
                                        lambda: None,
                                        self.config,
                                        self.sounds
                                        )
        self.activeItems.append(self.joypad)
        self.items.append(self.joypad)

    def makeMainMenuItem(self):
        # ^------------------------------------------------------------------^
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Previous Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Previous Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (50, 560),
                                          lambda: self.editDesc(
                                              "Go back to the previous menu"),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          self.sounds)
        self.items.append(self.mainmenu)
        self.activeItems.append(self.mainmenu)
        # ^------------------------------------------------------------------^

    def makeMenuItems(self):
        self.makeKeyboardMenu()
        self.makeJoypadMenu()
        self.makeMainMenuItem()
