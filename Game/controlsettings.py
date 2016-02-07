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
from libs.textglitcher import makeGlitched
from keyboardsettings import KeyboardSettings
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
        module_logger.info("Returning to previous menu")

    def makeKeyboardMenu(self, screen, keys, config, sounds):
        self.keybimg = self.font.render("Keyboard Settings", False,
                                           (255, 255, 255)).convert_alpha()
        self.keybselimg = makeGlitched("Keyboard Settings", self.font)
        self.keyboard = menuItem.menuitem(self.keybimg,
                                          self.keybselimg,
                                          (50, 240),
                                          lambda: self.editdesc("Edit Keyboard assignments"),
                                          lambda: KeyboardSettings().main(screen,
                                                                        keys,
                                                                        config,
                                                                        sounds),
                                          self.gameconfig,
                                          sounds
                                          )
                                          
    def makeJoypadMenu(self, screen, keys, config, sounds):
        self.joyimg = self.font.render("Joypad Settings", False,
                                           (255, 255, 255)).convert_alpha()
        self.joyselimg = makeGlitched("Joypad Settings", self.font)
        self.joypad = menuItem.menuitem(self.joyimg,
                                        self.joyselimg,
                                        (50, 380),
                                        lambda: self.editdesc("Edit Joypad Assignments (To be implemented)"),
                                        lambda: None,
                                        self.gameconfig,
                                        sounds
                                        )

    def main(self, screen, keys, config, sounds):
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
        pygame.display.set_caption("Glitch_Heaven")
        self.gameconfig = config
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
        self.makeKeyboardMenu(screen, keys, config, sounds)
        self.makeJoypadMenu(screen, keys, config, sounds)
        # ^------------------------------------------------------------------^
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Main Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Main Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (320, 560),
                                          lambda: self.editdesc("Go to the main menu"),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          sounds)
        # ^------------------------------------------------------------------^
        self.items = [self.keyboard, self.joypad, self.mainmenu]
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)  # Make the cursor visible
        module_logger.info("Mouse cursor shown")
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
                # ^----------------------------------------------------------^
            # Animates The title
            # v----------------------------------------------------------v
            self.title = self.titleani.next(self.dt)
            # ^----------------------------------------------------------^
            screen.blit(self.background, (0, 0))
            screen.blit(self.title, self.titlerect.topleft)
            if self.desc is not None:
                screen.blit(self.desc, (750-self.desc.get_rect().width,300))
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            pygame.display.update()
