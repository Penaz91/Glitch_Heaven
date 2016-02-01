# Keyboard Settings Component
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
from components.UI import keyboarditem as kitem
module_logger = logging.getLogger("Glitch_Heaven.ControlSettings")
fh = loghandler.TimedRotatingFileHandler(pathjoin("logs", "Game.log"),
                                         "midnight", 1)
ch = logging.StreamHandler()
formatter = logging.Formatter('[%(asctime)s] (%(name)s) -'
                              ' %(levelname)s --- %(message)s')
ch.setFormatter(formatter)
fh.setFormatter(formatter)
module_logger.addHandler(fh)
module_logger.addHandler(ch)


class KeyboardSettings:
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
        module_logger.info("Opening the Keyboard Settings Menu")
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
        # ^------------------------------------------------------------------^
        # "Left Key" menu element
        # v------------------------------------------------------------------v
        self.lefttext = self.font.render("Move Left: ",
                                         False,
                                         (255, 255, 255)).convert_alpha()
        key = config.get("Controls", "left")
        keytext = pygame.key.name(int(key))
        self.leftimg = self.font.render(keytext.upper(),
                                        False, (255, 255, 255)).convert_alpha()
        self.leftsel = makeGlitched(keytext.upper(), self.font)
        self.left = kitem.KeyboardItem(self.leftimg,
                                       self.leftsel,
                                       (self.lefttext.get_rect().width + 70,
                                           180),
                                       lambda: self.left.KeySelect(self.font,
                                                                   "left",
                                                                   config,
                                                                   keys),
                                       self.config,
                                       sounds)
        # ^------------------------------------------------------------------^
        # "Right Key" menu element
        # v------------------------------------------------------------------v
        self.righttext = self.font.render("Move Right: ",
                                          False,
                                          (255, 255, 255)).convert_alpha()
        key = config.get("Controls", "right")
        keytext = pygame.key.name(int(key))
        self.rightimg = self.font.render(keytext.upper(),
                                         False,
                                         (255, 255, 255)).convert_alpha()
        self.rightsel = makeGlitched(keytext.upper(), self.font)
        self.right = kitem.KeyboardItem(self.rightimg,
                                        self.rightsel,
                                        (self.righttext.get_rect().width + 70,
                                            240),
                                        lambda: self.right.KeySelect(self.font,
                                                                     "right",
                                                                     config,
                                                                     keys),
                                        self.config,
                                        sounds)
        # ^------------------------------------------------------------------^
        # "Jump Key" menu element
        # v------------------------------------------------------------------v
        self.jumptext = self.font.render("Jump: ",
                                         False,
                                         (255, 255, 255)).convert_alpha()
        key = config.get("Controls", "jump")
        keytext = pygame.key.name(int(key))
        self.jumpimg = self.font.render(keytext.upper(),
                                        False, (255, 255, 255)).convert_alpha()
        self.jumpsel = makeGlitched(keytext.upper(), self.font)
        self.jump = kitem.KeyboardItem(self.jumpimg,
                                       self.jumpsel,
                                       (self.jumptext.get_rect().width + 70,
                                           300),
                                       lambda: self.jump.KeySelect(self.font,
                                                                   "jump",
                                                                   config,
                                                                   keys),
                                       self.config,
                                       sounds)
        # ^------------------------------------------------------------------^
        # "Run Key" menu element
        # v------------------------------------------------------------------v
        self.runtext = self.font.render("Run: ",
                                        False,
                                        (255, 255, 255)).convert_alpha()
        key = config.get("Controls", "run")
        keytext = pygame.key.name(int(key))
        self.runimg = self.font.render(keytext.upper(),
                                       False,
                                       (255, 255, 255)).convert_alpha()
        self.runsel = makeGlitched(keytext.upper(), self.font)
        self.run = kitem.KeyboardItem(self.runimg,
                                      self.runsel,
                                      (self.runtext.get_rect().width + 70,
                                          360),
                                      lambda: self.run.KeySelect(self.font,
                                                                 "run",
                                                                 config,
                                                                 keys),
                                      self.config,
                                      sounds)
        # ^------------------------------------------------------------------^
        # "Action Key" menu element
        # v------------------------------------------------------------------v
        self.acttext = self.font.render("Action/Interact: ",
                                        False, (255, 255, 255)).convert_alpha()
        key = config.get("Controls", "action")
        keytext = pygame.key.name(int(key))
        self.actimg = self.font.render(keytext.upper(),
                                       False,
                                       (255, 255, 255)).convert_alpha()
        self.actsel = makeGlitched(keytext.upper(), self.font)
        self.act = kitem.KeyboardItem(self.actimg,
                                      self.actsel,
                                      (self.acttext.get_rect().width + 70,
                                          420),
                                      lambda: self.act.KeySelect(self.font,
                                                                 "action",
                                                                 config,
                                                                 keys),
                                      self.config,
                                      sounds)
        # ^------------------------------------------------------------------^
        # "Restart Key" menu element
        # v------------------------------------------------------------------v
        self.resttext = self.font.render("Restart Level: ",
                                        False, (255, 255, 255)).convert_alpha()
        key = config.get("Controls", "restart")
        keytext = pygame.key.name(int(key))
        self.restimg = self.font.render(keytext.upper(),
                                       False,
                                       (255, 255, 255)).convert_alpha()
        self.restsel = makeGlitched(keytext.upper(), self.font)
        self.rest = kitem.KeyboardItem(self.restimg,
                                       self.restsel,
                                      (self.resttext.get_rect().width + 70,
                                          480),
                                      lambda: self.rest.KeySelect(self.font,
                                                                  "restart",
                                                                  config,
                                                                  keys),
                                      self.config,
                                      sounds)
        # ^------------------------------------------------------------------^
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Previous Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = makeGlitched("Previous Menu", self.font)
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (50, 560),
                                          lambda: self.goToMenu(),
                                          self.config,
                                          sounds)
        # ^------------------------------------------------------------------^
        self.items = [self.left, self.right, self.jump,
                      self.run, self.act, self.rest, self.mainmenu]
        self.clock = pygame.time.Clock()
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
            screen.blit(self.lefttext, (50, 180))
            screen.blit(self.righttext, (50, 240))
            screen.blit(self.jumptext, (50, 300))
            screen.blit(self.runtext, (50, 360))
            screen.blit(self.acttext, (50, 420))
            screen.blit(self.resttext, (50, 480))
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            pygame.display.update()
