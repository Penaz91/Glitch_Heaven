# Pause Menu Component
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
module_logger = logging.getLogger("Glitch_Heaven.PauseMenu")
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


class pauseMenu:
    """ Represents a pause menu window"""

    def unpause(self):
        """ Stops the menu from running and resumes the game"""
        module_logger.info("Game unpaused")
        self.running = False

    def goToMenu(self, game):
        """
        Kills the current game and menu instance, and returns
        To the main menu, which is already running in BG.

        Keyword Arguments:
        - game: The game instance

        Returns:
        - Nothing
        """
        module_logger.info("Going back to main menu")
        game.running = False
        self.running = False

    def main(self, screen, keys, game, config, sounds):
        """
        The main method to show and make the menu work

        Keyword Arguments:
        - Screen: the Screen surface to make the menu on
        - Keys: The list of control keys to use
        - game: The game instance.

        Returns:
        - Nothing
        """
        module_logger.info("Opening the Pause Menu")
        pygame.display.set_caption("Glitch_Heaven")
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
        # Resume game menu element
        # v------------------------------------------------------------------v
        self.resgameimg = self.font.render("Resume Game", False,
                                           (255, 255, 255)).convert_alpha()
        self.selectedimg = makeGlitched("Resume Game", self.font)
        self.resgame = menuItem.menuitem(self.resgameimg,
                                         self.selectedimg,
                                         (320, 240),
                                         lambda: self.unpause(),
                                         self.config,
                                         sounds)
        # ^------------------------------------------------------------------^
        # Save game menu element
        # v------------------------------------------------------------------v
        self.saveimg = self.font.render("Save Game", False,
                                        (255, 255, 255)).convert_alpha()
        self.saveselected = makeGlitched("Save Game", self.font)
        self.savegame = menuItem.menuitem(self.saveimg,
                                          self.saveselected,
                                          (320, 320), lambda: game.saveGame(),
                                          self.config,
                                          sounds)
        # ^------------------------------------------------------------------^
        # Quit to desktop menu element
        # v------------------------------------------------------------------v
        self.exitimg = self.font.render("Quit to Desktop",
                                        False, (255, 255, 255)).convert_alpha()
        self.exitselected = makeGlitched("Quit to Desktop", self.font)
        self.exit = menuItem.menuitem(self.exitimg,
                                      self.exitselected,
                                      (320, 560), lambda: pygame.event.post(
                                        pygame.event.Event(pygame.QUIT)),
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
                                          (320, 400),
                                          lambda: self.goToMenu(game),
                                          self.config,
                                          sounds)
        # ^------------------------------------------------------------------^
        self.items = [self.resgame, self.savegame, self.mainmenu, self.exit]
        self.clock = pygame.time.Clock()
        while self.running:
            self.dt = self.clock.tick(30)/1000.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    module_logger.info("QUIT event has been raised, exiting")
                    quit()
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
                        self.items[self.currentItem].confirmSound.play()
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
                            item.confirmSound.play()
                            item.function()
                # ^----------------------------------------------------------^
            # Animates The title
            # v----------------------------------------------------------v
            self.title = self.titleani.next(self.dt)
            # ^----------------------------------------------------------^
            screen.blit(self.background, (0, 0))
            screen.blit(self.title, self.titlerect.topleft)
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            screen.blit(self.resgame.image, self.resgame.location)
            pygame.display.update()
