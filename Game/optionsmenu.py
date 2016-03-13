# Options Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os
from components.UI import menuItem
from libs import animation, timedanimation
from videosettings import VideoSettings
from audiosettings import AudioSettings
from controlsettings import ControlSettings
import logging
from logging import handlers as loghandler
from os.path import join as pathjoin
from libs.textglitcher import makeGlitched
module_logger = logging.getLogger("Glitch_Heaven.OptionsMenu")
fh = loghandler.TimedRotatingFileHandler(pathjoin("logs", "Game.log"),
                                         "midnight", 1)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                              ' %(levelname)s --- %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
module_logger.addHandler(fh)
module_logger.addHandler(ch)


class OptionsMenu:
    """ Represents a pause menu window"""

    def editdesc(self, string):
        self.desc = makeGlitched(string, self.font)

    def goToMenu(self):
        """
        Kills the current game and menu instance, and returns
        To the main menu, which is already running in BG.

        Keyword Arguments:
        - game: The game instance

        Returns:
        - Nothing
        """
        self.running = False
        module_logger.info("Going to the previous Menu")

    def main(self, screen, keys, config, sounds):
        """
        The main method to show and make the menu work

        Keyword Arguments:
        - Screen: the Screen surface to make the menu on
        - Keys: The list of control keys to use
        - Config: The game configuration

        Returns:
        - Nothing
        """
        module_logger.info("Entering options Menu")
        pygame.display.set_caption("Glitch_Heaven")
        self.screensize = screen.get_size()
        self.config = config
        self.desc = None
        # Title animation and properties
        # v------------------------------------------------------------------v
        self.titleani = animation.Animation()
        self.titleani.loadFromDir(
                os.path.join("resources", "UI", "AnimatedTitle"))
        self.titletimings = [2., 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12,
                             0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12,
                             0.12, 0.12, 0.12, 0.12, 2., 0.12, 0.12,
                             0.12, 0.12]
        self.titleani = timedanimation.TimedAnimation(self.titletimings)
        self.titleani.loadFromDir(
                os.path.join("resources", "UI", "AnimatedTitle"))
        self.title = self.titleani.first()
        self.titlesize = self.title.get_size()
        self.titlerect = self.title.get_rect()
        self.titlerect.x = self.screensize[0]/2 - self.titlesize[0] / 2
        self.titlerect.y = 32
        # ^------------------------------------------------------------------^
        self.font = pygame.font.Font(os.path.join(
                            "resources", "fonts",
                            "TranscendsGames.otf"), 24)
        self.running = True
        self.currentItem = None
        self.background = pygame.image.load(
                          os.path.join("resources",
                                       "UI",
                                       "back.png")).convert_alpha()
        # Video Settings menu element
        # v------------------------------------------------------------------v
        self.videoimg = self.font.render("Video Settings", False,
                                         (255, 255, 255)).convert_alpha()
        self.vidselimg = makeGlitched("Video Settings", self.font)
        self.video = menuItem.menuitem(self.videoimg,
                                       self.vidselimg,
                                       (50, 240),
                                       lambda: self.editdesc(
                                           "Customize your eye disappeal"),
                                       lambda: VideoSettings(
                                           screen, keys, self.config, sounds
                                           ).mainLoop(),
                                       self.config,
                                       sounds)
        # ^------------------------------------------------------------------^
        # Sound settings menu element
        # v------------------------------------------------------------------v
        self.sndimg = self.font.render("Audio Settings", False,
                                       (255, 255, 255)).convert_alpha()
        self.sndselimg = makeGlitched("Audio Settings", self.font)
        self.snd = menuItem.menuitem(self.sndimg,
                                     self.sndselimg,
                                     (50, 320),
                                     lambda: self.editdesc(
                                         "Avoid deafening with these controls"
                                         ),
                                     lambda: AudioSettings(
                                         screen, keys, self.config,
                                         sounds).mainLoop(),
                                     self.config,
                                     sounds)
        # ^------------------------------------------------------------------^
        # Controls/Controllers menu element
        # v------------------------------------------------------------------v
        self.ctrlimg = self.font.render("Control Settings",
                                        False, (255, 255, 255)).convert_alpha()
        self.ctrlselimg = makeGlitched("Control Settings", self.font)
        self.ctrl = menuItem.menuitem(self.ctrlimg,
                                      self.ctrlselimg,
                                      (50, 400),
                                      lambda: self.editdesc(
                                          "Edit keyboard/joypad settings"),
                                      lambda: ControlSettings().main(
                                          screen, keys, self.config, sounds),
                                      self.config,
                                      sounds)
        # ^------------------------------------------------------------------^
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Main Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Main Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (650, 560),
                                          lambda: self.editdesc(
                                              "Go to the main menu"),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          sounds)
        # ^------------------------------------------------------------------^
        self.items = [self.video, self.snd, self.ctrl, self.mainmenu]
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)  # Make the cursor visible
        module_logger.info("Mouse cursor shown")
        while self.running:
            self.dt = self.clock.tick(30)/1000.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                # Keyboard Handling
                # v----------------------------------------------------------v
                if event.type == pygame.KEYDOWN:
                    if self.currentItem is None:
                        self.currentItem = 0
                    if event.key == keys["down"]:
                        self.currentItem = ((self.currentItem+1) %
                                            len(self.items))
                    if event.key == keys["up"]:
                        self.currentItem = ((self.currentItem-1) %
                                            len(self.items))
                    if event.key == keys["confirm"]:
                        self.items[self.currentItem].confirmSound.play()
                        self.items[self.currentItem].function()
                    if event.key == keys["escape"]:
                        self.goToMenu()
                    for item in self.items:
                        item.makeUnselected()
                    self.items[self.currentItem].makeSelected()
                # ^----------------------------------------------------------^
                # Mouse Handling
                # v----------------------------------------------------------v
                if event.type == pygame.MOUSEMOTION:
                    if self.currentItem == 0:
                        self.currentItem = None
                    for item in self.items:
                        if item.rect.collidepoint(*pygame.mouse.get_pos()):
                            item.makeSelected()
                        else:
                            item.makeUnselected()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.items:
                        if item.rect.collidepoint(*pygame.mouse.get_pos()):
                            item.confirmSound.play()
                            item.function()
                if event.type == pygame.QUIT:
                    quit()
                # ^----------------------------------------------------------^
            # Animates The title
            # v----------------------------------------------------------v
            self.title = self.titleani.next(self.dt)
            # ^----------------------------------------------------------^
            screen.blit(self.background, (0, 0))
            screen.blit(self.title, self.titlerect.topleft)
            if self.desc is not None:
                screen.blit(self.desc, (750-self.desc.get_rect().width, 300))
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            pygame.display.update()
