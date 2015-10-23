# Main Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os
from components.UI import menuItem


class menu:

    def main(self, screen, keys):
        self.title = pygame.image.load(
                os.path.join("resources", "UI", "title.png")).convert_alpha()
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
        self.newgameimg = self.font.render("NewGame", False, (255, 255, 255))
        self.selectedimg = self.font.render("NewGame", False, (255, 0, 0))
        self.newgame = menuItem.menuitem(self.newgameimg,
                                         self.selectedimg,
                                         (320, 240))
        self.clock = pygame.time.Clock()
        while self.running:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if self.currentItem is None:
                        self.currentItem = 0
                    if event.key == keys["down"]:
                        print("down")
                    if event.key == keys["up"]:
                        print("up")
                    if event.key == keys["confirm"]:
                        print("enter")
                    if event.key == keys["escape"]:
                        print("esc")
                if event.type == pygame.MOUSEMOTION:
                    if self.currentItem == 0:
                        self.currentItem = None
                    if self.newgame.rect.collidepoint(*pygame.mouse.get_pos()):
                        self.newgame.makeSelected()
                    else:
                        self.newgame.makeUnselected()
            screen.blit(self.title, (self.titlerect.x, self.titlerect.y))
            screen.blit(self.newgame.image, self.newgame.location)
            pygame.display.update()