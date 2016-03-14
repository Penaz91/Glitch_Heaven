# New Game Menu Component
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
from tkinter import Tk
from tkinter import filedialog
from game import Game
from cfmenu import CFMenu
module_logger = logging.getLogger("Glitch_Heaven.NewGameMenu")
fh = loghandler.TimedRotatingFileHandler(pathjoin("logs", "Game.log"),
                                         "midnight", 1)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                              ' %(levelname)s --- %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
module_logger.addHandler(fh)
module_logger.addHandler(ch)


class NewGameMenu:
    """ Represents a pause menu window"""

    def editdesc(self, string):
        self.desc = makeGlitched(string, self.font)

    def loadcustom(self, keys, gameconfig, screen, sounds):
        """
        Loads a custom campaign from a open file dialog
        """
        try:
            Tk().withdraw()
            formats = [("Glitch_Heaven Campaign", "*.cmp")]
            self.camp = filedialog.askopenfilename(
                    filetypes=formats,
                    initialdir=pathjoin("data",
                                        "campaigns"))
            if self.camp:
                self.running = False
                Game().main(screen, keys, "newgame",
                            self.camp, gameconfig, sounds, self.chaos)
        except FileNotFoundError:
            module_logger.info("No File selected, Loading of campaign aborted")

    def newGame(self, keys, gameconfig, screen, sounds):
        self.running = False
        Game().main(screen, keys,
                    "newgame",
                    pathjoin("data",
                             "campaigns",
                             "main.cmp"),
                    self.gameconfig,
                    sounds,
                    self.chaos)

    def newCFGame(self, keys, gameconfig, screen, sounds):
        self.running = False
        Game().main(screen, keys,
                    "cfsingle",
                    pathjoin("data",
                             "campaigns",
                             "main.cmp"),
                    self.gameconfig,
                    sounds)

    def makeCampaignMenu(self, screen, keys, config, sounds):
        self.newmainimg = self.font.render("Start Main Campaign", False,
                                           (255, 255, 255)).convert_alpha()
        self.selectedmainimg = makeGlitched("Start Main Campaign", self.font)
        self.newmaingame = menuItem.menuitem(self.newmainimg,
                                             self.selectedmainimg,
                                             (50, 180),
                                             lambda: self.editdesc(
                                                 "Play the Main Game"),
                                             lambda: self.newGame(
                                                keys,
                                                config,
                                                screen,
                                                sounds),
                                             self.gameconfig,
                                             sounds
                                             )
        self.activeitems.append(self.newmaingame)

    def makeCustomCampaignMenu(self, screen, keys, config, sounds):
        self.newcustomimg = self.font.render("Start Custom Campaign", False,
                                             (255, 255, 255)).convert_alpha()
        self.selectedcustomimg = makeGlitched("Start Custom Campaign",
                                              self.font)
        self.newcustomgame = menuItem.menuitem(self.newcustomimg,
                                               self.selectedcustomimg,
                                               (50, 240),
                                               lambda: self.editdesc(
                                                   "Load a custom Campaign"),
                                               lambda: self.loadcustom(
                                                   keys,
                                                   self.gameconfig,
                                                   screen,
                                                   sounds),
                                               self.gameconfig,
                                               sounds
                                               )
        self.activeitems.append(self.newcustomgame)

    def makeSpeedRunMenu(self, screen, keys, config, sounds):
        self.srimg = self.font.render("SpeedRun Mode", False,
                                      (100, 100, 100)).convert_alpha()
        self.sr = menuItem.menuitem(self.srimg,
                                    self.srimg,
                                    (50, 300),
                                    lambda: self.editdesc(None),
                                    lambda: None,
                                    self.gameconfig,
                                    sounds)

    def makeNHMenu(self, screen, keys, config, sounds):
        if config.getboolean("Unlockables", "NHMode"):
            self.nhimg = self.font.render("Start the Second Quest",
                                          False,
                                          (100, 100, 100)).convert_alpha()
        else:
            self.nhimg = self.font.render("(File Corrupted)", False,
                                          (100, 100, 100)).convert_alpha()
        self.nh = menuItem.menuitem(self.nhimg,
                                    self.nhimg,
                                    (50, 360),
                                    lambda: self.editdesc(None),
                                    lambda: None,
                                    self.gameconfig,
                                    sounds)

    def makeSDMenu(self, screen, keys, config, sounds):
        if config.getboolean("Unlockables", "CFMode"):
            self.sdimg = self.font.render("Start 'Critical Failure' Mode",
                                          False,
                                          (255, 255, 255)).convert_alpha()
            self.sdselimg = makeGlitched("Start 'Critical Failure' Mode",
                                         self.font)
            self.sd = menuItem.menuitem(self.sdimg,
                                        self.sdselimg,
                                        (50, 420),
                                        lambda: self.editdesc(
                                            "Escape before the time runs out."
                                            ),
                                        lambda: CFMenu(
                                                screen,
                                                keys,
                                                self.gameconfig,
                                                sounds).mainLoop(),
                                        self.gameconfig,
                                        sounds)
            self.activeitems.append(self.sd)
        else:
            self.sdimg = self.font.render("(File Corrupted)", False,
                                          (100, 100, 100)).convert_alpha()
            self.sd = menuItem.menuitem(self.sdimg,
                                        self.sdimg,
                                        (50, 420),
                                        lambda: self.editdesc(None),
                                        lambda: None,
                                        self.gameconfig,
                                        sounds)

    def makeSMMenu(self, screen, keys, config, sounds):
        self.smimg = self.font.render("Play a Single Map", False,
                                      (100, 100, 100)).convert_alpha()
        self.sm = menuItem.menuitem(self.smimg,
                                    self.smimg,
                                    (50, 540),
                                    lambda: self.editdesc(None),
                                    lambda: None,
                                    self.gameconfig,
                                    sounds)

    def togglechaos(self):
        self.chaos = not self.chaos

    def makeChaosButton(self, screen, keys, config, sounds):
        if config.getboolean("Unlockables", "Chaos"):
            self.chimg = self.font.render("Toggle Chaos Modifier",
                                          False,
                                          (255, 255, 255)).convert_alpha()
            self.chselimg = makeGlitched("Toggle Chaos Modifier",
                                         self.font)
            self.cb = menuItem.menuitem(self.chimg,
                                        self.chselimg,
                                        (50, 480),
                                        lambda: self.editdesc("Chaos Mod: " +
                                                              str(self.chaos)),
                                        lambda: self.togglechaos(),
                                        self.gameconfig,
                                        sounds)
            self.activeitems.append(self.cb)
        else:
            self.chimg = self.font.render("(File Corrupted)", False,
                                          (100, 100, 100)).convert_alpha()
            self.cb = menuItem.menuitem(self.chimg,
                                        self.chimg,
                                        (50, 480),
                                        lambda: self.editdesc(None),
                                        lambda: None,
                                        self.gameconfig,
                                        sounds)

    def goToMenu(self):
        """
        Kills the current game and menu instance, and returns
        To the main menu, which is already running in BG.

        Keyword Arguments:
        - game: The game instance

        Returns:
        - Nothing
        """
        module_logger.info("Going to the previous menu")
        self.running = False

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
        module_logger.info("Opening the Video Settings Menu")
        pygame.display.set_caption("Glitch_Heaven")
        self.screensize = screen.get_size()
        self.activeitems = []
        self.gameconfig = config
        self.desc = None
        self.chaos = False
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
        # Main campaign menu element
        # v------------------------------------------------------------------v
        self.makeCampaignMenu(screen, keys, config, sounds)
        # Custom campaign menu element
        # v------------------------------------------------------------------v
        self.makeCustomCampaignMenu(screen, keys, config, sounds)
        # Insert a speedrun mode button
        # v------------------------------------------------------------------v
        self.makeSpeedRunMenu(screen, keys, config, sounds)
        # Insert a Hard mode button
        # v------------------------------------------------------------------v
        self.makeNHMenu(screen, keys, config, sounds)
        # Insert a sudden death mode button
        # v------------------------------------------------------------------v
        self.makeSDMenu(screen, keys, config, sounds)
        # Insert a chaos modifier button
        # v------------------------------------------------------------------v
        self.makeChaosButton(screen, keys, config, sounds)
        # Insert a single map mode button
        # v------------------------------------------------------------------v
        self.makeSMMenu(screen, keys, config, sounds)
        # ^------------------------------------------------------------------^
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Previous Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Previous Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (600, 560),
                                          lambda: self.editdesc(
                                              "Go to the main menu"),
                                          lambda: self.goToMenu(),
                                          self.gameconfig,
                                          sounds)
        self.activeitems.append(self.mainmenu)
        # ^------------------------------------------------------------------^
        self.items = [self.newmaingame, self.newcustomgame, self.sr,
                      self.nh, self.sd, self.sm, self.cb, self.mainmenu]
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
                                            len(self.activeitems))
                    if event.key == keys["up"]:
                        self.currentItem = ((self.currentItem-1) %
                                            len(self.activeitems))
                    if event.key == keys["confirm"]:
                        self.activeitems[self.currentItem].confirmSound.play()
                        self.activeitems[self.currentItem].function()
                    if event.key == keys["escape"]:
                        self.goToMenu()
                    for item in self.activeitems:
                        item.makeUnselected()
                    self.activeitems[self.currentItem].makeSelected()
                # ^----------------------------------------------------------^
                # Mouse Handling
                # v----------------------------------------------------------v
                if event.type == pygame.MOUSEMOTION:
                    if self.currentItem == 0:
                        self.currentItem = None
                    for item in self.activeitems:
                        if item.rect.collidepoint(*pygame.mouse.get_pos()):
                            item.makeSelected()
                        else:
                            item.makeUnselected()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for item in self.activeitems:
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
