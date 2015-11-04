# Main Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os
from components.UI import menuItem
from libs import animation


class pauseMenu:
    """ Represents a pause menu window"""

    def unpause(self):
        """ Stops the menu from running and resumes the game"""
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
        game.running = False
        self.running = False

    def main(self, screen, keys, game):
        """
        The main method to show and make the menu work

        Keyword Arguments:
        - Screen: the Screen surface to make the menu on
        - Keys: The list of control keys to use
        - game: The game instance.

        Returns:
        - Nothing
        """
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
        self.font = pygame.font.Font(os.path.join(
                            "resources", "fonts",
                            "TranscendsGames.otf"), 24)
        self.running = True
        self.screensize = screen.get_size()
        self.currentItem = None
        self.titlerect = self.title.get_rect()
        self.titlerect.x = self.screensize[0]/2 - self.titlesize[0] / 2
        self.titlerect.y = 32
        self.background = pygame.image.load(
                          os.path.join("resources",
                                       "UI",
                                       "back.png")).convert_alpha()
        self.newgameimg = self.font.render("Resume Game", False,
                                           (255, 255, 255))
        self.selectedimg = self.font.render("Resume Game", False, (255, 0, 0))
        self.saveimg = self.font.render("Save Game", False, (255, 255, 255))
        self.saveselected = self.font.render("Salve Game", False, (255, 0, 0))
        self.exitimg = self.font.render("Quit to Desktop",
                                        False, (255, 255, 255))
        self.exitselected = self.font.render("Quit to Desktop",
                                             False, (255, 0, 0))
        self.menu = self.font.render("Main Menu",
                                     False, (255, 255, 255))
        self.menusel = self.font.render("Main Menu",
                                        False, (255, 0, 0))
        self.newgame = menuItem.menuitem(self.newgameimg,
                                         self.selectedimg,
                                         (320, 240),
                                         lambda: self.unpause())
        self.savegame = menuItem.menuitem(self.saveimg,
                                          self.saveselected,
                                          (320, 320), lambda: game.saveGame())
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (320, 400),
                                          lambda: self.goToMenu(game))
        self.exit = menuItem.menuitem(self.exitimg,
                                      self.exitselected,
                                      (320, 560), lambda: quit())
        self.items = [self.newgame, self.savegame, self.mainmenu, self.exit]
        self.clock = pygame.time.Clock()
        while self.running:
            self.dt = self.clock.tick(30)/1000.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
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
            self.titletime += self.dt
            if self.titletime >= self.titletimings[self.titleani.currentframe]:
                self.title = self.titleani.next()
                self.titletime = 0
            screen.blit(self.background, (0, 0))
            screen.blit(self.title, self.titlerect.topleft)
            for item in self.items:
                screen.blit(item.image, item.rect.topleft)
            screen.blit(self.newgame.image, self.newgame.location)
            pygame.display.update()
