# Main Menu Component
# Part of the Glitch_Heaven project
# Copyright 2015 Penaz <penazarea@altervista.org>
import pygame
import os
from components.UI import menuItem
from libs import animation, timedanimation


class ControlSettings:
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
        self.running = False

    def main(self, screen, keys):
        """
        The main method to show and make the menu work

        Keyword Arguments:
        - Screen: the Screen surface to make the menu on
        - Keys: The list of control keys to use
        - game: The game instance.

        Returns:
        - Nothing
        """
        self.screensize = screen.get_size()
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
        """
        # Video Settings menu element
        # v------------------------------------------------------------------v
        self.videoimg = self.font.render("Video Settings", False,
                                         (255, 255, 255)).convert_alpha()
        self.vidselimg = self.font.render("Video Settings", False,
                                          (255, 0, 0)).convert_alpha()
        self.video = menuItem.menuitem(self.videoimg,
                                       self.vidselimg,
                                       (320, 240),
                                       lambda: VideoSettings.main())
        # ^------------------------------------------------------------------^
        # Sound settings menu element
        # v------------------------------------------------------------------v
        self.sndimg = self.font.render("Audio Settings", False,
                                       (255, 255, 255)).convert_alpha()
        self.sndselimg = self.font.render("Audio Settings", False,
                                          (255, 0, 0)).convert_alpha()
        self.snd = menuItem.menuitem(self.sndimg,
                                     self.sndselimg,
                                     (320, 320), lambda: AudioSettings.main())
        # ^------------------------------------------------------------------^
        # Controls/Controllers menu element
        # v------------------------------------------------------------------v
        self.ctrlimg = self.font.render("Control Settings",
                                        False, (255, 255, 255)).convert_alpha()
        self.ctrlselimg = self.font.render("Control Settings", False,
                                           (255, 0, 0)).convert_alpha()
        self.ctrl = menuItem.menuitem(self.ctrlimg,
                                      self.ctrlselimg,
                                      (320, 400),
                                      lambda: ControlSettings.main())"""
        # ^------------------------------------------------------------------^
        # "Main Menu" menu element
        # v------------------------------------------------------------------v
        self.menu = self.font.render("Main Menu",
                                     False, (255, 255, 255)).convert_alpha()
        self.menusel = self.font.render("Main Menu",
                                        False, (255, 0, 0)).convert_alpha()
        self.mainmenu = menuItem.menuitem(self.menu,
                                          self.menusel,
                                          (320, 560),
                                          lambda: self.goToMenu())
        # ^------------------------------------------------------------------^
        self.items = [self.mainmenu]
        self.clock = pygame.time.Clock()
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
            pygame.display.update()