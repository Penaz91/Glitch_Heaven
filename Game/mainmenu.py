# Main Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
from game import Game
import os
from components.UI import menuItem
from libs import timedanimation
from optionsmenu import OptionsMenu
from newgamemenu import NewGameMenu
import logging
from logging import handlers as loghandler
from os.path import join as pathjoin
from credits import Credits
from libs.textglitcher import makeGlitched
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

    def editdesc(self, string):
        self.desc = makeGlitched(string, self.font)

    def makeNewGameMenu(self, screen, keys, config, sounds):
        self.newgameimg = self.font.render("Start A New Game", False,
                                           (255, 255, 255)).convert_alpha()
        self.selectedgameimg = makeGlitched("Start A New Game", self.font)
        self.newgamemenu = menuItem.menuitem(self.newgameimg,
                                             self.selectedgameimg,
                                             (50, 180),
                                             lambda: self.editdesc(
                                                 "Start a new game,in any mode"
                                                 ),
                                             lambda: NewGameMenu().main(
                                                screen,
                                                keys,
                                                self.gameconfig,
                                                sounds),
                                             self.gameconfig,
                                             sounds)
        self.activeitems.append(self.newgamemenu)

    def makeCreditsMenu(self, screen, keys, config, sounds):
        self.creditsimg = self.font.render("Credits", False,
                                           (255, 255, 255)).convert_alpha()
        self.selectedcreditsimg = makeGlitched("Credits", self.font)
        self.credits = menuItem.menuitem(self.creditsimg,
                                         self.selectedcreditsimg,
                                         (50, 360),
                                         lambda: self.editdesc(
                                             "Look at Names"),
                                         lambda: Credits().main(
                                             screen,
                                             keys,
                                             self.gameconfig,
                                             sounds),
                                         self.gameconfig,
                                         sounds)
        self.activeitems.append(self.credits)

    def makeQuitMenu(self, screen, keys, config, sounds):
        self.exitimg = self.font.render("Quit", False,
                                        (255, 255, 255)).convert_alpha()
        self.exitselected = makeGlitched("Quit", self.font)
        self.exit = menuItem.menuitem(self.exitimg,
                                      self.exitselected,
                                      (700, 560),
                                      lambda: self.editdesc("Quit the Game"),
                                      lambda: pygame.event.post(
                                          pygame.event.Event(pygame.QUIT)),
                                      self.gameconfig,
                                      sounds)
        self.activeitems.append(self.exit)

    def makeLoadMenu(self, screen, keys, config, sounds):
        if not os.listdir(os.path.join("savegames")):
            self.cont = self.font.render("Load Saved Game", False,
                                         (100, 100, 100)).convert_alpha()
            self.cgam = menuItem.menuitem(self.cont,
                                          self.cont,
                                          (50, 240),
                                          lambda: self.editdesc(None),
                                          lambda: None,
                                          self.gameconfig,
                                          sounds)
        else:
            self.cont = self.font.render("Load Saved Game", False,
                                         (255, 255, 255)).convert_alpha()
            self.contsel = makeGlitched("Load Saved Game", self.font)
            self.cgam = menuItem.menuitem(self.cont,
                                          self.contsel,
                                          (50, 240),
                                          lambda: self.editdesc(
                                              "Load a previously saved Game"),
                                          lambda: Game().main(screen, keys,
                                                              "load",
                                                              None,
                                                              self.gameconfig,
                                                              sounds),
                                          self.gameconfig,
                                          sounds)
            self.activeitems.append(self.cgam)
        self.update = False

    def makeOptionsMenu(self, screen, keys, config, sounds):
        self.optimg = self.font.render("Options", False,
                                       (255, 255, 255)).convert_alpha()
        self.optsel = makeGlitched("Options", self.font)
        self.options = menuItem.menuitem(self.optimg,
                                         self.optsel,
                                         (50, 300),
                                         lambda: self.editdesc(
                                             "Fiddle With Options"),
                                         lambda: OptionsMenu().main(
                                             screen, keys, self.gameconfig,
                                             sounds),
                                         self.gameconfig,
                                         sounds)
        self.activeitems.append(self.options)

    def main(self, screen, keys, config, sounds):
        """
        Main menu method

        Keyword Arguments:
        - screen: The surface to draw the menu to.
        - keys: The control keys collection used
        """
        module_logger.info("Entering Main Menu")
        pygame.display.set_caption("Glitch_Heaven")
        self.screensize = screen.get_size()
        self.desc = None
        self.activeitems = []
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
        # New Game Menu menu element
        # v------------------------------------------------------------------v
        self.makeNewGameMenu(screen, keys, config, sounds)
        # ^------------------------------------------------------------------^
        # If there is a savefile, enable the continue game button
        # v------------------------------------------------------------------v
        self.makeLoadMenu(screen, keys, config, sounds)
        # ^------------------------------------------------------------------^
        # Insert an options button
        # v------------------------------------------------------------------v
        self.makeOptionsMenu(screen, keys, config, sounds)
        # ^------------------------------------------------------------------^
        # Credits menu element
        # v------------------------------------------------------------------v
        self.makeCreditsMenu(screen, keys, config, sounds)
        # ^------------------------------------------------------------------^
        # Quit game menu element
        # v------------------------------------------------------------------v
        self.makeQuitMenu(screen, keys, config, sounds)
        # ^------------------------------------------------------------------^
        self.items = [self.newgamemenu, self.cgam, self.options,
                      self.credits, self.exit]
        self.clock = pygame.time.Clock()
        pygame.mouse.set_visible(True)  # Make the cursor visible
        module_logger.info("Mouse cursor shown")
        while self.running:
            self.dt = self.clock.tick(30)/1000.
            if self.update:
                self.makeLoadMenu(screen, keys, config, sounds)
                self.items = [self.newgamemenu, self.cgam, self.options,
                              self.credits, self.exit]
                if os.listdir(os.path.join("savegames")):
                    self.activeitems = [self.newgamemenu, self.cgam,
                                        self.options, self.credits, self.exit]
                else:
                    self.activeitems = [self.newgamemenu, self.options,
                                        self.credits, self.exit]
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
                                            len(self.activeitems))
                    if event.key == keys["up"]:
                        self.currentItem = ((self.currentItem-1) %
                                            len(self.activeitems))
                    if event.key == keys["confirm"]:
                        self.activeitems[self.currentItem].confirmSound.play()
                        self.update = True
                        self.activeitems[self.currentItem].function()
                    if event.key == keys["escape"]:
                        print("esc")
                    for item in self.activeitems:
                        item.makeUnselected()
                    self.activeitems[self.currentItem].makeSelected()
                # ^------------------------------------------------------------------^
                # Mouse handling
                # v------------------------------------------------------------------v
                if event.type == pygame.MOUSEMOTION:
                    if self.currentItem == 0:
                        self.currentItem = None
                    for item in self.activeitems:
                        if item.rect.collidepoint(*pygame.mouse.get_pos())\
                                and not item.selectedStatus:
                            item.makeSelected()
                        else:
                            item.makeUnselected()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.activeitems:
                        if item.rect.collidepoint(*pygame.mouse.get_pos()):
                            item.confirmSound.play()
                            self.update = True
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
            if self.desc is not None:
                screen.blit(self.desc, (750-self.desc.get_rect().width, 300))
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            pygame.display.update()
