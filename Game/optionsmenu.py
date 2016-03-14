# Options Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
from components.UI import menuItem
from videosettings import VideoSettings
from audiosettings import AudioSettings
from controlsettings import ControlSettings
from libs.textglitcher import makeGlitched
from components.UI.menu import menu


class OptionsMenu (menu):
    """ Represents a pause menu window"""

    def __init__(self, screen, keys, config, sounds):
        self.logSectionName = "Glitch_Heaven.OptionsMenu"
        super().__init__(screen, keys, config, sounds)

    def makeVideoSettingsMenuItem(self):
        # Video Settings menu element
        # v------------------------------------------------------------------v
        self.videoimg = self.font.render("Video Settings", False,
                                         (255, 255, 255)).convert_alpha()
        self.vidselimg = makeGlitched("Video Settings", self.font)
        self.video = menuItem.menuitem(self.videoimg,
                                       self.vidselimg,
                                       (50, 240),
                                       lambda: self.editDesc(
                                           "Customize your eye disappeal"),
                                       lambda: VideoSettings(
                                           self.screen,
                                           self.keys,
                                           self.config,
                                           self.sounds
                                           ).mainLoop(),
                                       self.config,
                                       self.sounds)
        self.activeItems.append(self.video)
        self.items.append(self.video)

    def makeSoundSettingsMenuItem(self):
        # ^------------------------------------------------------------------^
        # Sound settings menu element
        # v------------------------------------------------------------------v
        self.sndimg = self.font.render("Audio Settings", False,
                                       (255, 255, 255)).convert_alpha()
        self.sndselimg = makeGlitched("Audio Settings", self.font)
        self.snd = menuItem.menuitem(self.sndimg,
                                     self.sndselimg,
                                     (50, 320),
                                     lambda: self.editDesc(
                                         "Avoid deafening with these controls"
                                         ),
                                     lambda: AudioSettings(
                                         self.screen,
                                         self.keys,
                                         self.config,
                                         self.sounds).mainLoop(),
                                     self.config,
                                     self.sounds)
        self.items.append(self.snd)
        self.activeItems.append(self.snd)

    def makeControlSettingsMenuItem(self):
        # ^------------------------------------------------------------------^
        # Controls/Controllers menu element
        # v------------------------------------------------------------------v
        self.ctrlimg = self.font.render("Control Settings",
                                        False, (255, 255, 255)).convert_alpha()
        self.ctrlselimg = makeGlitched("Control Settings", self.font)
        self.ctrl = menuItem.menuitem(self.ctrlimg,
                                      self.ctrlselimg,
                                      (50, 400),
                                      lambda: self.editDesc(
                                          "Edit keyboard/joypad settings"),
                                      lambda: ControlSettings(
                                          self.screen,
                                          self.keys, self.config,
                                          self.sounds
                                          ).mainLoop(),
                                      self.config,
                                      self.sounds)
        self.items.append(self.ctrl)
        self.activeItems.append(self.ctrl)

    def makeMainMenuItem(self):
        # ^------------------------------------------------------------------^
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Main Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Main Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (650, 560),
                                          lambda: self.editDesc(
                                              "Go to the main menu"),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          self.sounds)
        self.items.append(self.mainmenu)
        self.activeItems.append(self.mainmenu)

    def makeMenuItems(self):
        self.makeVideoSettingsMenuItem()
        self.makeSoundSettingsMenuItem()
        self.makeControlSettingsMenuItem()
        self.makeMainMenuItem()
