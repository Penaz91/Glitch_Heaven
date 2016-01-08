# Main Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os
from components.UI import menuItem
from game import Game
from libs import timedanimation
from optionsmenu import OptionsMenu
import logging
from logging import handlers as loghandler
from os.path import join as pathjoin
module_logger = logging.getLogger("Glitch_Heaven.MainMenu")
fh = loghandler.TimedRotatingFileHandler(pathjoin("logs", "Game.log"),
                                         "midnight", 1)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                              ' %(levelname)s --- %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
module_logger.addHandler(fh)
module_logger.addHandler(ch)
# TODO AREA:
# ---------------
# Tie Menu graphic to resolution
# ---------------

class menu:
    """ Represents the main Game menu """

    def main(self, screen, keys, config):
        """
        Main menu method

        Keyword Arguments:
        - screen: The surface to draw the menu to.
        - keys: The control keys collection used
        """
        module_logger.info("Entering Main Menu")
        self.screensize = screen.get_size()
        # Title animation and properties
        # v------------------------------------------------------------------v
        self.gameconfig = config
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
        # New game menu element
        # v------------------------------------------------------------------v
        self.newgameimg = self.font.render("NewGame", False,
                                           (255, 255, 255)).convert_alpha()
        self.selectedimg = self.font.render("NewGame", False,
                                            (255, 0, 0)).convert_alpha()
        self.newgame = menuItem.menuitem(self.newgameimg,
                                         self.selectedimg,
                                         (320, 240),
                                         lambda: Game().main(screen, keys,
                                                             "newgame",
                                                             self.gameconfig),
                                         self.gameconfig)
        # ^------------------------------------------------------------------^
        # Quit game menu element
        # v------------------------------------------------------------------v
        self.exitimg = self.font.render("Quit", False,
                                        (255, 255, 255)).convert_alpha()
        self.exitselected = self.font.render("Quit", False,
                                             (255, 0, 0)).convert_alpha()
        self.exit = menuItem.menuitem(self.exitimg,
                                      self.exitselected,
                                      (700, 560), lambda: pygame.event.post(
                                          pygame.event.Event(pygame.QUIT)),
                                      self.gameconfig)
        # ^------------------------------------------------------------------^
        # If there is a savefile, enable the continue game button
        # v------------------------------------------------------------------v
        if not os.path.exists(os.path.join("savegames",
                                           "SaveGame.dat")):
            self.cont = self.font.render("Continue Game", False,
                                         (100, 100, 100)).convert_alpha()
            self.cgam = menuItem.menuitem(self.cont,
                                          self.cont,
                                          (320, 320),
                                          lambda: None,
                                          self.gameconfig)
        else:
            self.cont = self.font.render("Continue Game", False,
                                         (255, 255, 255)).convert_alpha()
            self.contsel = self.font.render("Continue Game", False,
                                            (255, 0, 0)).convert_alpha()
            self.cgam = menuItem.menuitem(self.cont,
                                          self.contsel,
                                          (320, 320),
                                          lambda: Game().main(screen, keys,
                                                              "load",
                                                              self.gameconfig),
                                          self.gameconfig)
        # ^------------------------------------------------------------------^
        # Insert an options button
        # v------------------------------------------------------------------v
        self.optimg = self.font.render("Options", False,
                                       (255, 255, 255)).convert_alpha()
        self.optsel = self.font.render("Options", False,
                                       (255, 0, 0)).convert_alpha()
        self.options = menuItem.menuitem(self.optimg,
                                         self.optsel,
                                         (320, 440),
                                         lambda: OptionsMenu().main(
                                             screen, keys, self.gameconfig),
                                         self.gameconfig)
        # ^------------------------------------------------------------------^
        self.items = [self.newgame, self.cgam, self.options, self.exit]
        self.clock = pygame.time.Clock()
        while self.running:
            self.dt = self.clock.tick(30)/1000.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    module_logger.info("QUIT signal received, quitting")
                    self.running = False
                # Keyboard handling
                # v------------------------------------------------------------------v
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
                        print("esc")
                    for item in self.items:
                        item.makeUnselected()
                    self.items[self.currentItem].makeSelected()
                # ^------------------------------------------------------------------^
                # Mouse handling
                # v------------------------------------------------------------------v
                if event.type == pygame.MOUSEMOTION:
                    if self.currentItem == 0:
                        self.currentItem = None
                    for item in self.items:
                        if item.rect.collidepoint(*pygame.mouse.get_pos())\
                                and not item.selectedStatus:
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
                # ^------------------------------------------------------------------^
            # Animates The title
            # v----------------------------------------------------------v
            self.title = self.titleani.next(self.dt)
            # ^----------------------------------------------------------^
            screen.blit(self.background, (0, 0))
            screen.blit(self.title, self.titlerect.topleft)
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            pygame.display.update()
