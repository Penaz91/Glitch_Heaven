# Control Settings Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os
from components.UI import menuItem
from libs import animation, timedanimation
import logging
from logging import handlers as loghandler
from os.path import join as pathjoin
module_logger = logging.getLogger("Glitch_Heaven.ControlSettings")
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


class ControlSettings:
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
        module_logger.info("Entering Control menu")
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

        self.line1 = self.font.render("Current Controls:", False,
                                      (255, 255, 255))
        self.line2 = self.font.render("Left/Right Arrow Keys: Movement", False,
                                      (255, 255, 255))
        self.line3 = self.font.render("Up Arrow Key: Jump", False,
                                      (255, 255, 255))
        self.line4 = self.font.render("Down Arrow Key: Interact", False,
                                      (255, 255, 255))
        self.line5 = self.font.render("Z: Keep pressed to run", False,
                                      (255, 255, 255))
        self.line6 = self.font.render("Left Shift + 1->9: Debug Keys/Cheats",
                                      False,
                                      (255, 255, 255))
        self.line7 = self.font.render("Left Shift + q->y: Debug Keys/Cheats",
                                      False,
                                      (255, 255, 255))
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
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Main Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = self.font.render("Main Menu",
                                        False, (255, 0, 0)).convert_alpha()
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (320, 560),
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
                    for item in self.items:
                        if item.rect.collidepoint(*pygame.mouse.get_pos()):
                            item.function()
                # ^----------------------------------------------------------^
            # Animates The title
            # v----------------------------------------------------------v
            self.title = self.titleani.next(self.dt)
            # ^----------------------------------------------------------^
            screen.blit(self.background, (0, 0))
            screen.blit(self.title, self.titlerect.topleft)
            screen.blit(self.line1, (100, 120))
            screen.blit(self.line2, (100, 140))
            screen.blit(self.line3, (100, 160))
            screen.blit(self.line4, (100, 180))
            screen.blit(self.line5, (100, 200))
            screen.blit(self.line6, (100, 240))
            screen.blit(self.line7, (100, 260))
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            pygame.display.update()
