# Main Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os
from components.UI import menuItem
from game import Game
from libs import animation


class menu:

    def main(self, screen, keys):
        # self.title = pygame.image.load(
        #        os.path.join("resources", "UI", "title.png")).convert_alpha()
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
        self.newgameimg = self.font.render("NewGame", False, (255, 255, 255))
        self.selectedimg = self.font.render("NewGame", False, (255, 0, 0))
        self.exitimg = self.font.render("Quit", False, (255, 255, 255))
        self.exitselected = self.font.render("Quit", False, (255, 0, 0))
        if not os.path.exists(os.path.join("SaveGame.dat")):
            self.cont = self.font.render("Continue Game", False, (100, 100, 100))
            self.contgame = menuItem.menuitem(self.cont,
                                              self.cont,
                                              (320, 320),
                                              lambda: None)
        else:
            self.cont = self.font.render("Continue Game", False, (255, 255, 255))
            self.contsel = self.font.render("Continue Game", False, (255, 0, 0))
            self.contgame = menuItem.menuitem(self.cont,
                                          self.contsel,
                                          (320, 320),
                                          lambda: Game().main(screen, keys,
                                                              "load"))
        self.newgame = menuItem.menuitem(self.newgameimg,
                                         self.selectedimg,
                                         (320, 240),
                                         lambda: Game().main(screen, keys,
                                                             "newgame"))
        self.exit = menuItem.menuitem(self.exitimg,
                                      self.exitselected,
                                      (320, 560), lambda: quit())
        self.items = [self.newgame, self.contgame, self.exit]
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
        pygame.quit()
        quit()
