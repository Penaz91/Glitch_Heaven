# Audio Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os
from components.UI import menuItem, meter
from libs import animation, timedanimation
import logging
from logging import handlers as loghandler
from os.path import join as pathjoin
module_logger = logging.getLogger("Glitch_Heaven.AudioSettings")
fh = loghandler.TimedRotatingFileHandler(pathjoin("logs", "Game.log"),
                                         "midnight", 1)
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                              ' %(levelname)s --- %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
module_logger.addHandler(fh)
module_logger.addHandler(ch)


class AudioSettings:
    """ Represents a pause menu window"""

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
        module_logger.info("Returning to previous menu")

    def main(self, screen, keys, config):
        """
        The main method to show and make the menu work

        Keyword Arguments:
        - Screen: the Screen surface to make the menu on
        - Keys: The list of control keys to use
        - game: The game instance.

        Returns:
        - Nothing
        """
        module_logger.info("Entering Audio Settings Menu")
        self.screensize = screen.get_size()
        self.config = config
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
        self.menumeter = meter.Meter((320, 250), (200, 10),
                                     self.config, "menuvolume")
        self.menuwriting = self.font.render("Menu Volume: ", False,
                                            (255, 255, 255)).convert_alpha()
        self.sfxmeter = meter.Meter((320, 330), (200, 10),
                                    self.config, "sfxvolume")
        self.sfxwriting = self.font.render("SFX Volume: ", False,
                                           (255, 255, 255)).convert_alpha()
        self.musicmeter = meter.Meter((320, 410), (200, 10),
                                      self.config, "musicvolume")
        self.musicwriting = self.font.render("Music Volume: ", False,
                                             (255, 255, 255)).convert_alpha()
        """
        # Video Settings menu element
        # v------------------------------------------------------------------v
        self.videoimg = self.font.render("Video Settings", False,
                                         (255, 255, 255)).convert_alpha()
        self.vidselimg = self.font.render("Video Settings", False,
                                          (255, 0, 0)).convert_alpha()
        self.video = menuItem.menuitem(self.videoimg,
                                       self.vidselimg,
                                       (320, 240),
                                       lambda: VideoSettings.main())
        # ^------------------------------------------------------------------^
        # Sound settings menu element
        # v------------------------------------------------------------------v
        self.sndimg = self.font.render("Audio Settings", False,
                                       (255, 255, 255)).convert_alpha()
        self.sndselimg = self.font.render("Audio Settings", False,
                                          (255, 0, 0)).convert_alpha()
        self.snd = menuItem.menuitem(self.sndimg,
                                     self.sndselimg,
                                     (320, 320), lambda: AudioSettings.main())
        # ^------------------------------------------------------------------^
        # Controls/Controllers menu element
        # v------------------------------------------------------------------v
        self.ctrlimg = self.font.render("Control Settings",
                                        False, (255, 255, 255)).convert_alpha()
        self.ctrlselimg = self.font.render("Control Settings", False,
                                           (255, 0, 0)).convert_alpha()
        self.ctrl = menuItem.menuitem(self.ctrlimg,
                                      self.ctrlselimg,
                                      (320, 400),
                                      lambda: ControlSettings.main())"""
        # ^------------------------------------------------------------------^
        # "Previous Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Previous Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = self.font.render("Previous Menu",
                                        False, (255, 0, 0)).convert_alpha()
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (50, 560),
                                          lambda: self.goToMenu(),
                                          self.config)
        # ^------------------------------------------------------------------^
        self.items = [self.mainmenu]
        self.clock = pygame.time.Clock()
        while self.running:
            self.dt = self.clock.tick(30)/1000.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
                # Keyboard Handling
                # v----------------------------------------------------------v
                if event.type == pygame.KEYDOWN:
                    if self.currentItem is None:
                        self.currentItem = 0
                    if event.key == keys["down"]:
                        print("down")
                        self.currentItem = ((self.currentItem+1) %
                                            len(self.items))
                    if event.key == keys["up"]:
                        print("up")
                        self.currentItem = ((self.currentItem-1) %
                                            len(self.items))
                    if event.key == keys["confirm"]:
                        self.items[self.currentItem].function()
                    if event.key == keys["escape"]:
                        print("esc")
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
                    mousepos = pygame.mouse.get_pos()
                    for item in self.items:
                        if item.rect.collidepoint(*mousepos):
                            item.function()
                    if self.menumeter.rect.collidepoint(*mousepos):
                        amount = self.menumeter.set_quantity(mousepos)
                        module_logger.debug("Menu volume set at: " + str(amount))
                    if self.sfxmeter.rect.collidepoint(*mousepos):
                        amount = self.sfxmeter.set_quantity(mousepos)
                        module_logger.debug("Sfx volume set at: " + str(amount))
                    if self.musicmeter.rect.collidepoint(*mousepos):
                        amount = self.musicmeter.set_quantity(mousepos)
                        module_logger.debug("Music volume set at: " + str(amount))
                # ^----------------------------------------------------------^
            # Animates The title
            # v----------------------------------------------------------v
            self.title = self.titleani.next(self.dt)
            # ^----------------------------------------------------------^
            screen.blit(self.background, (0, 0))
            screen.blit(self.title, self.titlerect.topleft)
            screen.blit(self.menuwriting, (190, 240))
            screen.blit(self.sfxwriting, (190, 320))
            screen.blit(self.sfxwriting, (190, 400))
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            self.menumeter.draw(screen)
            self.sfxmeter.draw(screen)
            self.musicmeter.draw(screen)
            pygame.display.update()
