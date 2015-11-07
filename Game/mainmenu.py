# Main Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os
from components.UI import menuItem
from game import Game
from libs import animation


class menu:
    """ Represents the main Game menu """

    def main(self, screen, keys, config):
        """
        Main menu method

        Keyword Arguments:
        - screen: The surface to draw the menu to.
        - keys: The control keys collection used
        """
        self.screensize = screen.get_size()
        # Title animation and properties
        # v------------------------------------------------------------------v
        self.titleani = animation.Animation()
        self.titleani.loadFromDir(
                os.path.join("resources", "UI", "AnimatedTitle"))
        self.title = self.titleani.next()
        self.titletimings = [2., 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12,
                             0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12,
                             0.12, 0.12, 0.12, 0.12, 2., 0.12, 0.12,
                             0.12, 0.12]
        self.titletime = 0.
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
        self.newgameimg = self.font.render("NewGame", False, (255, 255, 255))
        self.selectedimg = self.font.render("NewGame", False, (255, 0, 0))
        self.newgame = menuItem.menuitem(self.newgameimg,
                                         self.selectedimg,
                                         (320, 240),
                                         lambda: Game().main(screen, keys, config,
                                                             "newgame"))
        # ^------------------------------------------------------------------^
        # Quit game menu element
        # v------------------------------------------------------------------v
        self.exitimg = self.font.render("Quit", False, (255, 255, 255))
        self.exitselected = self.font.render("Quit", False, (255, 0, 0))
        self.exit = menuItem.menuitem(self.exitimg,
                                      self.exitselected,
                                      (320, 560), lambda: quit())
        # ^------------------------------------------------------------------^
        # If there is a savefile, enable the continue game button
        # v------------------------------------------------------------------v
        if not os.path.exists(os.path.join("SaveGame.dat")):
            self.cont = self.font.render("Continue Game", False,
                                         (100, 100, 100))
            self.contgame = menuItem.menuitem(self.cont,
                                              self.cont,
                                              (320, 320),
                                              lambda: None)
        else:
            self.cont = self.font.render("Continue Game", False,
                                         (255, 255, 255))
            self.contsel = self.font.render("Continue Game", False,
                                            (255, 0, 0))
            self.contgame = menuItem.menuitem(self.cont,
                                              self.contsel,
                                              (320, 320),
                                              lambda: Game().main(screen, keys, config,
                                                                  "load"))
        # ^------------------------------------------------------------------^
        self.items = [self.newgame, self.contgame, self.exit]
        self.clock = pygame.time.Clock()
        while self.running:
            self.dt = self.clock.tick(30)/1000.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
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
                # ^------------------------------------------------------------------^
            # Handles the timed animation
            # MIGHT NEED DEPRECATION IN FAVOUR OF A TIMEDANIMATION OBJECT
            # v----------------------------------------------------------v
            self.titletime += self.dt
            if self.titletime >= self.titletimings[self.titleani.currentframe]:
                self.title = self.titleani.next()
                self.titletime = 0
            # ^----------------------------------------------------------^
            screen.blit(self.background, (0, 0))
            screen.blit(self.title, self.titlerect.topleft)
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            screen.blit(self.newgame.image, self.newgame.location)
            pygame.display.update()
        pygame.quit()
        quit()
