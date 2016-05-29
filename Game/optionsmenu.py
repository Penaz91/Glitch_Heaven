# Options Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015-2016 Penaz <penazarea@altervista.org>
from components.UI import menuItem
from videosettings import VideoSettings
from audiosettings import AudioSettings
from keyboardsettings import KeyboardSettings
from libs.textglitcher import makeGlitched
from components.UI.menu import menu
from components.UI.textMenuItem import textMenuItem


class OptionsMenu (menu):
    """ Represents a pause menu window"""

    def __init__(self, screen, keys, config, sounds, log):
        self.logSectionName = "optionsMenu"
        super().__init__(screen, keys, config, sounds, log)

    def makeVideoSettingsMenuItem(self):
        self.video = textMenuItem("Video Settings", (50, 240),
                                  lambda: self.editDesc(
                                           "Customize your eye disappeal"),
                                  lambda: VideoSettings(
                                           self.screen, self.keys,
                                           self.config, self.sounds,
                                           self.mainLogger,).mainLoop(),
                                  self.config, self.sounds, self.font)
        self.activeItems.append(self.video)
        self.items.append(self.video)

    def makeSoundSettingsMenuItem(self):
        self.snd = textMenuItem("Audio Settings", (50, 320),
                                lambda: self.editDesc(
                                         "Avoid deafening with these controls"
                                         ),
                                lambda: AudioSettings(
                                         self.screen, self.keys,
                                         self.config, self.sounds,
                                         self.mainLogger).mainLoop(),
                                self.config, self.sounds, self.font)
        self.items.append(self.snd)
        self.activeItems.append(self.snd)

    def makeControlSettingsMenuItem(self):
        self.ctrl = textMenuItem("Keyboard Settings", (50, 400),
                                 lambda: self.editDesc(
                                              "Edit Keyboard assignments"),
                                 lambda: KeyboardSettings(
                                              self.screen, self.keys,
                                              self.config, self.sounds,
                                              self.mainLogger).mainLoop(),
                                 self.config, self.sounds, self.font)
        self.items.append(self.ctrl)
        self.activeItems.append(self.ctrl)

    def makeMainMenuItem(self):
        self.mainmenu = textMenuItem("Main Menu", (650, 560),
                                     lambda: self.editDesc(
                                              "Go to the main menu"),
                                     lambda: self.goToMenu(),
                                     self.config, self.sounds, self.font)
        self.items.append(self.mainmenu)
        self.activeItems.append(self.mainmenu)

    def makeMenuItems(self):
        self.makeVideoSettingsMenuItem()
        self.makeSoundSettingsMenuItem()
        self.makeControlSettingsMenuItem()
        self.makeMainMenuItem()
